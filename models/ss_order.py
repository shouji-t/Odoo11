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

class SsOrder(models.Model):
    _name = "ss.order"
    _description = 'SS Order'
    _rec_name = 'pj_member_id'
    _inherit = ['mail.thread']
    _order = 'pj_member_cd'

    pj_sales_ids = fields.One2many('ss.sales', 'id', string='PJ Sales')

    # PJ要員管理
    active = fields.Boolean('Active', default=True, store=True, index=True)

    # 要員
    pj_member_id = fields.Many2one('hr.employee', string=u'要員', required=True, index=True, track_visibility='always')
    pj_member_cd = fields.Char(string='従業員コード', store=True, related='pj_member_id.x_employee_cd', index=True)
    pj_member_type = fields.Selection(u'要員区分', related='pj_member_id.x_member_type', readonly=True, store=True)
    pj_member_note = fields.Text(u'変更履歴', track_visibility='onchange')
    pj_member_remarks = fields.Text(u'備考', track_visibility='onchange')

    # PJIDと名前
    pj_id = fields.Many2one('ss.pj', string='PJ', required=True)
    pj_cd = fields.Char(u'PJコード', related='pj_id.pj_cd', store=True, readonly=True, index=True)
    pj_name = fields.Char(u'PJ名', related='pj_id.pj_name', store=True, readonly=True, index=True)

    # PJ担当者
    pj_user_id = fields.Many2one('res.users', related='pj_id.pj_user_id', store=True, readonly=True)

    # BU
    pj_bu_id = fields.Many2one('hr.department', u'部門', related='pj_id.pj_bu_id', store=True, readonly=True, index=True)
    pj_bu_cd = fields.Char(u'部門コード', related='pj_id.pj_bu_cd', readonly=True, store=True, index=True)
    pj_bu_name = fields.Char(u'部門名', related='pj_id.pj_bu_name', readonly=True, store=True)

    pj_partner_c_id = fields.Many2one('res.partner', u'顧客', related='pj_id.pj_partner_id', readonly= True, store=True)
    pj_partner_c_cd = fields.Char('顧客コード', related='pj_id.pj_partner_cd', readonly= True, store=True, index=True)
    pj_partner_s_id = fields.Many2one('res.partner', u'仕入先', related='pj_member_id.x_partner_id', readonly= True, store=True)
    pj_partner_s_cd = fields.Char('仕入先コード', related='pj_member_id.x_partner_cd', readonly= True, store=True, index=True )

    # ------------------------------------------------------------------
    # 受注情報　顧客　
    # ------------------------------------------------------------------
    pj_o_member_orderno = fields.Char(u'受注_書類番号')
    pj_o_member_orderdatefrom = fields.Date(u'受注_期間FROM', track_visibility='onchange')
    pj_o_member_orderdateto = fields.Date(u'受注_期間TO(確定)', track_visibility='onchange')
    pj_o_member_orderdateto_forecase = fields.Date(u'受注_期間TO(見込)')
    pj_o_member_orderamount = fields.Integer(u'受注_金額')
    pj_o_member_orderisprogress = fields.Boolean(u'受注_仕掛品', Default=False)
    pj_o_member_orderdateaccpt = fields.Date(u'受注_検収日')

    pj_o_price_type = fields.Selection([
        ('month', u'月給'),
        ('hour',  u'時給'),
        ('day',   u'日給'),
    ], string=u'単価区分', default='month', required=True)
    pj_o_price_unit = fields.Integer(u'売価')
    pj_o_price_purchase = fields.Integer(u'原価', related='pj_member_id.x_cost', store=True)
    pj_o_payofftype = fields.Selection([
        ('fix', u'固定'),
        ('updown', u'上下割'),
        ('middle', u'中間割'),
    ], string=u'精算条件', default='fix')
    pj_o_normal_dutyhours = fields.Integer(u'標準時数日数', default=150)
    pj_o_normal_hourlywage = fields.Float(u'時間割増率', default=1.00)
    pj_o_is_duty = fields.Boolean(u'精算')
    pj_o_duty_lowerlimit = fields.Integer(u'精算下限')
    pj_o_duty_upperlimit = fields.Integer(u'精算上限')
    pj_o_price_lowerlimit = fields.Integer(u'下限単価', onchange='_onchange_pj_o_price_ref')
    pj_o_price_upperlimit = fields.Integer(u'上限単価', onchange='_onchange_pj_o_price_ref')
    # pj_o_price_lowerlimit_ref = fields.Integer(u'下限単価(参考)', compute='_compute_pj_o_price_ref')
    # pj_o_price_upperlimit_ref = fields.Integer(u'上限単価(参考)', compute='_compute_pj_o_price_ref')
    pj_o_manhour_contract = fields.Float(u'標準工数', default=1)
    pj_o_amount = fields.Integer(u'売上', compute='_compute_pj_o_amount', store=True)
    pj_o_cost = fields.Integer(u'原価', compute='_compute_pj_o_cost', store=True)

    # PJ粗利 粗利率
    pj_o_profit = fields.Integer(string=u'粗利', store=True, readonly=True, compute='_compute_pj_o_profit')
    pj_o_profitrate = fields.Float(string=u'粗利率', store=True, readonly=True, compute='_compute_pj_o_profitrate')

    # ------------------------------------------------------------------
    # 発注情報　外注　
    # ------------------------------------------------------------------
    pj_p_member_orderno = fields.Char(u'z発注_書類番号')
    pj_p_member_orderdatefrom = fields.Date(u'z発注_期間FROM')
    pj_p_member_orderdateto = fields.Date(u'z発注_期間TO(確定)')
    pj_p_member_orderdateto_forecase = fields.Date(u'z発注_期間TO(見込)')
    pj_p_member_orderamount = fields.Integer(u'z発注_金額')
    pj_p_member_orderisprogress = fields.Boolean(u'z発注_仕掛品', Default=False)
    pj_p_member_orderdateaccpt = fields.Date(u'z発注_検収日')

    pj_p_price_type = fields.Selection([
        ('month', u'月給'),
        ('hour',  u'時給'),
        ('day',   u'日給'),
    ], string=u'z単価区分', default='month', required=True)
    # pj_p_price_unit = fields.Integer(u'z売価')
    pj_p_price_unit = fields.Integer(u'z原価')
    pj_p_price_purchase = fields.Integer(u'z原価0')
    pj_p_payofftype = fields.Selection([
        ('fix', u'固定'),
        ('updown', u'上下割'),
        ('middle', u'中間割'),
    ], string=u'z精算条件', default='fix')
    pj_p_normal_dutyhours = fields.Integer(u'z標準時数日数', default=150)
    pj_p_normal_hourlywage = fields.Float(u'z時間割増率', default=1.00)
    pj_p_is_duty = fields.Boolean(u'z精算')
    pj_p_duty_lowerlimit = fields.Integer(u'z精算下限')
    pj_p_duty_upperlimit = fields.Integer(u'z精算上限')
    pj_p_price_lowerlimit = fields.Integer(u'z下限単価', onchange='_onchange_pj_p_price_ref')
    pj_p_price_upperlimit = fields.Integer(u'z上限単価', onchange='_onchange_pj_p_price_ref')
    # pj_p_price_lowerlimit_ref = fields.Integer(u'z下限単価(参考)', compute='_compute_pj_p_price_ref')
    # pj_p_price_upperlimit_ref = fields.Integer(u'z上限単価(参考)', compute='_compute_pj_p_price_ref')
    pj_p_manhour_contract = fields.Float(u'z標準工数', default=1)
    pj_p_amount = fields.Integer(u'z発注金額', compute='_compute_pj_p_amount', store=True)
    pj_p_cost = fields.Integer(u'z原価', compute='_compute_pj_p_cost', store=True)

    pj_o_member_orderdateto_forecast = fields.Date(u'要員終了見込み', compute='_compute_pj_o_member_orderdate_')

    # CompanyId
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.user.company_id.id)

    # 変更履歴＆注記、備考のradio button
    pj_member_note_flag = fields.Boolean(u'変更履歴', default=False)
    pj_member_remarks_flag = fields.Boolean(u'備考', default=False)

    # @api.multi
    # def toggle_orderstate(self):
    #     """ Inverse the value of the field ``active`` on the records in ``self``. """
    #     for record in self:
    #         record.pj_orderstate = not record.pj_orderstate

    # ------------------------------------------------------------------
    # 精算条件 pj_payofftype （fix:固定 / updown:上下割 / middle:中間割）
    # ------------------------------------------------------------------
    # 1.精算条件=fix:固定　
    #   売上単価(pj_price_unit)

    # 2.精算条件=updown:上下割　
    #   下限単価(pj_price_lowerlimit) = 売上単価(pj_price_unit) / 精算下限(pj_duty_lowerlimit)
    #   上限単価(pj_price_upperlimit) = 売上単価(pj_price_unit) / 精算上限(pj_duty_upperlimit)
    #
    # 3.精算条件=middle:中間割　
    # 4.時給 / 月給　
    # ------------------------------------------------------------------
    #

    # 計算項目

    # 単価計算(参考): 下限単価(pj_price_lowerlimit) 上限単価(pj_price_upperlimit)
    @api.onchange('pj_o_price_unit', 'pj_o_duty_lowerlimit', 'pj_o_duty_upperlimit', 'pj_o_payofftype', 'pj_o_price_type')
    def _onchange_pj_o_price_ref(self):
        for record in self:
            if record.pj_o_price_type == 'month':
                if record.pj_o_payofftype == 'updown':
                    if record.pj_o_price_unit and record.pj_o_duty_lowerlimit:
                        record.pj_o_price_lowerlimit = math.floor(
                            (record.pj_o_price_unit / record.pj_o_duty_lowerlimit) / 10) *10
                    if record.pj_o_price_unit and record.pj_o_duty_upperlimit:
                        record.pj_o_price_upperlimit = math.floor(
                            (record.pj_o_price_unit / record.pj_o_duty_upperlimit) / 10) *10
                elif record.pj_o_payofftype == 'middle':
                    if record.pj_o_price_unit and record.pj_o_duty_lowerlimit and record.pj_o_duty_upperlimit:
                        record.pj_o_price_lowerlimit = math.floor(
                            (record.pj_o_price_unit / ((record.pj_o_duty_lowerlimit + record.pj_o_duty_upperlimit) / 2)) / 10) *10
                        record.pj_o_price_upperlimit = record.pj_o_price_lowerlimit

    # 売上 pj_o_amount
    @api.depends('pj_o_price_unit', 'pj_o_manhour_contract', 'pj_o_normal_dutyhours', 'pj_o_normal_hourlywage')
    def _compute_pj_o_amount(self):
        for record in self:
            if record.pj_o_price_type == 'month':
                record.pj_o_amount = round(record.pj_o_price_unit * record.pj_o_manhour_contract)
            elif record.pj_o_price_type == 'hour':
                record.pj_o_amount = round(record.pj_o_price_unit * record.pj_o_normal_dutyhours)
            elif record.pj_o_price_type == 'day':
                record.pj_o_amount = round(record.pj_o_price_unit * record.pj_o_normal_dutyhours)

    # 原価 pj_o_cost
    @api.depends('pj_o_price_purchase', 'pj_o_manhour_contract')
    def _compute_pj_o_cost(self):
        for record in self:
            if record.pj_o_price_type == 'month':
                record.pj_o_cost = round(record.pj_o_price_purchase * record.pj_o_manhour_contract)
            elif record.pj_o_price_type == 'hour':
                record.pj_o_cost = round(record.pj_o_price_purchase * record.pj_o_normal_dutyhours)
            elif record.pj_o_price_type == 'day':
                record.pj_o_cost = round(record.pj_o_price_purchase * record.pj_o_normal_dutyhours)

    # 粗利 pj_o_profit
    @api.depends('pj_o_amount', 'pj_o_cost')
    def _compute_pj_o_profit(self):
        for record in self:
            if record.pj_o_amount and record.pj_o_cost:
                record.pj_o_profit = record.pj_o_amount - record.pj_o_cost

    # 粗利率 pj_o_profitrate
    @api.depends('pj_o_amount', 'pj_o_cost')
    def _compute_pj_o_profitrate(self):
        for record in self:
            if record.pj_o_amount and record.pj_o_cost:
                record.pj_o_profitrate = (record.pj_o_amount - record.pj_o_cost) / record.pj_o_amount


    # 売上 pj_p_amount
    @api.depends('pj_p_price_unit', 'pj_p_manhour_contract', 'pj_p_normal_dutyhours', 'pj_p_normal_hourlywage')
    def _compute_pj_p_amount(self):
        for record in self:
            if record.pj_p_price_type == 'month':
                record.pj_p_amount = round(record.pj_p_price_unit * record.pj_p_manhour_contract)
            elif record.pj_p_price_type == 'hour':
                record.pj_p_amount = round(record.pj_p_price_unit * record.pj_p_normal_dutyhours)
            elif record.pj_p_price_type == 'day':
                record.pj_p_amount = round(record.pj_p_price_unit * record.pj_p_normal_dutyhours)

    # # 原価 pj_p_cost
    # @api.depends('pj_p_price_purchase', 'pj_p_manhour_contract')
    # def _compute_pj_p_cost(self):
    #     for record in self:
    #         if record.pj_p_price_type == 'month':
    #             record.pj_p_cost = round(record.pj_p_price_purchase * record.pj_p_manhour_contract)
    #         elif record.pj_p_price_type == 'hour':
    #             record.pj_p_cost = round(record.pj_p_price_purchase * record.pj_p_normal_dutyhours)
    #         elif record.pj_p_price_type == 'day':
    #             record.pj_p_cost = round(record.pj_p_price_purchase * record.pj_p_normal_dutyhours)

    @api.depends('pj_p_price_unit', 'pj_p_manhour_contract')
    def _compute_pj_p_cost(self):
        for record in self:
            if record.pj_p_price_type == 'month':
                record.pj_p_cost = round(record.pj_p_price_unit * record.pj_p_manhour_contract)
            elif record.pj_p_price_type == 'hour':
                record.pj_p_cost = round(record.pj_p_price_unit * record.pj_p_normal_dutyhours)
            elif record.pj_p_price_type == 'day':
                record.pj_p_cost = round(record.pj_p_price_unit * record.pj_p_normal_dutyhours)

    # 単価計算(参考): 下限単価(pj_price_lowerlimit) 上限単価(pj_price_upperlimit)
    @api.onchange('pj_p_price_unit', 'pj_p_duty_lowerlimit', 'pj_p_duty_upperlimit', 'pj_p_payofftype', 'pj_p_price_type')
    def _onchange_pj_p_price_ref(self):
        for record in self:
            if record.pj_p_price_type == 'month':
                if record.pj_p_payofftype == 'updown':
                    if record.pj_p_price_unit and record.pj_p_duty_lowerlimit:
                        record.pj_p_price_lowerlimit = math.floor(
                            (record.pj_p_price_unit / record.pj_p_duty_lowerlimit) / 10) *10
                    if record.pj_p_price_unit and record.pj_p_duty_upperlimit:
                        record.pj_p_price_upperlimit = math.floor(
                            (record.pj_p_price_unit / record.pj_p_duty_upperlimit) / 10) *10
                elif record.pj_p_payofftype == 'middle':
                    if record.pj_p_price_unit and record.pj_p_duty_lowerlimit and record.pj_p_duty_upperlimit:
                        record.pj_p_price_lowerlimit = math.floor(
                            (record.pj_p_price_unit / ((record.pj_p_duty_lowerlimit + record.pj_p_duty_upperlimit) / 2)) / 10) *10
                        record.pj_p_price_upperlimit = record.pj_p_price_lowerlimit

    # 受注条件情報⇒発注情報
    @api.multi
    def action_CopyFromOrder(self):
        for record in self:
            self.update({
                'pj_p_member_orderdatefrom': self.pj_o_member_orderdatefrom,
                'pj_p_member_orderdateto': self.pj_o_member_orderdateto,
                'pj_p_member_orderdateto_forecase': self.pj_o_member_orderdateto_forecase,
                'pj_p_member_orderisprogress': self.pj_o_member_orderisprogress,
                'pj_p_member_orderdateaccpt': self.pj_o_member_orderdateaccpt,
                'pj_p_price_type': self.pj_o_price_type,
                'pj_p_price_unit': self.pj_o_price_purchase,
                'pj_p_price_purchase': self.pj_o_price_purchase,
                'pj_p_normal_dutyhours': self.pj_o_normal_dutyhours,
                'pj_p_normal_hourlywage': self.pj_o_normal_hourlywage,
                'pj_p_is_duty': self.pj_o_is_duty,
                'pj_p_duty_lowerlimit': self.pj_o_duty_lowerlimit,
                'pj_p_duty_upperlimit': self.pj_o_duty_upperlimit,
                'pj_p_manhour_contract': self.pj_o_manhour_contract,
                'pj_p_member_orderisprogress': self.pj_o_member_orderisprogress,
                'pj_p_member_orderdateaccpt': self.pj_o_member_orderdateaccpt,
            })

    # 参考価格⇒下限上限価格(受注)
    @api.multi
    def action_CopyPriceFromRef_o(self):
        for record in self:
            self.update({
                'pj_o_price_lowerlimit': self.pj_o_price_lowerlimit_ref,
                'pj_o_price_upperlimit': self.pj_o_price_upperlimit_ref,
            })

    # 参考価格⇒下限上限価格(外注)
    @api.multi
    def action_CopyPriceFromRef_p(self):
        for record in self:
            self.update({
                'pj_p_price_lowerlimit': self.pj_p_price_lowerlimit_ref,
                'pj_p_price_upperlimit': self.pj_p_price_upperlimit_ref,
            })

    # 要員終了見込み（見込み優先）
    @api.depends('pj_o_member_orderdateto_forecase', 'pj_o_member_orderdateto')
    def _compute_pj_o_member_orderdate_(self):
        for record in self:
            if record.pj_o_member_orderdateto_forecase:
                record.pj_o_member_orderdateto_forecast = record.pj_o_member_orderdateto_forecase
            else:
                record.pj_o_member_orderdateto_forecast = record.pj_o_member_orderdateto

    # 変更履歴、備考のradio button
    @api.onchange('pj_member_note')
    def _onchange_pj_member_note(self):
        for record in self:
            if record.pj_member_note:
                record.pj_member_note_flag = True
            else:
                record.pj_member_note_flag = False

    @api.onchange('pj_member_remarks')
    def _onchange_pj_member_remarks(self):
        for record in self:
            if record.pj_member_remarks:
                record.pj_member_remarks_flag = True
            else:
                record.pj_member_remarks_flag = False

