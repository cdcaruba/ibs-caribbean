
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

{
    "name": "Digital View Quotation to propsal",
    "version": "13.0.1.0.0",
    'sequence': 5,
    "category": "Customer Relationship Management",
    "author": "Dinuth perera",
    "license": "AGPL-3",
    "depends": ["crm","sale"],
    "data": [
        'security/ir.model.access.csv',
        'reports/sale_documents.xml',
        'data/mail_template.xml',
        'views/res_company.xml',
        'views/sale_order.xml',
        'views/account_move.xml',
        'views/views.xml',
        'views/sale_customer_portal.xml',
    ],
    
    "installable": True,
    'application': True,
}