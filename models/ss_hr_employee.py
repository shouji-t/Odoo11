# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class SsEmployee(models.Model):
    _inherit = "hr.employee"

    x_employee_cd = fields.Char('従業員コード')
    x_kata = fields.Char('かたかな')

    # x_department_cd = fields.Char('部門コード')
    # hr.departmentのx_department_cdフィールドを取るため
    x_department_cd = fields.Char('部門コード', related='department_id.x_department_cd')

    x_kinmu_kubun = fields.Many2one('ss.kubun', '勤務区分')
