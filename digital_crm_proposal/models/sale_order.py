from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"


    is_proposal = fields.Boolean("Proposal Available", related="company_id.is_proposal")
    billing_email = fields.Char("Billing Email")
    billing_phone = fields.Char("Billing Phone")
    contact_person_id = fields.Many2one('res.partner', domain="[('parent_id','=',partner_id)]" , string="Contact Person")
    contact_email = fields.Char("Contact Email")
    contact_phone = fields.Char("Contact Phone")
    start_date = fields.Date("Start Date", defaults=fields.Date.today)
    end_date = fields.Date("End Date", defaults=fields.Date.today)
    conditions_id = fields.Many2one('digital.propsal.conditions', string="Conditions")
    recurring_id = fields.Many2one('digital.recurring.period', string="Recurring Period")

   
            
    @api.onchange('partner_invoice_id')
    def onchange_partner_invoice_id_propsal(self):
        if self.partner_invoice_id:
            self.billing_email = self.partner_invoice_id.email
            self.billing_phone = self.partner_invoice_id.phone


    @api.onchange('contact_person_id')
    def onchange_contact_person_id_propsal(self):
        if self.contact_person_id:
            self.contact_email = self.contact_person_id.email
            self.contact_phone = self.contact_person_id.phone

    @api.onchange('conditions_id')
    def onchange_conditions_id(self):
        if self.conditions_id:
            self.note = self.conditions_id.conditions


    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if res['name'] and self.env.company.is_proposal:
            res['name'] = "%(number)s %(company_name)s" %{
                        'number': res['name'], 
                        'company_name': res['partner_id'].name
                    }        
        return res

    
    @api.depends('state')
    def _compute_type_name(self):
        for record in self:
            if record.is_proposal:
                record.type_name = _('Proposal') if record.state in ('draft', 'sent', 'cancel') else _('Advertising Agreement')
            else:
                record.type_name = _('Quotation') if record.state in ('draft', 'sent', 'cancel') else _('Sales Order')


        
    def _find_mail_template(self, force_confirmation_template=False):
        """
            Change email tamplate only for proposal company 
        """
        template_id = False

        if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
            if self.is_proposal:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('digital_crm_proposal.mail_template_sale_confirmation_degital', raise_if_not_found=False)
            else:
                template_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_confirmation_template'))
                template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                if self.is_proposal:
                    template_id = self.env['ir.model.data'].xmlid_to_res_id('digital_crm_proposal.mail_template_sale_confirmation_degital', raise_if_not_found=False)
                else:
                    template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.mail_template_sale_confirmation', raise_if_not_found=False)
        if not template_id:
            if self.is_proposal:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('digital_crm_proposal.email_template_edi_proposal_digital', raise_if_not_found=False)
            else:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.email_template_edi_sale', raise_if_not_found=False)

        return template_id
    
    


    # Change reports base on Conditins
    
    @api.model
    def fields_view_get(self, view_id=None, view_type='tree', toolbar=False, submenu=False):

        # if view_id:
        user_company = self.env.company
        if user_company.is_proposal:
            reports = self.env['ir.actions.report'].search([('model','=','sale.order' )])
            for report in reports:
                report_name = report.name.split("/")
                if len(report_name) >1:
                    if report.name.split(" ")[0].lower().replace(" ","")=="proposal":
                        report.create_action()
                    elif report.name.split(" ")[0].lower().replace(" ","")=="quotation":
                        report.unlink_action()
        else:
            reports = self.env['ir.actions.report'].search([('model','=','sale.order' )])
            for report in reports:
                report_name = report.name.split("/")
                if len(report_name) >1:
                    if report.name.split(" ")[0].lower().replace(" ","")=="proposal":
                        report.unlink_action()
                    elif report.name.split(" ")[0].lower().replace(" ","")=="quotation":
                        report.create_action()

        return super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)


    def action_confirm(self):     

        if  self.is_proposal :  
            partner_emails = ['angeloquandus@ibs.group','keananmaxwell@ibs.group']
            followers = []
            for emails in partner_emails: 
                partner_ids = self.env['res.partner'].search([('email','=',emails)], limit=1).id
                followers.append(partner_ids)
            self.message_subscribe(followers)  
        return super(SaleOrder, self).action_confirm()  
