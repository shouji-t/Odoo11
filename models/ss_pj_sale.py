# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api
from datetime import datetime

class SsPjOrder(models.Model):
    _inherit = "sale.order"

    pj_name = fields.Char(u'PJ名', required=True)
    pj_id = fields.Char(u'PJコード', size=12, compute='_compute_pj_id', store=True)
    pj_account_date = fields.Date(u'経理年月', required=True)

    pj_type = fields.Selection([
        ('contract', u'請負'),
        ('dispatch', u'派遣'),
        ('maintaining', u'保守'),
        ('other', u'その他'),
        ], string=u'種別')

    # BU
    pj_bu_cd = fields.Many2one('hr.department', u'BUコード')
    pj_bu_name = fields.Char(u'BU名', related='pj_bu_cd.name', readonly=True)

    # PJ管理
    pj_state = fields.Selection([
        ('new', u'新規'),
        ('run', u'稼働中'),
        ('cancel', u'終止'),
        ('done', u'終了'),
        ], string='PJ Status', copy=False, index=True, track_visibility='onchange', default='new')
    pj_startdate = fields.Date(u'PJ開始日',default=fields.Date.context_today, required=True)
    pj_enddate = fields.Date(u'PJ予定終了日',default=fields.Date.context_today, required=True)

    @api.model
    def get_last_id(self):
        last_id = self.env['sale.order'].search([], limit=1, order='id desc').id
        return last_id

    # PJ_IDを生成する
    @api.depends('pj_bu_cd', 'partner_id')  
    def _compute_pj_id(self):     
        last_id = self.get_last_id()
        last_id_string = str(last_id + 1).rjust(4,'0')
        for record in self:
            if record.pj_bu_cd.x_department_cd and record.partner_id.x_partner_cd:
                record.pj_id = record.pj_bu_cd.x_department_cd + record.partner_id.x_partner_cd 

     #  フォーム合計の計算
    @api.depends('order_line.pj_amount_subtotal')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.pj_amount_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

class SsPjOrderLine(models.Model):
    _inherit = "sale.order.line"

    # pj_id = fields.Char('pj_id', required=True)
    # name = fields.Char(string=u'担当者名', required=True)

    pj_member_id = fields.Many2one('hr.employee', string=u'要員')
    pj_member_type = fields.Selection([
        ('employee', u'社員'),
        ('bp', u'BP'),
        ('personal', u'個人'),
        ], string=u'要員区分')
    pj_price_unit = fields.Integer(u'売上単価')
    pj_price_purchase = fields.Integer(u'元単価')
    pj_is_duty = fields.Boolean(u'精算')
    pj_duty_lowerlimit = fields.Integer(u'精算下限')
    pj_duty_upperlimit = fields.Integer(u'精算上限')
    pj_price_lowerlimit = fields.Integer(u'下限単価', compute='_compute_pj_price_lowerlimit')
    pj_price_upperlimit = fields.Integer(u'上限単価', compute='_compute_pj_price_upperlimit')
    pj_manhour = fields.Float(u'当月工数')
    pj_duty_hours = fields.Integer(u'当月時間')
    pj_hours_lowerlimit = fields.Integer(u'当月下限')
    pj_hours_upperlimit = fields.Integer(u'当月上限')
    pj_payoffhour = fields.Integer(u'精算時間', compute='_compute_pj_payoffhour')
    pj_amount = fields.Integer(u'売上', compute='_compute_pj_amount')
    pj_excess_deduct = fields.Integer(u'超過・控除', compute='_compute_pj_excess_deduct')

    # 小計項目を追加する
    pj_subtotal = fields.Integer(u'小計', compute='_compute_pj_subtotal')

    pj_carfare = fields.Integer(u'交通費')
    pj_amount_subtotal = fields.Integer(u'売上合計', compute='_compute_pj_amount_subtotal')

     # PJを取る
    pj_id = fields.Char(related="order_id.pj_id", string=u"PJコード", store=True)
    pj_name = fields.Char(related="order_id.pj_name", string=u"PJ名称")
    pj_account_date = fields.Date(related="order_id.pj_account_date", string=u"経理年月")

  
    # 計算項目
    @api.depends('pj_price_unit', 'pj_duty_lowerlimit')
    def _compute_pj_price_lowerlimit(self):
        for record in self:
            if record.pj_duty_lowerlimit:
                record.pj_duty_lowerlimit =  record.pj_price_unit / record.pj_duty_lowerlimit

    @api.depends('pj_price_unit', 'pj_duty_upperlimit')
    def _compute_pj_price_upperlimit(self):
        for record in self:
            if record.pj_duty_lowerlimit:
                record.pj_duty_lowerlimit =  record.pj_price_unit / record.pj_duty_lowerlimit

    @api.depends('pj_duty_lowerlimit', 'pj_duty_upperlimit', 'pj_duty_hours')
    def _compute_pj_payoffhour(self):
        for record in self:
            if record.pj_duty_hours and (record.pj_duty_hours < record.pj_duty_lowerlimit):
                record.pj_payoffhour =  record.pj_duty_hours - record.pj_duty_lowerlimit
            elif record.pj_duty_hours and (record.pj_duty_hours > record.pj_duty_upperlimit):
                record.pj_payoffhour =  record.pj_duty_hours - record.pj_duty_upperlimit

    @api.depends('pj_price_lowerlimit', 'pj_price_upperlimit', 'pj_duty_hours', 'pj_payoffhour')
    def _compute_pj_excess_deduct(self):
        for record in self:
            if record.pj_payoffhour and record.pj_payoffhour < 0:
                record.pj_excess_deduct =  record.pj_price_lowerlimit * record.pj_payoffhour
            elif record.pj_payoffhour and record.pj_payoffhour > 0:
                record.pj_excess_deduct =  record.pj_price_upperlimit * record.pj_payoffhour

    #売上
    @api.depends('pj_price_unit', 'pj_manhour')
    def _compute_pj_amount(self):
        for record in self:      
            record.pj_amount =  record.pj_price_unit * record.pj_manhour

    #小計
    @api.depends('pj_amount','pj_excess_deduct')
    def _compute_pj_subtotal(self):
        for record in self:
            record.pj_subtotal =  record.pj_amount + record.pj_excess_deduct

    #売上合計
    @api.depends('pj_subtotal','pj_carfare')
    def _compute_pj_amount_subtotal(self):
        for record in self:
            record.pj_amount_subtotal =  record.pj_subtotal + record.pj_carfare

            