# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class SsPj(models.Model):
    _name = 'ss.pj'

    pj_id = fields.Char('pj_id', required=True)
    name = fields.Char('Name', required=True)

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, readonly = True,
        default=lambda self: self.env.user.company_id.id)

    partner_id = fields.Many2one('res.partner', 'Partner')
    type = fields.Selection([('contract', u'請負'), ('dispatch', u'派遣')], u'種別')
    employee_id = fields.Char(u'要員ID')
    employee_type = fields.Char(u'要員区分')
    price_unit = fields.Integer(u'売上単価')
    price_purchase = fields.Integer(u'元単価')
    duty_lowerlimit = fields.Integer(u'精算下限')
    duty_upperlimit = fields.Integer(u'精算上限')
    price_base = fields.Integer(u'下限単価')
    price_upperlimit = fields.Integer(u'上限単価')

   _sql_constraints = [
        ('unique_pj_id',
         'unique(pj_id)', 'pj_id should be unique per pj!')]

class SsPjDetail(models.Model):


    # _name = 'ss.pj.detail'

    # pj_id = fields.Char('pj_id', required=True)
    # name = fields.Char('Name', required=True)

    #  pj_idとnameフィールドを使うために、ss.pjモデルを継承する。
    _inherit = 'ss.pj'

    pj_sub_id = fields.Char(u'SUBID')
    manhour = fields.Float(u'当月工数')
    hours = fields.Char(u'当月時間')
    hours_lowerlimit = fields.Integer(u'当月下限')
    hours_upperlimit = fields.Integer(u'当月上限')
    payoffhour = fields.Char(u'精算時間')
    amount = fields.Char(u'売上')

    # 小計項目を追加する
    subtotal = fields.Char(u'小計テスト', compute='_compute_subtotal')

    carfare = fields.Char(u'交通費')
    amount_total = fields.Char(u'売上合計')

    # 計算項目テスト
    @api.depends('amount')
    def _compute_subtotal(self):
        self.subtotal =  self.amount



