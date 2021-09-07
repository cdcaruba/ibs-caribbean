# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleInherit(models.Model):
    _inherit = 'sale.order'

    _check_company_auto = True

    company_id = fields.Many2one('res.company')
    contact_person = fields.Char(string='Contact Person', check_company=True)
    company = fields.Char(string='Company', check_company=True)
    billing_contact = fields.Char(string='Billing Contact', related='partner_invoice_id.child_ids.name')
    email = fields.Char(string='Email', related='partner_invoice_id.email')
    billing_email = fields.Char(string='Billing Email', related='partner_invoice_id.child_ids.email')
    telephone = fields.Char(string='Telephone', related='partner_invoice_id.phone')
    billing_telephone = fields.Char(string='Billing Telephone', related='partner_invoice_id.child_ids.phone')
    recurring_period = fields.Char(string='Recurring Period')
    term_and_condition = fields.Char(string='Terms & Conditions')
    contract = fields.Char(string='Contract')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    # def write(self, values):
    #     """Override default Odoo write function and extend."""
    #     # Do your custom logic here
    #     return super(SaleInherit, self).write(values)

    # <!********** Email Notification **********>
    @api.onchange('signed_by')
    def _onchange_signed_by(self):

        def mail_reminder(self):
            assign_to_user = self.env['sale.order'].search([('email_sent', '=', False)])
            for session in assign_to_user:
                if session.email_sent is False:
                    session.mail_reminder_abc()
                    session.email_sent = True

        def mail_reminder_abc(self):
            # user_group = self.env.ref("sudo_incident.incident_manager_security")
            # email_list = [usr.partner_id.email for usr in user_group.users if usr.partner_id.email]
            #
            # user_group_l1 = self.env.ref("sudo_incident.incident_group_l1_security")
            # email_group_l1 = [usr.partner_id.email for usr in user_group_l1.users if usr.partner_id.email]
            user_current = self.partner_id.email
            user = self.user
            log = self.user_id
            abc = self.user_id.login
            all_eamils = [log]
            all_eamils.extend(user_current)
            # all_eamils.extend(email_group_l1)

            for email in all_eamils:
                template_rec = self.env.ref('so_customization.mail_template_so_mail')
                template_rec.write({'email_to': email})
                template_rec.send_mail(self.id, force_send=True)
    # <!**********End of Email Notification **********>


