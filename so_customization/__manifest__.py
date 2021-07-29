# -*- coding: utf-8 -*-
{
    'name': "SO Customization",

    'summary': """This module is designed for SO CRM and Sale Template customization""",

    'description': """This module is designed for SO CRM and Sale Template customization""",

    'author': "Sofftar",
    'website': "http://www.sofftar.com",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'sale_management', 'account','crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/inherit_invoice.xml',
        'data/so_cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
