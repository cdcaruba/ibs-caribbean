from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    is_proposal = fields.Boolean("Proposal Available", related="company_id.is_proposal")
    billing_email = fields.Char("Billing Email")
    billing_phone = fields.Char("Billing Phone")
    contact_person_id = fields.Many2one('res.partner', domain="[('parent_id','=',partner_id)]" , string="Contact Person")
    contact_email = fields.Char("Contact Email")
    contact_phone = fields.Char("Contact Phone")
    start_date = fields.Date("Start Date", defaults=fields.Date.today)
    end_date = fields.Date("End Date", defaults=fields.Date.today)
    recurring_id = fields.Many2one('digital.recurring.period', string="Recurring Period")

    @api.onchange('partner_shipping_id')
    def onchange_partner_invoice_id_propsal(self):
        if self.partner_shipping_id:
            self.billing_email = self.partner_shipping_id.email
            self.billing_phone = self.partner_shipping_id.phone


    @api.onchange('contact_person_id')
    def onchange_contact_person_id_propsal(self):
        if self.contact_person_id:
            self.contact_email = self.contact_person_id.email
            self.contact_phone = self.contact_person_id.phone