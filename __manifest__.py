# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

{
    'name': 'Ssm',
    'version': '11.0.1.0.1',
    'license': 'LGPL-3',
    'category': 'ERP',
    "sequence": 1,
    'summary': 'MSD Ssm (Sales Support Management) System. OOO',
    'complexity': "easy",
    'author': 'Msd Cloud Integration',
    'website': 'http://www.msdcorp.co.jp',
    'depends': ['crm','sale','base'],
    'data': [
        'views/dumy_view.xml',
        'views/ss_res_partner_view.xml',
        'views/ss_crm_lead_view.xml',
        'views/ss_hr_department_view.xml',
        'views/ss_hr_employee_view.xml',
        'views/ss_crm_lead_view.xml',
        'views/ss_pj_view.xml',
        'views/ss_budget_view.xml',
        'menu/ss_menu.xml',
    ],
    'demo': [
        'demo/dumy_demo.xml',
        'demo/bu_demo.xml',
        'demo/pj_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
