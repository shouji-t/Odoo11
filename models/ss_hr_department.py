# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class SsHrDepartment(models.Model):
    _inherit = 'hr.department'
    _rec_name = 'x_department_cd'

    x_department_cd = fields.Char('部門コード', index=True)

    budget_ids = fields.One2many('ss.budget', 'department', 'Budgets in this department')

    # フォームリスト部門コード
    # def name_get(self):
    #     result = [] 
    #     for record in self:
    #         result.append((record.id, record.x_department_cd)) 
    #     return result