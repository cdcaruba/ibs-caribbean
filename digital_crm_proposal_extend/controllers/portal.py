import binascii
from datetime import date

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as get_records_pager
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.osv import expression


class CustomerPortal(CustomerPortal):

    @http.route(['/my/orders/<int:order_id>/accept'], type='json', auth="public", website=True)
    def portal_quote_accept(self, order_id, access_token=None, name=None, signature=None):
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid order.')}

        if not order_sudo.has_to_be_signed():
            return {'error': _('The order is not in a state requiring customer signature.')}
        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            order_sudo.write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}

        if not order_sudo.has_to_be_paid():
            order_sudo.action_confirm()
            order_sudo._send_order_confirmation_mail()
        
        pdf = request.env.ref('sale.action_report_saleorder').with_user(SUPERUSER_ID)._render_qweb_pdf([order_sudo.id])[0]
        order_details =  request.env['sale.order'].sudo().search([('id','=',order_id)], limit=1)
        if order_details and order_details.is_proposal:
            pdf = request.env.ref('digital_crm_proposal_extend.action_report_proposal').sudo()._render_qweb_pdf([order_sudo.id])[0]
            # return self._show_report(model=order_sudo, report_type=report_type, report_ref='digital_crm_proposal_extend.action_report_proposal', download=download)
       

        _message_post_helper(
            'sale.order', order_sudo.id, _('Advertising Agreement  has been signed! \n  Yay! We have %s onboard. Copy of the signed agreement is attached.') % (name,),
            attachments=[('%s.pdf' % order_sudo.name, pdf)],
            **({'token': access_token} if access_token else {}))

        query_string = '&message=sign_ok'
        if order_sudo.has_to_be_paid(True):
            query_string += '#allow_payment=yes'
        return {
            'force_refresh': True,
            'redirect_url': order_sudo.get_portal_url(query_string=query_string),
        }

    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        """Overide main portal download function and added condition to replace new proposal template"""
        response = super(CustomerPortal, self).portal_order_page(order_id=order_id, report_type=report_type, access_token=access_token, message=message, download=download, **kw)
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        if report_type in ('html', 'pdf', 'text'):
            order_details = request.env['sale.order'].sudo().search([('id', '=', order_id)], limit=1)
            if order_details and order_details.is_proposal:
                return self._show_report(model=order_sudo, report_type=report_type, report_ref='digital_crm_proposal_extend.action_report_proposal', download=download)
            else:
                return self._show_report(model=order_sudo, report_type=report_type,  report_ref='sale.action_report_saleorder', download=download)

        return response
