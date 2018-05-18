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
    account_pj_date = fields.Char('経理年月', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, readonly = True,
        default=lambda self: self.env.user.company_id.id)

    partner_id = fields.Many2one('res.partner', 'Partner')
    type = fields.Selection([('contract', u'請負'), ('dispatch', u'派遣')], u'種別')

    # PJ管理
    pj_startdate = fields.Date('PJ開始日',default=fields.Date.context_today, required=True)
    pj_enddate = fields.Date('PJ予定終了日',default=fields.Date.context_today, required=True)

    # 追加フィールド
    status = fields.Selection([('order', u'見積'), ('inprogress', u'進行中'), ('end', u'終了'), ('cancel', u'中止')], u'状態')
    sales_amount = fields.Char('売上金額')

    pj_sub_ids = fields.One2many('ss.pj.detail', 'pj_sub_id', 'PjDetail')

class SsPjDetail(models.Model):

    _name = 'ss.pj.detail'

    # pj_id = fields.Char('pj_id', required=True)
    name = fields.Char('担当者名', required=True)

    #  pj_idとnameフィールドを使うために、ss.pjモデルを継承する。
    # _inherit = 'ss.pj'

    # pj_sub_id = fields.Char(u'pj_sub_id')
    pj_sub_id = fields.Many2one('ss.pj', 'pj_sub_id')
    employee_id = fields.Char(u'要員ID')
    employee_type = fields.Char(u'要員区分')
    price_unit = fields.Integer(u'売上単価')
    price_purchase = fields.Integer(u'元単価')
    duty_lowerlimit = fields.Integer(u'精算下限')
    duty_upperlimit = fields.Integer(u'精算上限')
    price_base = fields.Integer(u'下限単価')
    price_upperlimit = fields.Integer(u'上限単価')
    manhour = fields.Float(u'当月工数')
    hours = fields.Char(u'当月時間')
    hours_lowerlimit = fields.Integer(u'当月下限')
    hours_upperlimit = fields.Integer(u'当月上限')
    payoffhour = fields.Char(u'精算時間')
    amount = fields.Char(u'売上')

    excess_deduct = fields.Char(u'超過・控除')

    # 小計項目を追加する
    subtotal = fields.Integer(u'小計', compute='_compute_subtotal')

    carfare = fields.Integer(u'交通費')
    amount_subtotal = fields.Integer(u'売上合計')

     # PJを取る
    pj_id = fields.Char(related="pj_sub_id.pj_id", string="PJコード")
    pj_name = fields.Char(related="pj_sub_id.name", string="PJ名称")
    pj_account_date = fields.Char(related="pj_sub_id.account_pj_date", string="経理年月")

    # 計算項目テスト
    @api.depends('amount')
    def _compute_subtotal(self):
        self.subtotal =  self.amount



