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

    x_regdate = fields.Datetime('申請日', default=fields.Datetime.now, required=True, readonly=True, copy=False)
    x_regstatus = fields.Selection([
        ('regist', u'申請中'),
        ('process', u'処理中'),
        ('done', u'終了'),
        ('cancel', u'廃棄'),
        ], string='新規申請状態', default='regist', copy=False)
    x_contract = fields.Boolean('契約書', default=False)
    x_order = fields.Boolean('注文書', default=False)
    x_purchase = fields.Boolean('発注書', default=False)
