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

class SsPj(models.Model):
    _name = "ss.pj"
    _description = "PJ"
    _rec_name = 'pj_cd'
    _order = 'pj_register_date desc'

    @api.model
    def create_pj_cd(self):
       for pj in self:
          self.name = self.env['ir.sequence'].next_by_code('ss.pj') or _('New')

    # PJIDと名前
    pj_cd = fields.Char(u'PJコード', size=12, store=True, readonly=False)
    pj_name = fields.Char(u'PJ名', required=True)

    # PJ種別
    pj_type = fields.Selection([
        ('dispatch', u'派遣'),
        ('contract', u'請負'),
        ('subcontracting', u'業務委託'),
        ('quasidelegation', u'準委任'),
        ('delegation', u'委任'),
        ('maintaining', u'保守'),
        ('totalcontract', u'一括請負'),
        ('other', u'その他'),
    ], string=u'種別', required=True)

    # PJ担当者
    pj_user_id = fields.Many2one('res.users', string='PJ担当者')

    # 申請登録
    pj_register_date = fields.Date(u'登録年月日')
    pj_register_user_id = fields.Many2one('res.users', string='登録担当者')

    # 許可
    pj_permitted_date = fields.Date(u'許可年月日')
    pj_permitted_user_id = fields.Many2one('res.users', string='許可担当者')

    # 終了
    pj_closed_date = fields.Date(u'終了年月日')
    pj_closed_user_id = fields.Many2one('res.users', string='終了担当者')

    # BU
    pj_bu_cd = fields.Many2one('hr.department', u'BUコード', required=True)
    pj_bu_name = fields.Char(u'BU名', related='pj_bu_cd.name', readonly=True)

    # 顧客コード
    pj_partner_id = fields.Many2one('res.partner', string='顧客', domain=[('customer', '=', True)], required=True)
    pj_partner_cd = fields.Char(u'顧客コード', related='pj_partner_id.x_partner_cd', readonly=True, store=True)

    # PJ管理
    pj_state = fields.Selection([
        ('new', u'新規'),
        ('run', u'稼働中'),
        ('cancel', u'終止'),
        ('end', u'終了'),
    ], string='稼働状態', copy=False, index=True, track_visibility='onchange', default='new', required=True)

    #PJ日付
    pj_startdate = fields.Date(u'PJ開始日', default=fields.Date.context_today, required=True)
    pj_enddate = fields.Date(u'PJ予定終了日')
    pj_total_months = fields.Date(u'PJ実施月数')

    #PJ検収状態
    pj_receipted_date = fields.Date(u'検収年月日')
    pj_receipted_user_id = fields.Many2one('res.users', string='検収担当者')

    #PJ要員詳細
    pj_line = fields.One2many('ss.pj.line', 'pj_id', string='PJ Lines')

    #PJ合計金額
    pj_amount_total = fields.Integer(string=u'合計金額', store=True, readonly=True, compute='_amount_all', track_visibility='always')

    #PJ原価金額
    pj_cost_total = fields.Integer(string=u'原価金額', store=True, readonly=True, compute='_cost_all', track_visibility='always')

    #
    pj_note = fields.Text(u'備考')

    # PJ_CDを生成する
    #     for record in self:
    #         if record.pj_bu_cd.x_department_cd and record.partner_id.x_partner_cd:
    #             record.pj_cd = record.pj_bu_cd.x_department_cd + record.partner_id.x_partner_cd + record.name

    #  フォーム合計の計算
    @api.depends('pj_line.pj_amount')
    def _amount_all(self):
        for pj in self:
            amount_untaxed = amount_tax = 0.0
            for line in pj.pj_line:
                amount_untaxed += line.pj_amount
            pj.update({
                'pj_amount_total': amount_untaxed + amount_tax,
            })

    #  フォーム原価合計の計算
    @api.depends('pj_line.pj_cost')
    def _cost_all(self):
        for pj in self:
            cost_total = 0.0
            for line in pj.pj_line:
                cost_total += line.pj_cost
            pj.update({
                'pj_cost_total': cost_total,
            })

