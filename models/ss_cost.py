# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class SsCost(models.Model):
    _name = 'ss.cost'
    _order = 'employee_cd'

    pj_account_date = fields.Char(u'経理年月', index=True)
    employee_id = fields.Many2one('hr.employee', string='要員', index=True)
    employee_cd = fields.Char(string='要員コード', related='employee_id.x_employee_cd', store=True)
    employee_cost = fields.Integer('原価' )
    employee_rank = fields.Char('原価ランク' )

