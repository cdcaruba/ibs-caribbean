# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Quotation Builder PDF",

    'summary': """
        Quotation Builder PDF""",

    'description': """
        Enables the printed PDF of the quotation to display the same modifications
        as the portal view. Text and image customizations done with Odoo's Quotation
        Builder will be displayed on the PDF. The animated and complex widgets
        designed for the webiste will not be displaid on the report.
    """,
    'author': "Odoo Inc",
    'website': "http://www.odoo.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['sale_quotation_builder', 'website', 'web_enterprise'],
    'data': [
        'views/assets.xml',
        'reports/sale_report.xml',
    ],
}
