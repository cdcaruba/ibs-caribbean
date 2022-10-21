from odoo import models, fields, api


class DigitalPropsalConditions(models.Model):
    _name = 'digital.propsal.conditions'

    name = fields.Char("Tittle", required=True)
    conditions = fields.Text("Terms and Conditions", required=True)
    

class DigitalRecurringPeriod(models.Model):
    _name = 'digital.recurring.period'

    name = fields.Char(string="Name", required=True) 