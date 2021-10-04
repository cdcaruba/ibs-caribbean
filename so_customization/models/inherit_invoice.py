# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InvoiceInherit(models.Model):
    _inherit = 'account.move'

    contact_person = fields.Char(string='Contact Person')
    company = fields.Char(string='Company')
    billing_contact = fields.Char(string='Billing Contact')
    email = fields.Char(string='Email')
    billing_email = fields.Char(string='Billing Email')
    telephone = fields.Char(string='Telephone')
    billing_telephone = fields.Char(string='Billing Telephone')
    recurring_period = fields.Char(string='Recurring Period')
    term_and_condition = fields.Char(string='Terms & Conditions')
    contract = fields.Char(string='Contract')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

