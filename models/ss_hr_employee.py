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
    x_member_type = fields.Selection([
        ('employee', u'社員'),
        ('bp', u'BP'),
        ('personal', u'個人'),
    ], string=u'要員区分')
    x_cost = fields.Integer('原価')

    # x_department_cd = fields.Char('部門コード')
    # hr.departmentのx_department_cdフィールドを取るため
    x_department_cd = fields.Char('BUコード', related='department_id.x_department_cd')
    x_department_name = fields.Char('BU名', related='department_id.name', readonly = True)
    x_partner_id = fields.Many2one('res.partner', u'仕入先', domain=[('supplier', '=', True)])
    x_kinmu_kubun = fields.Many2one('ss.kubun', '勤務区分')
