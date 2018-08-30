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
    'version': '11.0.1.0.8',
    'license': 'LGPL-3',
    'category': 'ERP',
    "sequence": 1,
    'summary': 'MSD Ssm (Sales Support Management) System. OO8',
    'complexity': "easy",
    'author': 'Msd Cloud Integration',
    'website': 'http://www.msdcorp.co.jp',
    'depends': ['crm','sale','base','hr','hr_expense'],
    'data': [
        'views/dumy_view.xml',
        'views/ss_res_partner_view.xml',
        'views/ss_crm_lead_view.xml',
        'views/ss_hr_department_view.xml',
        'views/ss_hr_employee_view.xml',
        'views/ss_pj_view.xml',
        'views/ss_pj_order_view.xml',
        'views/ss_budget_view.xml',
        'security/ssm_security.xml',
        'security/ir.model.access.csv',
        'menu/ss_menu.xml',
        'data/ir_sequence_data.xml',
    ],
    'demo': [
        # 'demo/dumy_demo.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
