# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "quotation_builder_pdf",

    'summary': """
        Quotation Builder PDF""",

    'description': """
        Enables the printed PDF of the quotation to display the same modifications
        as the portal view. Every customization done with Odoo's Quotation Builder
        will be displayed on the PDF.
    """,
    'author': "Odoo Inc",
    'website': "http://www.odoo.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['sale_quotation_builder'],
    'data': [
        'views/assets.xml',
        'reports/sale_report.xml',
    ],
}
