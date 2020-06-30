# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import api, fields, models
# from odoo import api, fields, models, _
# from calendar import monthrange
# from datetime import datetime
# import math

class SsPj(models.Model):
    _name = "ss.pj"
    _description = "PJ"
    _rec_name = 'pj_cd'
    _inherit = ['mail.thread']
    _order = 'pj_register_date desc'

    # PJIDと名前
    pj_cd = fields.Char(u'PJコード', default='NEW', index=True, size=12, store=True, copy=False, readonly=False,
                        track_visibility='always')
    pj_name = fields.Char(u'PJ名', required=True)
    active = fields.Boolean('Active', default=True, store=True)

    pj_orders = fields.One2many('ss.order', 'pj_id', string='PJ要員')

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
    pj_user_name = fields.Char(u'PJ担当者名', related='pj_user_id.name', readonly=True, store=True)

    # 申請登録
    pj_register_date = fields.Date(u'登録年月日', default=fields.Date.context_today)
    pj_register_user_id = fields.Many2one('res.users', string='登録担当者', default=lambda self: self.env.user)

    # 許可
    # pj_permitted_date = fields.Date(u'許可年月日')
    # pj_permitted_user_id = fields.Many2one('res.users', string='許可担当者')

    # 終了
    pj_closed_date = fields.Date(u'終了年月日')
    pj_closed_user_id = fields.Many2one('res.users', string='終了担当者')

    # BU
    pj_bu_id = fields.Many2one('hr.department', u'BU', required=True)
    pj_bu_cd = fields.Char(u'部門コード', related='pj_bu_id.x_department_cd', readonly=True, store=True)
    pj_bu_name = fields.Char(u'部門名', related='pj_bu_id.name', readonly=True, store=True)

    # 顧客コード
    pj_partner_id = fields.Many2one('res.partner', string='顧客', domain=[
                                    ('customer', '=', True)], required=True, track_visibility='always')
    pj_partner_cd = fields.Char(
        u'顧客コード', related='pj_partner_id.x_partner_cd', readonly=True, store=True)

    # PJ管理
    pj_state = fields.Selection([
        ('new', u'新規'),
        ('run', u'稼働中'),
        ('cancel', u'終止'),
        ('end', u'終了'),
    ], string='稼働状態', copy=False, index=True, default='new', required=True)

    # PJ日付
    pj_startdate = fields.Date(u'PJ開始日', default=fields.Date.context_today, required=True)
    pj_enddate = fields.Date(u'PJ予定終了日')
    pj_total_months = fields.Date(u'PJ実施月数')

    # PJ検収状態
    # pj_receipted_date = fields.Date(u'検収年月日')
    # pj_receipted_user_id = fields.Many2one('res.users', string='検収担当者')

    # PJ金額
    pj_amount_total = fields.Integer(u'合計金額', readonly=True)
    pj_cost_total = fields.Integer(u'原価金額', readonly=True)
    pj_profit = fields.Integer(u'粗利', readonly=True)
    pj_profitrate = fields.Float(u'粗利率', readonly=True)

    pj_note = fields.Text(u'変更履歴', track_visibility='onchange')
    pj_remarks = fields.Text(u'備考', track_visibility='onchange')

    # PJ連番
    pj_serial = fields.Char(u'PJ連番', compute='_compute_pj_serial_no', store=True)

    # CompanyId
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.user.company_id.id)

    # 変更履歴、備考のradio button
    pj_note_flag = fields.Boolean(u'変更履歴', default=False, onchange='_onchange_pj_note')
    pj_remarks_flag = fields.Boolean(u'備考', default=False, onchange='_onchange_pj_remarks')

    # PJ_CDを生成する
    @api.multi
    def action_SetNewPJNo(self):
        for record in self:
            if record.pj_bu_cd and record.pj_partner_cd:
                number = self.env['ir.sequence'].next_by_code('ss.pj') or _('New')
                record.pj_cd = record.pj_bu_cd + record.pj_partner_cd + str(number).zfill(4)

    # PJ要員詳細
    # pj_line = fields.One2many('ss.pj.line', 'pj_id', string='PJ Lines')


    # PJ合計金額
    pj_amount_total = fields.Integer(
        string=u'合計金額', store=True, readonly=True, compute='_amount_all')

    # PJ原価金額
    pj_cost_total = fields.Integer(
        string=u'原価金額', store=True, readonly=True, compute='_cost_all')

    # PJ粗利
    pj_profit = fields.Integer(
        string=u'粗利', store=True, readonly=True, compute='_profit_all')

    # PJ粗利率
    pj_profitrate = fields.Float(
        string=u'粗利率', store=True, readonly=True, compute='_profitrate_all')


    #  フォーム合計の計算
    @api.depends('pj_orders.pj_o_amount')
    def _amount_all(self):
        for pj in self:
            amount_untaxed = amount_tax = 0.0
            for line in pj.pj_orders:
                amount_untaxed += line.pj_o_amount
            pj.update({
                'pj_amount_total': amount_untaxed + amount_tax,
            })

    #  フォーム原価合計の計算
    @api.depends('pj_orders.pj_o_cost')
    def _cost_all(self):
        for pj in self:
            cost_total = 0.0
            for line in pj.pj_orders:
                cost_total += line.pj_o_cost
            pj.update({
                'pj_cost_total': cost_total,
            })

    #  粗利の計算
    @api.depends('pj_amount_total', 'pj_cost_total')
    def _profit_all(self):
        for pj in self:
            if pj.pj_amount_total and pj.pj_cost_total:
                pj.pj_profit = pj.pj_amount_total - pj.pj_cost_total

    #  粗利率の計算
    @api.depends('pj_amount_total', 'pj_cost_total')
    def _profitrate_all(self):
        for pj in self:
            if pj.pj_amount_total and pj.pj_cost_total:
                pj.pj_profitrate = (pj.pj_amount_total - pj.pj_cost_total) / pj.pj_amount_total

    # PJ連番
    @api.depends('pj_cd')
    def _compute_pj_serial_no(self):
        for record in self:
            if record.pj_cd:
                record.pj_serial = record.pj_cd[-4:]

    # 変更履歴、備考のradio button
    @api.onchange('pj_note')
    def _onchange_pj_note(self):
        for record in self:
            if record.pj_note:
                record.pj_note_flag = True
            else:
                record.pj_note_flag = False

    @api.onchange('pj_remarks')
    def _onchange_pj_remarks(self):
        for record in self:
            if record.pj_remarks:
                record.pj_remarks_flag = True
            else:
                record.pj_remarks_flag = False

