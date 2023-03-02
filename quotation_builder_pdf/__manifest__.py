# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Quotation Builder PDF",

    'summary': """
        Quotation Builder PDF""",

    'description': """
        Task #2314417 - Enables the printed PDF of the quotation to display the same modifications
        as the portal view. Text and image customizations done with Odoo's Quotation
        Builder will be displayed on the PDF. The animated and complex widgets
        designed for the webiste will not be displayed on the report.
    """,
    'author': "Odoo Inc",
    'website': "http://www.odoo.com",
    'category': 'Custom Development',
    'version': '15.0.1.0.0',
    "license": "OPL-1",
    'depends': ['sale_quotation_builder', 'website', 'web_enterprise'],
    'data': [
        'data/report_paperformat.xml',
        'reports/sale_report.xml',
        'reports/layout_report.xml',
    ],
    'assets': {
        'web.assets_common': [
            'quotation_builder_pdf/static/src/css/report_assets_common.css',
        ],
    },
    "cloc_exclude": {
        "./**/*"
    }
}
