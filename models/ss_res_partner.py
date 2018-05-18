# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    x_partner_cd = fields.Char('顧客コード')

    #SsPj class Many2one - David Tang
    #１対多項目のため、目的モデルで正反対の多対１関係を実装する
    pj_ids = fields.One2many('ss.pj', 'partner_id', 'Pj')
