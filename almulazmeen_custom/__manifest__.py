# -*- coding: utf-8 -*-
{
    'name': "Almulazmeen Customization",

    'summary': """
     Almulazmeen Customization """,

    'description': """
        Almulazmeen Customization
    """,

    'author': "Agile Solutions",
    'website': "http://www.agileitsolution.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale','hr_contract','om_account_accountant','account_invoice_pricelist'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/pos.xml',
        'views/hr_contract.xml',
        'views/hr.xml',
        'views/product.xml',
        'views/account.xml',
        'views/res_partner.xml',
        'views/medical.xml',
        'views/appointment.xml',
        'views/price_list.xml',
        'views/lab.xml',
        'views/room.xml',
        'views/operations.xml',
        'views/drug.xml',
        'views/sale.xml',
        'report/doctor_visits.xml',
        'report/patient_report.xml',
        'report/med_insurance_report_temp.xml',
        'wizard/med_insurance_report.xml',
        'wizard/doctor_visit.xml',
        'wizard/doctor_visit_invoice.xml',
        'data/appointment.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
