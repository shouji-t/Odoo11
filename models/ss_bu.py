# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class SsBu(models.Model):
    _name = 'ss.bu'

    bu_id = fields.Char('bu_id')
    name = fields.Char('Name')

    _sql_constraints = [
        ('unique_bu_id',
         'unique(bu_id)', 'bu_id should be unique per bu!')]


