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
    'version': '11.0.1.0.24',
    'license': 'LGPL-3',
    'category': 'MSD',
    "sequence": 1,
    'summary': 'MSD Ssm (Sales Support Management) System. 024',
    'complexity': "easy",
    'author': 'Msd Cloud Integration',
    'website': 'http://www.msdcorp.co.jp',
    'depends': ['crm', 'sale', 'base', 'hr', 'hr_expense'],
    'data': [
        'views/dumy_view.xml',
        'views/ss_res_partner_view.xml',
        'views/ss_crm_lead_view.xml',
        'views/ss_hr_department_view.xml',
        'views/ss_hr_employee_view.xml',
        'views/ss_tax_view.xml',
        'views/ss_cost_view.xml',
        'views/ss_costrank_view.xml',
        'views/ss_budget_view.xml',
        'views/ss_pj_view.xml',
        'views/ss_order_view.xml',
        'views/ss_sales_view.xml',
        'views/ss_sales_wizard_view.xml',
        'views/ss_sales_invoice_wizard_view.xml',
        'report/report_menu.xml',
        'report/ss_pj_report_views.xml',
        'report/ss_sales_report_views.xml',
        'report/ss_sales_reporta_views.xml',
        'report/ss_sales_reportz_views.xml',
        'report/ss_member_expiring_report_views.xml',
        'report/ss_sales_invoicea_views.xml',
        # 'report/report_ss_order.xml',
        # 'report/ss_pj_order_report_views.xml',
        'report/ss_budget_report_views.xml',
        'security/ssm_security.xml',
        'security/ir.model.access.csv',
        'menu/ss_menu.xml',
        # 'data/ir_sequence_data.xml',
    ],
    'demo': [
        # 'demo/dumy_demo.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
