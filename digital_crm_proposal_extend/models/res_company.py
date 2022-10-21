from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    is_proposal = fields.Boolean("Proposal Available", default=False)
    attach_terms_conditions = fields.Many2many('ir.attachment', 'terms_attachment_rel', 'company_id', 'attach_id', string="Terms and Conditions")