class SsPjLine(models.Model):
    _name = "ss.pj.line"
    _description = 'SS PJ Line'
    _order = 'sequence'

    # pj_cd = fields.Char('pj_cd', required=True)
    # name = fields.Char(string=u'担当者名', required=True)

    pj_id = fields.Many2one('ss.pj', string='PJ Reference', required=True, ondelete='cascade', index=True, copy=False)

    sequence = fields.Integer(string='Sequence', default=10)

    pj_member_id = fields.Many2one('hr.employee', string=u'要員')
    pj_member_type = fields.Selection([
        ('employee', u'社員'),
        ('personal', u'委託'),
        ('bp', u'BP'),
    ], string=u'要員区分')
    pj_price_type = fields.Selection([
        ('month', u'月給'),
        ('hour', u'時給'),
    ], string=u'単価区分', default='month', required=True)
    pj_price_unit = fields.Integer(u'売上単価')
    pj_price_purchase = fields.Integer(u'元単価')
    pj_payofftype = fields.Selection([
        ('fix', u'固定'),
        ('updown', u'上下割'),
        ('middle', u'中間割'),
    ], string=u'精算条件', default='fix')
    pj_fraction = fields.Selection([
        ('truncation', u'切り捨て'),
        ('roundedup', u'切り上げ'),
    ], string=u'端数計算')
    pj_is_duty = fields.Boolean(u'精算')
    pj_duty_lowerlimit = fields.Integer(u'精算下限')
    pj_duty_upperlimit = fields.Integer(u'精算上限')
    pj_price_lowerlimit = fields.Integer(u'下限単価', compute='_compute_pj_price', store=True, readonly=False)
    pj_price_upperlimit = fields.Integer(u'上限単価', compute='_compute_pj_price', store=True, readonly=False)
    pj_manhour_contract = fields.Float(u'標準工数', default=1)
    pj_amount = fields.Integer(u'売上', compute='_compute_pj_amount', store=True)
    pj_cost = fields.Integer(u'原価', compute='_compute_pj_cost', store=True)

    # PJを取る
    pj_cd = fields.Char(related="pj_id.pj_cd", string=u"PJコード")
    pj_name = fields.Char(related="pj_id.pj_name", string=u"PJ名称")

    #------------------------------------------------------------------
    # 精算条件 pj_payofftype （fix:固定 / updown:上下割 / middle:中間割）
    #------------------------------------------------------------------
    # 1.精算条件=fix:固定　
    #   売上単価(pj_price_unit)

    # 2.精算条件=updown:上下割　
    #   下限単価(pj_price_lowerlimit) = 売上単価(pj_price_unit) / 精算下限(pj_duty_lowerlimit)
    #   上限単価(pj_price_upperlimit) = 売上単価(pj_price_unit) / 精算上限(pj_duty_upperlimit)
    #
    # 3.精算条件=middle:中間割　
    #
    #------------------------------------------------------------------
    #

    # 計算項目

    # 単価計算: 下限単価(pj_price_lowerlimit) 上限単価(pj_price_upperlimit)
    @api.depends('pj_price_unit', 'pj_duty_lowerlimit', 'pj_duty_upperlimit', 'pj_payofftype')
    def _compute_pj_price(self):
        for record in self:
            if record.pj_payofftype == 'updown':
                if record.pj_price_unit and record.pj_duty_lowerlimit:
                    record.pj_price_lowerlimit = round(record.pj_price_unit / record.pj_duty_lowerlimit)
                if record.pj_price_unit and record.pj_duty_upperlimit:
                    record.pj_price_upperlimit = round(record.pj_price_unit / record.pj_duty_upperlimit)
            elif record.pj_payofftype == 'middle':
                if record.pj_price_unit and record.pj_duty_lowerlimit and record.pj_duty_upperlimit:
                    record.pj_price_lowerlimit = round(record.pj_price_unit / ((record.pj_duty_lowerlimit + record.pj_duty_upperlimit) / 2))
                    record.pj_price_upperlimit = record.pj_price_lowerlimit

    # 当月下限 pj_hours_lowerlimit 当月上限 pj_hours_upperlimit
    @api.depends('pj_duty_lowerlimit', 'pj_duty_upperlimit', 'pj_manhour_contract', 'pj_payofftype')
    def _compute_pj_hours(self):
        for record in self:
            if record.pj_payofftype != 'fix':
                record.pj_hours_lowerlimit = round(record.pj_duty_lowerlimit * record.pj_manhour_contract)
                record.pj_hours_upperlimit = round(record.pj_duty_upperlimit * record.pj_manhour_contract)

    # 売上 pj_amount
    @api.depends('pj_price_unit', 'pj_manhour_contract')
    def _compute_pj_amount(self):
        for record in self:
            record.pj_amount = record.pj_price_unit * record.pj_manhour_contract

    # 原価 pj_cost
    @api.depends('pj_price_purchase', 'pj_manhour_contract')
    def _compute_pj_cost(self):
        for record in self:
            record.pj_cost = record.pj_price_purchase * record.pj_manhour_contract

