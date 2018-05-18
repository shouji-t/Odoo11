# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = "res.company"

    #SsPj class Many2one - David Tang
    #１対多項目のため、目的モデルで正反対の多対１関係を実装する
    pj_ids = fields.One2many('ss.pj', 'company_id', 'Pj')
