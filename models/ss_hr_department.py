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
    _inherit = "hr.department"

    x_department_cd = fields.Char('部門コード', index=True)
