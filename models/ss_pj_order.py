# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import api, fields, models, _
from calendar import monthrange
from datetime import datetime
import math

class SsPjOrder(models.Model):
    _name = "ss.pj.order"
    _description = "PJ_ORDER"
    _order = 'pj_register_date desc'
    _inherit = "ss.pj"

    pj = fields.Many2one('ss.pj', u'pj')
    pj_order_line = fields.One2many(
        'ss.pj.order.line', 'pj_order_id', string='PJ Order Lines')

    # SS.PJ情報
    # pj_cd = fields.Char(u'PJコード', size=12, store=True, readonly=False)
    # pj_name = fields.Char(u'PJ名', required=True)
    # PJ種別
    # pj_type = fields.Selection([
    #     ('dispatch', u'派遣'),
    #     ('contract', u'請負'),
    #     ('subcontracting', u'業務委託'),
    #     ('quasidelegation', u'準委任'),
    #     ('delegation', u'委任'),
    #     ('maintaining', u'保守'),
    #     ('totalcontract', u'一括請負'),
    #     ('other', u'その他'),
    # ], string=u'種別', required=True)
    #
    # # PJ担当者
    # pj_user_id = fields.Many2one('res.users', string='PJ担当者')
    #
    # # 申請登録
    # pj_register_date = fields.Date(u'登録年月日')
    # pj_register_user_id = fields.Many2one('res.users', string='登録担当者')
    #
    # # 許可
    # pj_permitted_date = fields.Date(u'許可年月日')
    # pj_permitted_user_id = fields.Many2one('res.users', string='許可担当者')
    #
    # # 終了
    # pj_closed_date = fields.Date(u'終了年月日')
    # pj_closed_user_id = fields.Many2one('res.users', string='終了担当者')
    #
    # # BU
    # pj_bu_cd = fields.Many2one('hr.department', u'BUコード', required=True)
    # pj_bu_name = fields.Char(u'BU名', related='pj_bu_cd.name', readonly=True)
    #
    # # 顧客コード
    # pj_partner_id = fields.Many2one('res.partner', string='顧客', domain=[('customer', '=', True)], required=True)
    # pj_partner_cd = fields.Char(u'顧客コード', related='pj_partner_id.x_partner_cd', readonly=True, store=True)
    #
    # # PJ管理
    # pj_state = fields.Selection([
    #     ('new', u'新規'),
    #     ('run', u'稼働中'),
    #     ('cancel', u'終止'),
    #     ('end', u'終了'),
    # ], string='稼働状態', copy=False, index=True, track_visibility='onchange', default='new', required=True)
    #
    # #PJ日付
    # pj_startdate = fields.Date(u'PJ開始日', default=fields.Date.context_today, required=True)
    # pj_enddate = fields.Date(u'PJ予定終了日')
    # pj_total_months = fields.Date(u'PJ実施月数')
    #
    # #PJ検収状態
    # pj_receipted_date = fields.Date(u'検収年月日')
    # pj_receipted_user_id = fields.Many2one('res.users', string='検収担当者')
    #
    # #PJ要員詳細
    # pj_line = fields.One2many('ss.pj.line', 'pj_id', string='PJ Lines')
    #
    #PJ合計金額
    pj_amount_total = fields.Integer(compute='_amount_total')

    #
    # #PJ原価金額
    # pj_cost_total = fields.Integer(string=u'原価金額', store=True, readonly=True, compute='_cost_all', track_visibility='always')
    #
    # #
    # pj_note = fields.Text(u'備考')

    # 経理年月
    pj_account_date = fields.Char(
        u'経理年月', compute='_compute_pj_account_date', store=True)
    # pj_account_date = fields.Char(u'経理年月')
    pj_long_date = fields.Date(u'経理年月', required=True)
    #

    # PJ処理状態
    pj_process = fields.Selection([
        ('new', u'処理待ち'),
        ('proc', u'処理中'),
        ('done', u'処理済'),
    ], string='処理状態', copy=False, index=True, track_visibility='onchange', default='new', required=True)

    # pj_account_dateの生成

    @api.depends('pj_long_date')
    def _compute_pj_account_date(self):
        for record in self:
            if record.pj_long_date:
                # 月末を計算する　(閏年も含めて)
                stringDate = datetime.strptime(record.pj_long_date, '%Y-%m-%d')
                year = int(stringDate.strftime('%Y'))
                month = int(stringDate.strftime('%m'))
                last_day = str(monthrange(year, month)[1])

                record.pj_account_date = stringDate.strftime('%Y%m')
                record.pj_long_date = stringDate.strftime('%Y-%m-' + last_day)

    #  フォーム合計の計算
    @api.depends('pj_order_line.pj_amount_subtotal')
    def _amount_total(self):
        for pj in self:
            amount = 0.0
            for line in pj.pj_order_line:
                amount += line.pj_amount_subtotal
            pj.pj_amount_total = amount
            # pj.update({
            #     'pj_amount_total': amount,
            # })

    # @api.onchange('pj')
    # def _onchange_pj(self):
    #     self._set_pj_values(self)
    #
    # @api.multi
    # def _set_pj_values(self, vals):
    #     for o_pj in vals:
    #         o_pj.pj_partner_id = o_pj.pj.pj_partner_id
    #         o_pj.pj_bu_cd = o_pj.pj.pj_bu_cd
    #
    # @api.multi
    # def action_apply(self):
    #     self.ensure_one()

