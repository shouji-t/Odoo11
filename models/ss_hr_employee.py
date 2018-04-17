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
    x_department_cd = fields.Char('部門コード')
