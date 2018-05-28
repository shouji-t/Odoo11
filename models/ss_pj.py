# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class SsPjOrder(models.Model):
    _inherit = "sale.order"

    pj_id = fields.Char('PJコード', size=12,  required=True)
    pj_account_date = fields.Char('経理年月', required=True)

    pj_type = fields.Selection([
        ('contract', u'請負'),
        ('dispatch', u'派遣'),
        ('maintaining', u'保守'),
        ('other', u'その他'),
        ], string='種別')

    # BU
    pj_bu_cd = fields.Many2one('hr.department', 'BUコード')
    pj_bu_name = fields.Char('BU名')

    # PJ管理
    pj_state = fields.Selection([
        ('new', '新規'),
        ('run', '稼働中'),
        ('cancel', '終止'),
        ('done', '終了'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='new')
    pj_startdate = fields.Date('PJ開始日',default=fields.Date.context_today, required=True)
    pj_enddate = fields.Date('PJ予定終了日',default=fields.Date.context_today, required=True)

class SsPjOrderLine(models.Model):
    _inherit = "sale.order.line"

    # pj_id = fields.Char('pj_id', required=True)
    name = fields.Char('担当者名', required=True)

    pj_member_id = fields.Many2one('hr.employee', string='要員')
    pj_member_type = fields.Selection([
        ('employee', u'社員'),
        ('bp', u'BP'),
        ('personal', u'個人'),
        ], string='要員区分')
    pj_price_unit = fields.Integer(u'売上単価')
    pj_price_purchase = fields.Integer(u'元単価')
    pj_is_duty = fields.Boolean(u'精算')
    pj_duty_lowerlimit = fields.Integer(u'精算下限')
    pj_duty_upperlimit = fields.Integer(u'精算上限')
    pj_price_lowerlimit = fields.Integer(u'下限単価', compute='_compute_pj_price_lowerlimit')
    pj_price_upperlimit = fields.Integer(u'上限単価', compute='_compute_pj_price_upperlimit')
    pj_manhour = fields.Float(u'当月工数')
    pj_duty_hours = fields.Char(u'当月時間')
    pj_hours_lowerlimit = fields.Integer(u'当月下限')
    pj_hours_upperlimit = fields.Integer(u'当月上限')
    pj_payoffhour = fields.Integer(u'精算時間', compute='_compute_pj_payoffhour')
    pj_amount = fields.Char(u'売上', compute='_compute_pj_amount')
    pj_excess_deduct = fields.Integer(u'超過・控除', compute='_compute_pj_excess_deduct')

    # 小計項目を追加する
    pj_subtotal = fields.Integer(u'小計', compute='_compute_pj_subtotal')

    pj_carfare = fields.Integer(u'交通費')
    pj_amount_subtotal = fields.Integer(u'売上合計', compute='_compute_pj_amount_subtotal')

     # PJを取る
    pj_id = fields.Char(related="pj_sub_id.pj_id", string="PJコード")
    pj_name = fields.Char(related="pj_sub_id.name", string="PJ名称")
    pj_account_date = fields.Char(related="pj_sub_id.account_pj_date", string="経理年月")

    # 計算項目
    @api.depends('pj_price_unit', 'pj_duty_lowerlimit')
    def _compute_pj_price_lowerlimit(self):
        if self.pj_duty_lowerlimit:
            self.pj_duty_lowerlimit =  self.pj_price_unit / self.pj_duty_lowerlimit

    @api.depends('pj_price_unit', 'pj_duty_upperlimit')
    def _compute_pj_price_upperlimit(self):
        if self.pj_duty_lowerlimit:
            self.pj_duty_lowerlimit =  self.pj_price_unit / self.pj_duty_lowerlimit

    @api.depends('pj_duty_lowerlimit', 'pj_duty_upperlimit', 'pj_duty_hours')
    def _compute_pj_payoffhour(self):
        if self.pj_duty_hours and (self.pj_duty_hours < self.pj_duty_lowerlimit):
            self.pj_payoffhour =  self.pj_duty_hours - self.pj_duty_lowerlimit
        elif self.pj_duty_hours and (self.pj_duty_hours > self.pj_duty_upperlimit):
            self.pj_payoffhour =  self.pj_duty_hours - self.pj_duty_upperlimit

    @api.depends('pj_duty_hours')
    def _compute_pj_excess_deduct(self):
        if self.pj_payoffhour and self.pj_payoffhour < 0:
            self.pj_excess_deduct =  self.pj_price_lowerlimit * self.pj_payoffhour
        elif self.pj_payoffhour and self.pj_payoffhour > 0:
            self.pj_excess_deduct =  self.pj_price_upperlimit * self.pj_payoffhour

    #売上
    @api.depends('pj_price_unit', 'pj_manhour')
    def _compute_pj_amount(self):
        self.pj_amount =  self.pj_price_unit * self.pj_manhour

    #小計
    @api.depends('amount')
    def _compute_pj_subtotal(self):
        self.pj_subtotal =  self.pj_amount + self.pj_excess_deduct

    #売上合計
    @api.depends('amount')
    def _compute_pj_amount_subtotal(self):
        self.pj_amount_subtotal =  self.pj_subtotal + self.pj_carfare


