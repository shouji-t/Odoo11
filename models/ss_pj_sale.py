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

class SsPjOrder(models.Model):
    _inherit = "sale.order"

    pj = fields.Many2one('ss.pj', u'pj')

    # PJ情報
    pj_cd = fields.Char(related="pj.pj_cd", string=u"PJコード", readonly=True, store=True)
    pj_name = fields.Char(related="pj.pj_name", string=u"PJ名称", readonly=True, store=True)
    pj_type = fields.Selection(related="pj.pj_type", string=u"PJ種別", readonly=True, store=True)
    pj_bu_cd = fields.Many2one(related="pj.pj_bu_cd", string=u"BUコード", readonly=True, store=True)
    pj_bu_name = fields.Char(related="pj.pj_bu_name", string=u"BU名", readonly=True, store=True)
    pj_partner_cd = fields.Char(related="pj.pj_partner_cd", string=u"顧客コード", readonly=True, store=True)
    pj_state = fields.Selection(related="pj.pj_state", string=u"PJ状態", readonly=True, store=True)
    pj_partner_id = fields.Many2one(related="pj.pj_partner_id", string=u"顧客", readonly=True, store=True)
    # partner_id = fields.Many2one(related="pj.pj_partner_id", string=u"顧客", readonly=True, store=True)

    # 経理年月
    pj_account_date = fields.Char(u'経理年月', compute='_compute_pj_account_date', store=True)
    pj_long_date = fields.Date(u'経理年月', required=True)

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
        ('personal', u'委託'),
        ('bp', u'BP'),
    ], string=u'要員区分')
    pj_price_unit = fields.Monetary(u'売上単価')
    pj_price_purchase = fields.Monetary(u'元単価')
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
    pj_manhour = fields.Float(u'当月工数', default=1)
    pj_duty_hours = fields.Float(u'当月時間')
    pj_hours_lowerlimit = fields.Integer(u'当月下限', compute='_compute_pj_hours', store=True, readonly=False)
    pj_hours_upperlimit = fields.Integer(u'当月上限', compute='_compute_pj_hours', store=True, readonly=False)
    pj_payoffhour = fields.Float(u'精算時間', compute='_compute_pj_payoffhour', store=True)
    pj_amount = fields.Monetary(u'売上', compute='_compute_pj_amount', store=True)
    pj_excess_deduct = fields.Monetary(u'超過・控除', compute='_compute_pj_excess_deduct', store=True)
    pj_adjustment = fields.Monetary(u'調整額')

    # 小計項目を追加する
    pj_subtotal = fields.Monetary(u'小計', compute='_compute_pj_subtotal', store=True)
    pj_tax = fields.Monetary(u'消費税')

    pj_carfare = fields.Monetary(u'業務費用')
    pj_amount_subtotal = fields.Monetary(u'売上合計', compute='_compute_pj_amount_subtotal', store=True)

    # PJを取る
    pj_cd = fields.Char(related="order_id.pj_cd", string=u"PJコード")
    pj_name = fields.Char(related="order_id.pj_name", string=u"PJ名称")
    pj_account_date = fields.Char(related="order_id.pj_account_date", string=u"経理年月")

    # プロダクトをデフォルトにする
    # product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)],
    #                              change_default=True, ondelete='restrict', required=True,
    #                              default=lambda self: self.env['product.template'].search(
    #                                  [('name', '=', 'product_ssm')]).id)

    product_id = fields.Many2one('product.product', string='Product',
                                 default=lambda self: self.env['product.template'].search(
                                     [('name', '=', 'Default')]).id)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True, default='')


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
    #
    #------------------------------------------------------------------
    #

    # 計算項目

    # 当月下限 pj_hours_lowerlimit 当月上限 pj_hours_upperlimit
    @api.depends('pj_duty_lowerlimit', 'pj_duty_upperlimit', 'pj_manhour', 'pj_payofftype')
    def _compute_pj_hours(self):
        for record in self:
            if record.pj_payofftype != 'fix':
                record.pj_hours_lowerlimit = round(record.pj_duty_lowerlimit * record.pj_manhour)
                record.pj_hours_upperlimit = round(record.pj_duty_upperlimit * record.pj_manhour)

    # 精算時間 pj_payoffhour
    @api.depends('pj_duty_lowerlimit', 'pj_duty_upperlimit', 'pj_duty_hours')
    def _compute_pj_payoffhour(self):
        for record in self:
            if record.pj_duty_hours and (record.pj_duty_hours < record.pj_duty_lowerlimit):
                record.pj_payoffhour = record.pj_duty_hours - record.pj_duty_lowerlimit
            elif record.pj_duty_hours and (record.pj_duty_hours > record.pj_duty_upperlimit):
                record.pj_payoffhour = record.pj_duty_hours - record.pj_duty_upperlimit

    # 売上 pj_amount
    @api.depends('pj_price_unit', 'pj_manhour')
    def _compute_pj_amount(self):
        for record in self:
            record.pj_amount = record.pj_price_unit * record.pj_manhour
            if record.pj_amount and record.pj_excess_deduct:
                record.pj_subtotal = record.pj_amount + record.pj_excess_deduct

    # 超過・控除 pj_excess_deduct
    @api.depends('pj_price_lowerlimit', 'pj_price_upperlimit', 'pj_duty_hours', 'pj_payoffhour')
    def _compute_pj_excess_deduct(self):
        for record in self:
            if record.pj_payoffhour and record.pj_payoffhour <= 0:
                record.pj_excess_deduct = record.pj_price_lowerlimit * record.pj_payoffhour
                if record.pj_amount and record.pj_excess_deduct:
                    record.pj_subtotal = record.pj_amount + record.pj_excess_deduct
            elif record.pj_payoffhour and record.pj_payoffhour > 0:
                record.pj_excess_deduct = record.pj_price_upperlimit * record.pj_payoffhour
                record.pj_subtotal = record.pj_amount + record.pj_excess_deduct

    # 小計 pj_subtotal
    @api.depends('pj_amount', 'pj_excess_deduct')
    def _compute_pj_subtotal(self):
        for record in self:
            record.pj_subtotal = record.pj_amount + record.pj_excess_deduct

    # 売上合計 pj_amount_subtotal 小計+交通費
    @api.depends('pj_subtotal', 'pj_carfare', 'pj_adjustment')
    def _compute_pj_amount_subtotal(self):
        for record in self:
            record.pj_amount_subtotal = record.pj_subtotal + record.pj_carfare + record.pj_adjustment


