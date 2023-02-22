# -*- coding: utf-8 -*-
{
    'name': "Medical Inspection",

    'summary': """
     Medical Inspection """,

    'description': """
        Medical Inspection
    """,

    'author': "Agile Solutions",
    'website': "http://www.agileitsolution.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['almulazmeen_custom'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/medical_inspection.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