class SsPjOrderLine(models.Model):
    _name = "ss.pj.order.line"
    _description = 'SS_PJ_OrderLine'
    _order = 'sequence'
    _inherit = "ss.pj.line"

    pj_order_id = fields.Many2one('ss.pj.order', string='PJ Order Reference',
                                  required=True, ondelete='cascade', index=True, copy=False)

    # sequence = fields.Integer(string='Sequence', default=10)

    # pj_id = fields.Char('pj_id', required=True)
    # name = fields.Char(string=u'担当者名', required=True)

    # pj_member_id = fields.Many2one('hr.employee', string=u'要員')
    # pj_member_type = fields.Selection([
    #     ('employee', u'社員'),
    #     ('personal', u'委託'),
    #     ('bp', u'BP'),
    # ], string=u'要員区分')
    # pj_price_type = fields.Selection([
    #     ('month', u'月給'),
    #     ('hour', u'時給'),
    # ], string=u'単価区分', default='month', required=True)
    # pj_price_unit = fields.Integer(u'売上単価')
    # pj_price_purchase = fields.Integer(u'元単価')
    # pj_payofftype = fields.Selection([
    #     ('fix', u'固定'),
    #     ('updown', u'上下割'),
    #     ('middle', u'中間割'),
    # ], string=u'精算条件', default='fix')
    # pj_fraction = fields.Selection([
    #     ('truncation', u'切り捨て'),
    #     ('roundedup', u'切り上げ'),
    # ], string=u'端数計算')
    # pj_is_duty = fields.Boolean(u'精算')
    # pj_duty_lowerlimit = fields.Integer(u'精算下限')
    # pj_duty_upperlimit = fields.Integer(u'精算上限')
    # pj_price_lowerlimit = fields.Integer(
    #     u'下限単価', compute='_compute_pj_price', store=True, readonly=False)
    # pj_price_upperlimit = fields.Integer(
    #     u'上限単価', compute='_compute_pj_price', store=True, readonly=False)
    # pj_manhour_contract = fields.Float(u'標準工数', default=1)
    # pj_amount = fields.Integer(u'売上', compute='_compute_pj_amount', store=True)
    # pj_cost = fields.Integer(u'原価', compute='_compute_pj_cost', store=True)

    pj_manhour = fields.Float(u'当月工数', default=1)
    pj_duty_hours = fields.Float(u'当月時間')
    pj_hours_lowerlimit = fields.Float(
        u'当月下限', compute='_compute_pj_hours', store=True, readonly=False)
    pj_hours_upperlimit = fields.Float(
        u'当月上限', compute='_compute_pj_hours', store=True, readonly=False)
    pj_payoffhour = fields.Float(
        u'精算時間', compute='_compute_pj_payoffhour', store=True)
    pj_excess_deduct = fields.Integer(
        u'超過・控除', compute='_compute_pj_excess_deduct', store=True)
    pj_adjustment = fields.Integer(u'調整額')
    pj_adjustment_comment = fields.Char(u'調整理由')

    # # 小計項目を追加する
    pj_subtotal = fields.Integer(
        u'小計', compute='_compute_pj_subtotal', store=True)
    pj_tax = fields.Integer(u'消費税', compute='_compute_pj_tax', store=True)

    pj_carfare = fields.Integer(u'業務費用')
    pj_amount_subtotal = fields.Integer(
        u'売上合計', compute='_compute_pj_amount_subtotal', store=True)

    # PJを取る
    # pj_cd = fields.Char(related="pj_order_id.pj_cd", string=u"PJコード")
    # pj_name = fields.Char(related="pj_order_id.pj_name", string=u"PJ名称")
    # pj_account_date = fields.Char(related="pj_id.pj_account_date", string=u"経理年月")

    #------------------------------------------------------------------
    # 精算条件 pj_payofftype （fix:固定 / updown:上下割 / middle:中間割）
    #------------------------------------------------------------------
    # 1.精算条件=fix:固定　
    #   売上単価(pj_price_unit)
    # 2.精算条件=updown:上下割　

    #   当月下限(pj_hours_lowerlimit)
    #   当月上限(pj_hours_upperlimit)
    #
    # 3.精算条件=middle:中間割　
    # 4.時給 / 月給　
    #------------------------------------------------------------------

    # 計算項目

    # 当月下限 pj_hours_lowerlimit 当月上限 pj_hours_upperlimit
    @api.depends('pj_duty_lowerlimit', 'pj_duty_upperlimit', 'pj_manhour', 'pj_payofftype')
    def _compute_pj_hours(self):
        for record in self:
            if record.pj_price_type == 'month':
                if record.pj_payofftype != 'fix':
                    record.pj_hours_lowerlimit = round(record.pj_duty_lowerlimit * record.pj_manhour)
                    record.pj_hours_upperlimit = round(record.pj_duty_upperlimit * record.pj_manhour)

    # 精算時間 pj_payoffhour
    @api.depends('pj_duty_lowerlimit', 'pj_duty_upperlimit', 'pj_duty_hours', 'pj_manhour', 'pj_hours_lowerlimit', 'pj_hours_upperlimit')
    def _compute_pj_payoffhour(self):
        for record in self:
            if record.pj_duty_hours and (record.pj_duty_hours < record.pj_hours_lowerlimit):
                record.pj_payoffhour = record.pj_duty_hours - record.pj_hours_lowerlimit
            elif record.pj_duty_hours and (record.pj_duty_hours > record.pj_hours_upperlimit):
                record.pj_payoffhour = record.pj_duty_hours - record.pj_hours_upperlimit

    # 超過・控除 pj_excess_deduct
    # 時給超過分　単価ｘ1.25
    @api.depends('pj_price_lowerlimit', 'pj_price_upperlimit', 'pj_duty_hours', 'pj_payoffhour')
    def _compute_pj_excess_deduct(self):
        for record in self:
            if record.pj_payoffhour and record.pj_payoffhour <= 0:
                record.pj_excess_deduct = round(record.pj_price_lowerlimit * record.pj_payoffhour)
            elif record.pj_payoffhour and record.pj_payoffhour > 0:
                if record.pj_price_type == 'month':
                    record.pj_excess_deduct = round(record.pj_price_upperlimit * record.pj_payoffhour)
                elif record.pj_price_type == 'hour':
                    record.pj_excess_deduct = math.floor(round(record.pj_price_unit * record.pj_payoffhour) * record.pj_normal_hourlywage)
            if record.pj_amount and record.pj_excess_deduct:
                record.pj_subtotal = record.pj_amount + record.pj_excess_deduct

    # 売上 pj_amount
    @api.depends('pj_price_unit', 'pj_manhour', 'pj_hours_lowerlimit')
    def _compute_pj_amount(self):
        for record in self:
            if record.pj_price_type == 'month':
                record.pj_amount = round(record.pj_price_unit * record.pj_manhour)
                if record.pj_amount and record.pj_excess_deduct:
                    record.pj_subtotal = record.pj_amount + record.pj_excess_deduct
            elif record.pj_price_type == 'hour':
                record.pj_amount = round(record.pj_price_unit * record.pj_hours_lowerlimit)
                if record.pj_amount and record.pj_excess_deduct:
                    record.pj_subtotal = record.pj_amount + record.pj_excess_deduct

    # 小計 pj_subtotal
    @api.depends('pj_amount', 'pj_excess_deduct', 'pj_adjustment')
    def _compute_pj_subtotal(self):
        for record in self:
            record.pj_subtotal = record.pj_amount + record.pj_excess_deduct + record.pj_adjustment

    # 消費税 pj_tax
    # 消費税計算　消費税率取得
    @api.depends('pj_amount', 'pj_excess_deduct', 'pj_adjustment')
    def _compute_pj_tax(self):
        for record in self:
            record.pj_tax = round((record.pj_amount + record.pj_excess_deduct + record.pj_adjustment) * 0.08)

    # 売上合計 pj_amount_subtotal 小計+ 消費税 + 業務費用
    @api.depends('pj_subtotal', 'pj_carfare', 'pj_adjustment')
    def _compute_pj_amount_subtotal(self):
        for record in self:
            record.pj_amount_subtotal = record.pj_subtotal + record.pj_tax + record.pj_carfare
