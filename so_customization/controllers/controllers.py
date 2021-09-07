# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.sale.controllers.portal import CustomerPortal

from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.osv import expression


class CustomerPortalInherit(CustomerPortal):
    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        res = super(CustomerPortalInherit, self).portal_order_page( order_id, report_type=None, access_token=None, message=False, download=False, **kw)
        order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        order_sudo['type_name'] = 'Proposal'

        return res


        # values = {
        #     'sale_order': order_sudo,
        #     # 'message': message,
        #     # 'token': access_token,
        #     # 'return_url': '/shop/payment/validate',
        #     # 'bootstrap_formatting': True,
        #     'email': order_sudo.email,
        #     'telephone': order_sudo.telephone,
        #     # 'report_type': 'html',
        #     # 'action': order_sudo._get_portal_return_action(),
        # }
        #
        # return request.render('so_customization.inherit_sale_template_new', values, res)
        # return request.render('sale.sale_order_portal_template', values, res)

       


