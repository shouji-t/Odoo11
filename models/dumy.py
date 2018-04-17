# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class SsDumy(models.Model):
    _name = 'ss.dumy'

    code = fields.Char('code')
    name = fields.Char('Name')
