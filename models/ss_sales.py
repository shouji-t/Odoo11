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
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
import math

class SsSales(models.Model):
    _name = "ss.sales"
    _description = "PJ_SALES"
    _order = 'pj_order_id'
    # _inherit = "ss.order"

    pj_order_id = fields.Many2one('ss.order', u'PJ要員', required=True)

    # 経理年月
    pj_account_date = fields.Char(u'経理年月', compute='_compute_pj_account_date', store=True, index=True)
    pj_long_date = fields.Date(u'経理年月', required=True)

    # PJ処理状態
    pj_process = fields.Selection([
        ('new', u'処理待ち'),
        ('proc', u'処理中'),
        ('done', u'処理済'),
    ], string='処理状態', copy=False, index=True, default='new', required=True)

    # 要員
    pj_member_id = fields.Many2one('hr.employee', string=u'要員', related='pj_order_id.pj_member_id', readonly=True, store=True, index=True)
    pj_member_cd = fields.Char(string='従業員コード', related='pj_order_id.pj_member_cd', readonly=True, store=True, index=True)
    pj_member_type = fields.Selection(u'要員区分', related='pj_order_id.pj_member_type', readonly=True, store=True)
    pj_member_note = fields.Text(u'備考', related='pj_order_id.pj_member_note', readonly=True, store=True)

    # PJIDと名前
    pj_id = fields.Many2one('ss.pj', string='PJ', related='pj_order_id.pj_id', store=True, readonly=True)
    pj_cd = fields.Char(u'PJコード', related='pj_order_id.pj_cd', store=True, readonly=True, index=True)
    pj_name = fields.Char(u'PJ名', related='pj_order_id.pj_name', store=True, readonly=True, index=True)

    # PJ担当者
    pj_user_id = fields.Many2one('res.users', related='pj_order_id.pj_user_id', store=True, readonly=True)

    # BU
    pj_bu_id = fields.Many2one('hr.department', u'BU', related='pj_order_id.pj_bu_id', store=True, readonly=True)
    pj_bu_cd = fields.Char(u'部門コード', related='pj_order_id.pj_bu_cd', readonly=True, store=True, index=True)
    pj_bu_name = fields.Char(u'部門名', related='pj_order_id.pj_bu_name', readonly=True, store=True, index=True)

    pj_partner_c_id = fields.Many2one('res.partner', u'顧客', related='pj_order_id.pj_partner_c_id', readonly= True, store=True)
    pj_partner_c_cd = fields.Char('顧客コード', related='pj_order_id.pj_partner_c_cd', readonly= True, store=True, index=True)
    pj_partner_s_id = fields.Many2one('res.partner', u'仕入先', related='pj_order_id.pj_partner_s_id', readonly= True, store=True)
    pj_partner_s_cd = fields.Char('仕入先コード', related='pj_order_id.pj_partner_s_cd', readonly= True, store=True, index=True )

    # ------------------------------------------------------------------
    # 受注情報　顧客　
    # ------------------------------------------------------------------
    pj_o_member_orderno = fields.Char(u'受注_書類番号')
    pj_o_member_orderdatefrom = fields.Date(u'受注_期間FROM')
    pj_o_member_orderdateto = fields.Date(u'受注_期間TO(確定)')
    pj_o_member_orderdateto_forecase = fields.Date(u'受注_期間TO(見込)')
    pj_o_member_orderamount = fields.Integer(u'受注_金額')
    pj_o_member_orderisprogress = fields.Boolean(u'受注_仕掛品', default=False)
    pj_o_member_orderdateaccpt = fields.Date(u'受注_検収日')

    pj_o_price_type = fields.Selection([
        ('month', u'月給'),
        ('hour',  u'時給'),
        ('day',   u'日給'),
    ], string=u'単価区分', default='month')
    pj_o_price_unit = fields.Integer(u'売価')
    pj_o_price_purchase = fields.Integer(u'原価')
    pj_o_payofftype = fields.Selection([
        ('fix', u'固定'),
        ('updown', u'上下割'),
        ('middle', u'中間割'),
    ], string=u'精算条件', default='fix')
    pj_o_normal_dutyhours = fields.Integer(u'標準時数・日数', default=150)
    pj_o_normal_hourlywage = fields.Float(u'時間割増率', default=1.00)
    pj_o_is_duty = fields.Boolean(u'精算')
    pj_o_duty_lowerlimit = fields.Integer(u'精算下限')
    pj_o_duty_upperlimit = fields.Integer(u'精算上限')
    pj_o_price_lowerlimit = fields.Integer(u'下限単価')
    pj_o_price_upperlimit = fields.Integer(u'上限単価')
    pj_o_manhour_contract = fields.Float(u'標準工数', default=1)
    pj_o_amount = fields.Integer(u'売上', compute='_compute_pj_o_amount', store=True)
    pj_o_cost = fields.Integer(u'原価', compute='_compute_pj_o_cost', store=True)

    # PJ粗利 粗利率
    pj_o_profit = fields.Integer(string=u'粗利', store=True, readonly=True, compute='_compute_pj_o_profit')
    pj_o_profitrate = fields.Float(string=u'粗利率', store=True, readonly=True, compute='_compute_pj_o_profitrate')

    ## Order 受注
    pj_o_manhour = fields.Float(u'当月工数', default=1)
    pj_o_duty_hours = fields.Float(u'当月時間・日数')
    pj_o_hours_lowerlimit = fields.Float(u'当月下限', compute='_compute_pj_o_hours', store=True)
    pj_o_hours_upperlimit = fields.Float(u'当月上限', compute='_compute_pj_o_hours', store=True)
    pj_o_payoffhour = fields.Float(u'精算時間・日数', compute='_compute_pj_o_payoffhour', store=True)
    pj_o_excess_deduct = fields.Integer(u'超過・控除', compute='_compute_pj_o_excess_deduct', store=True)
    pj_o_adjustment = fields.Integer(u'調整額')
    pj_o_adjustment_comment = fields.Char(u'調整理由')

    # # 小計項目を追加する
    pj_o_subtotal = fields.Integer(u'小計', compute='_compute_pj_o_subtotal', store=True)
    pj_o_tax = fields.Integer(u'消費税', compute='_compute_pj_o_tax', store=True)

    pj_o_carfare = fields.Integer(u'業務費用')
    pj_o_amount_subtotal = fields.Integer(u'売上合計', compute='_compute_pj_o_amount_subtotal', store=True)
    pj_o_amount_inprogress = fields.Integer(u'仕掛品金額')

    # ------------------------------------------------------------------
    # 発注情報　外注　
    # ------------------------------------------------------------------
    pj_p_member_orderno = fields.Char(u'z書類番号')
    pj_p_member_orderdatefrom = fields.Date(u'z発注期間FROM')
    pj_p_member_orderdateto = fields.Date(u'z発注期間TO(確定)')
    pj_p_member_orderdateto_forecase = fields.Date(u'z発注期間TO(見込)')
    pj_p_member_orderamount = fields.Integer(u'z発注金額')
    pj_p_member_orderisprogress = fields.Boolean(u'z仕掛品', default=False)
    pj_p_member_orderdateaccpt = fields.Date(u'z検収日')

    pj_p_price_type = fields.Selection([
        ('month', u'月給'),
        ('hour',  u'時給'),
        ('day',   u'日給'),
    ], string=u'z単価区分', default='month')
    pj_p_price_unit = fields.Integer(u'z原価')
    pj_p_price_purchase = fields.Integer(u'z原価0', related='pj_member_id.x_cost', store=True)
    pj_p_payofftype = fields.Selection([
        ('fix',    u'固定'),
        ('updown', u'上下割'),
        ('middle', u'中間割'),
    ], string=u'z精算条件', default='fix')
    pj_p_normal_dutyhours = fields.Integer(u'z標準時数・日数', default=150)
    pj_p_normal_hourlywage = fields.Float(u'z時間割増率', default=1.00)
    pj_p_is_duty = fields.Boolean(u'z精算')
    pj_p_duty_lowerlimit = fields.Integer(u'z精算下限')
    pj_p_duty_upperlimit = fields.Integer(u'z精算上限')
    pj_p_price_lowerlimit = fields.Integer(u'z下限単価')
    pj_p_price_upperlimit = fields.Integer(u'z上限単価')
    pj_p_manhour_contract = fields.Float(u'z標準工数', default=1)
    pj_p_amount = fields.Integer(u'z発注金額', compute='_compute_pj_p_amount', store=True)
    pj_p_cost = fields.Integer(u'z原価', compute='_compute_pj_p_cost', store=True)

    ## Purchase 発注
    pj_p_manhour = fields.Float(u'z当月工数', default=1)
    pj_p_duty_hours = fields.Float(u'z当月時間・日数')
    pj_p_hours_lowerlimit = fields.Float(
        u'z当月下限', compute='_compute_pj_p_hours', store=True)
    pj_p_hours_upperlimit = fields.Float(
        u'z当月上限', compute='_compute_pj_p_hours', store=True)
    pj_p_payoffhour = fields.Float(
        u'z精算時間・日数', compute='_compute_pj_p_payoffhour', store=True)
    pj_p_excess_deduct = fields.Integer(
        u'z超過・控除', compute='_compute_pj_p_excess_deduct', store=True)
    pj_p_adjustment = fields.Integer(u'z調整額')
    pj_p_adjustment_comment = fields.Char(u'z調整理由')

    # # 小計項目を追加する
    pj_p_subtotal = fields.Integer(u'z小計', compute='_compute_pj_p_subtotal', store=True)
    pj_p_tax = fields.Integer(u'z消費税', compute='_compute_pj_p_tax', store=True)

    pj_p_carfare = fields.Integer(u'z業務費用')
    pj_p_amount_subtotal = fields.Integer(u'z発注合計', compute='_compute_pj_p_amount_subtotal', store=True)
    pj_p_amount_inprogress = fields.Integer(u'z仕掛品金額')

    pj_confirm = fields.Boolean('承認締め', index=True)
    pj_state = fields.Selection([
        ('wip', 'WIP'),
        ('done', 'Done'),
        ], default='wip')

    # CompanyId
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.user.company_id.id)

    pj_o_amount_inprogress_all = fields.Integer(u'仕掛品累計金額')
    pj_p_amount_inprogress_all = fields.Integer(u'z仕掛品累計金額')

    def toggle_confirm(self):
        for c in self:
            c.pj_confirm = not c.pj_confirm

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

    # PJ要員選択後、PJ要員情報をセットする
    @api.onchange('pj_order_id')
    def onchange_pjorder(self):
        if self.pj_order_id :
            self.update({
                # 'pj_member_id':self.pj_order_id.pj_member_id,
                # 'pj_member_cd':self.pj_order_id.pj_member_cd,
                # 'pj_member_type':self.pj_order_id.pj_member_type,
                # 'pj_member_note':self.pj_order_id.pj_member_note,
                # 'pj_id':self.pj_order_id.pj_id,
                # 'pj_cd':self.pj_order_id.pj_cd,
                # 'pj_name':self.pj_order_id.pj_name,
                # 'pj_bu_cd':self.pj_order_id.pj_bu_cd,
                # 'pj_bu_name':self.pj_order_id.pj_bu_name,
                # 'pj_partner_c_id':self.pj_order_id.pj_partner_c_id,
                # 'pj_partner_c_cd':self.pj_order_id.pj_partner_c_cd,
                # 'pj_partner_s_id':self.pj_order_id.pj_partner_s_id,
                # 'pj_partner_s_cd':self.pj_order_id.pj_partner_s_cd,
                'pj_o_price_type':self.pj_order_id.pj_o_price_type,
                'pj_o_price_unit':self.pj_order_id.pj_o_price_unit,
                'pj_o_price_purchase': self.pj_order_id.pj_o_price_purchase,
                'pj_o_payofftype': self.pj_order_id.pj_o_payofftype,
                'pj_o_normal_dutyhours': self.pj_order_id.pj_o_normal_dutyhours,
                'pj_o_normal_hourlywage': self.pj_order_id.pj_o_normal_hourlywage,
                'pj_o_is_duty': self.pj_order_id.pj_o_is_duty,
                'pj_o_duty_lowerlimit': self.pj_order_id.pj_o_duty_lowerlimit,
                'pj_o_duty_upperlimit': self.pj_order_id.pj_o_duty_upperlimit,
                'pj_o_price_lowerlimit': self.pj_order_id.pj_o_price_lowerlimit,
                'pj_o_price_upperlimit': self.pj_order_id.pj_o_price_upperlimit,
                'pj_o_manhour_contract': self.pj_order_id.pj_o_manhour_contract,
                'pj_o_amount': self.pj_order_id.pj_o_amount,
                'pj_o_cost': self.pj_order_id.pj_o_cost,
                'pj_o_profit': self.pj_order_id.pj_o_profit,
                'pj_o_profitrate': self.pj_order_id.pj_o_profitrate,
                'pj_o_member_orderisprogress':self.pj_order_id.pj_o_member_orderisprogress,
                'pj_o_member_orderdateaccpt':self.pj_order_id.pj_o_member_orderdateaccpt,
                'pj_p_price_type': self.pj_order_id.pj_p_price_type,
                'pj_p_price_unit': self.pj_order_id.pj_p_price_unit,
                'pj_p_normal_dutyhours': self.pj_order_id.pj_p_normal_dutyhours,
                'pj_p_payofftype': self.pj_order_id.pj_p_payofftype,
                'pj_p_normal_hourlywage': self.pj_order_id.pj_p_normal_hourlywage,
                'pj_p_is_duty': self.pj_order_id.pj_p_is_duty,
                'pj_p_duty_lowerlimit': self.pj_order_id.pj_p_duty_lowerlimit,
                'pj_p_duty_upperlimit': self.pj_order_id.pj_p_duty_upperlimit,
                'pj_p_price_lowerlimit': self.pj_order_id.pj_p_price_lowerlimit,
                'pj_p_price_upperlimit': self.pj_order_id.pj_p_price_upperlimit,
                'pj_p_manhour_contract': self.pj_order_id.pj_p_manhour_contract,
                'pj_p_amount': self.pj_order_id.pj_p_amount,
                'pj_p_cost': self.pj_order_id.pj_p_cost,
                'pj_p_member_orderisprogress': self.pj_order_id.pj_p_member_orderisprogress,
                'pj_p_member_orderdateaccpt': self.pj_order_id.pj_p_member_orderdateaccpt,
            })

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

    # 当月下限 pj_o_hours_lowerlimit 当月上限 pj_o_hours_upperlimit
    @api.depends('pj_o_duty_lowerlimit', 'pj_o_duty_upperlimit', 'pj_o_manhour', 'pj_o_payofftype')
    def _compute_pj_o_hours(self):
        for record in self:
            if record.pj_o_price_type == 'month':
                if record.pj_o_payofftype != 'fix':
                    record.pj_o_hours_lowerlimit = round(record.pj_o_duty_lowerlimit * record.pj_o_manhour)
                    record.pj_o_hours_upperlimit = round(record.pj_o_duty_upperlimit * record.pj_o_manhour)

    # 精算時間 pj_o_payoffhour
    @api.depends('pj_o_duty_lowerlimit', 'pj_o_duty_upperlimit', 'pj_o_duty_hours', 'pj_o_manhour', 'pj_o_hours_lowerlimit', 'pj_o_hours_upperlimit')
    def _compute_pj_o_payoffhour(self):
        for record in self:
            if record.pj_o_duty_hours and (record.pj_o_duty_hours < record.pj_o_hours_lowerlimit):
                record.pj_o_payoffhour = record.pj_o_duty_hours - record.pj_o_hours_lowerlimit
            elif record.pj_o_duty_hours and (record.pj_o_duty_hours > record.pj_o_hours_upperlimit):
                record.pj_o_payoffhour = record.pj_o_duty_hours - record.pj_o_hours_upperlimit

    # 超過・控除 pj_o_excess_deduct
    # 時給超過分　単価ｘ1.25
    @api.depends('pj_o_price_lowerlimit', 'pj_o_price_upperlimit', 'pj_o_duty_hours', 'pj_o_payoffhour')
    def _compute_pj_o_excess_deduct(self):
        for record in self:
            if record.pj_o_payoffhour and record.pj_o_payoffhour <= 0:
                record.pj_o_excess_deduct = round(record.pj_o_price_lowerlimit * record.pj_o_payoffhour)
            elif record.pj_o_payoffhour and record.pj_o_payoffhour > 0:
                if record.pj_o_price_type == 'month':
                    record.pj_o_excess_deduct = round(record.pj_o_price_upperlimit * record.pj_o_payoffhour)
                elif record.pj_o_price_type == 'hour':
                    record.pj_o_excess_deduct = math.floor(round(record.pj_o_price_unit * record.pj_o_payoffhour) * record.pj_o_normal_hourlywage)
                elif record.pj_o_price_type == 'day':
                    record.pj_o_excess_deduct = 0
            if record.pj_o_amount and record.pj_o_excess_deduct:
                record.pj_o_subtotal = record.pj_o_amount + record.pj_o_excess_deduct

    # 売上 pj_o_amount
    @api.depends('pj_o_price_unit', 'pj_o_manhour', 'pj_o_hours_lowerlimit', 'pj_o_duty_hours')
    def _compute_pj_o_amount(self):
        for record in self:
            if record.pj_o_price_type == 'month':
                record.pj_o_amount = round(record.pj_o_price_unit * record.pj_o_manhour)
                if record.pj_o_amount and record.pj_o_excess_deduct:
                    record.pj_o_subtotal = record.pj_o_amount + record.pj_o_excess_deduct
            elif record.pj_o_price_type == 'hour':
                record.pj_o_amount = round(record.pj_o_price_unit * record.pj_o_hours_lowerlimit)
                if record.pj_o_amount and record.pj_o_excess_deduct:
                    record.pj_o_subtotal = record.pj_o_amount + record.pj_o_excess_deduct
            elif record.pj_o_price_type == 'day':
                record.pj_o_amount = round(record.pj_o_price_unit * record.pj_o_duty_hours)
                if record.pj_o_amount:
                    record.pj_o_subtotal = record.pj_o_amount

    # 小計 pj_o_subtotal
    @api.depends('pj_o_amount', 'pj_o_excess_deduct', 'pj_o_adjustment')
    def _compute_pj_o_subtotal(self):
        for record in self:
            record.pj_o_subtotal = record.pj_o_amount + record.pj_o_excess_deduct + record.pj_o_adjustment

    # 消費税 pj_o_tax
    # 消費税計算　消費税率取得
    @api.depends('pj_o_amount', 'pj_o_excess_deduct', 'pj_o_adjustment')
    def _compute_pj_o_tax(self):
        for record in self:
            tax = self.env['ss.tax']._get_tax_rate(record.pj_long_date)
            record.pj_o_tax = round((record.pj_o_amount + record.pj_o_excess_deduct + record.pj_o_adjustment) * tax)

    # 売上合計 pj_o_amount_subtotal 小計+ 消費税 + 業務費用
    # 仕掛品処理　
    @api.depends('pj_o_subtotal', 'pj_o_carfare', 'pj_o_adjustment')
    def _compute_pj_o_amount_subtotal(self):
        for record in self:
            record.pj_o_amount_subtotal = record.pj_o_subtotal + record.pj_o_tax + record.pj_o_carfare
            # 仕掛品金の場合の処理
            if record.pj_o_member_orderisprogress == True :
                #　契約内の前月の仕掛品があれば、取得する

                amount_inprogress_premonth = 0
                lastmonth = (datetime.strptime(record.pj_long_date, "%Y-%m-%d") - relativedelta(months=1)).strftime('%Y%m')
                # sqlcondition = ['&', ('pj_account_date', '=', lastmonth), '&', ('pj_member_cd', '=', record.pj_member_cd), ('pj_cd', '=', record.pj_cd)]
                sqlcondition = ['&', ('pj_account_date', '=', lastmonth), '&', ('pj_order_id', '=', record.pj_order_id.id), ('pj_cd', '=', record.pj_cd)]
                emp = self.env['ss.sales'].search(sqlcondition)
                if emp:
                    amount_inprogress_premonth = emp.pj_o_amount_inprogress_all

                record.pj_o_amount_inprogress = record.pj_o_amount_subtotal
                record.pj_o_amount_subtotal = 0
                record.pj_o_amount_inprogress_all = record.pj_o_amount_inprogress + amount_inprogress_premonth

                # 検収月の場合は
                if record.pj_account_date == datetime.strptime(record.pj_o_member_orderdateaccpt, "%Y-%m-%d").strftime('%Y%m'):
                    record.pj_o_amount_subtotal = record.pj_o_amount_inprogress + amount_inprogress_premonth
                    record.pj_o_amount_inprogress_all = 0

    ## Purchase 発注
    # 当月下限 pj_p_hours_lowerlimit 当月上限 pj_p_hours_upperlimit
    @api.depends('pj_p_duty_lowerlimit', 'pj_p_duty_upperlimit', 'pj_p_manhour', 'pj_p_payofftype')
    def _compute_pj_p_hours(self):
        for record in self:
            if record.pj_p_price_type == 'month':
                if record.pj_p_payofftype != 'fix':
                    record.pj_p_hours_lowerlimit = round(record.pj_p_duty_lowerlimit * record.pj_p_manhour)
                    record.pj_p_hours_upperlimit = round(record.pj_p_duty_upperlimit * record.pj_p_manhour)

    # 精算時間 pj_p_payoffhour
    @api.depends('pj_p_duty_lowerlimit', 'pj_p_duty_upperlimit', 'pj_p_duty_hours', 'pj_p_manhour', 'pj_p_hours_lowerlimit', 'pj_p_hours_upperlimit')
    def _compute_pj_p_payoffhour(self):
        for record in self:
            if record.pj_p_duty_hours and (record.pj_p_duty_hours < record.pj_p_hours_lowerlimit):
                record.pj_p_payoffhour = record.pj_p_duty_hours - record.pj_p_hours_lowerlimit
            elif record.pj_p_duty_hours and (record.pj_p_duty_hours > record.pj_p_hours_upperlimit):
                record.pj_p_payoffhour = record.pj_p_duty_hours - record.pj_p_hours_upperlimit

    # 超過・控除 pj_p_excess_deduct
    # 時給超過分　単価ｘ1.25
    @api.depends('pj_p_price_lowerlimit', 'pj_p_price_upperlimit', 'pj_p_duty_hours', 'pj_p_payoffhour', 'pj_p_manhour')
    def _compute_pj_p_excess_deduct(self):
        for record in self:
            if record.pj_p_payoffhour and record.pj_p_payoffhour <= 0:
                record.pj_p_excess_deduct = round(record.pj_p_price_lowerlimit * record.pj_p_payoffhour)
            elif record.pj_p_payoffhour and record.pj_p_payoffhour > 0:
                if record.pj_p_price_type == 'month':
                    record.pj_p_excess_deduct = round(record.pj_p_price_upperlimit * record.pj_p_payoffhour)
                elif record.pj_p_price_type == 'hour':
                    record.pj_p_excess_deduct = math.floor(round(record.pj_p_price_unit * record.pj_p_payoffhour) * record.pj_p_normal_hourlywage)
                elif record.pj_p_price_type == 'day':
                    record.pj_p_excess_deduct = 0
            if record.pj_p_amount and record.pj_p_excess_deduct:
                record.pj_p_subtotal = record.pj_p_amount + record.pj_p_excess_deduct

    # 売上 pj_p_amount
    @api.depends('pj_p_price_unit', 'pj_p_manhour', 'pj_p_hours_lowerlimit', 'pj_p_duty_hours')
    def _compute_pj_p_amount(self):
        for record in self:
            if record.pj_p_price_type == 'month':
                record.pj_p_amount = round(record.pj_p_price_unit * record.pj_p_manhour)
                if record.pj_p_amount and record.pj_p_excess_deduct:
                    record.pj_p_subtotal = record.pj_p_amount + record.pj_p_excess_deduct
            elif record.pj_p_price_type == 'hour':
                record.pj_p_amount = round(record.pj_p_price_unit * record.pj_p_hours_lowerlimit)
                if record.pj_p_amount and record.pj_p_excess_deduct:
                    record.pj_p_subtotal = record.pj_p_amount + record.pj_p_excess_deduct
            elif record.pj_p_price_type == 'day':
                record.pj_p_amount = round(record.pj_p_price_unit * record.pj_p_duty_hours)
                if record.pj_p_amount :
                    record.pj_p_subtotal = record.pj_p_amount

    # 小計 pj_p_subtotal
    @api.depends('pj_p_amount', 'pj_p_excess_deduct', 'pj_p_adjustment')
    def _compute_pj_p_subtotal(self):
        for record in self:
            record.pj_p_subtotal = record.pj_p_amount + record.pj_p_excess_deduct + record.pj_p_adjustment

    # 消費税 pj_p_tax
    # 消費税計算　消費税率取得
    @api.depends('pj_p_amount', 'pj_p_excess_deduct', 'pj_p_adjustment')
    def _compute_pj_p_tax(self):
        for record in self:
            tax = self.env['ss.tax']._get_tax_rate(record.pj_long_date)
            record.pj_p_tax = round((record.pj_p_amount + record.pj_p_excess_deduct + record.pj_p_adjustment) * tax)

    # 売上合計 pj_p_amount_subtotal 小計+ 消費税 + 業務費用
    @api.depends('pj_p_subtotal', 'pj_p_carfare', 'pj_p_adjustment')
    def _compute_pj_p_amount_subtotal(self):
        for record in self:
            record.pj_p_amount_subtotal = record.pj_p_subtotal + record.pj_p_tax + record.pj_p_carfare
            # 仕掛品金の場合の処理
            if record.pj_p_member_orderisprogress == True :
                #　契約内の前月の仕掛品があれば、取得する

                amount_inprogress_premonth = 0
                lastmonth = (datetime.strptime(record.pj_long_date, "%Y-%m-%d") - relativedelta(months=1)).strftime('%Y%m')
                sqlcondition = ['&', ('pj_account_date', '=', lastmonth), '&', ('pj_member_cd', '=', record.pj_member_cd), ('pj_cd', '=', record.pj_cd)]
                emp = self.env['ss.sales'].search(sqlcondition)
                if emp:
                    amount_inprogress_premonth = emp.pj_p_amount_inprogress_all

                record.pj_p_amount_inprogress = record.pj_p_amount_subtotal
                record.pj_p_amount_subtotal = 0
                record.pj_p_amount_inprogress_all = record.pj_p_amount_inprogress + amount_inprogress_premonth

                # 検収月の場合は
                if record.pj_account_date == datetime.strptime(record.pj_p_member_orderdateaccpt, "%Y-%m-%d").strftime('%Y%m'):
                    record.pj_p_amount_subtotal = record.pj_p_amount_inprogress + amount_inprogress_premonth
                    record.pj_p_amount_inprogress_all = 0


    # ------------------------------------------------------------------------------------------------
    @api.onchange('pj_o_manhour','pj_o_duty_hours')
    def onchange_hours_o(self):
        self._compute_pj_o_payoffhour()
        self._compute_pj_o_excess_deduct()
        self._compute_pj_o_amount()
        self._compute_pj_o_subtotal()
        self._compute_pj_o_tax()
        self._compute_pj_o_amount_subtotal()
        for record in self:
            record.pj_p_manhour = record.pj_o_manhour
            record.pj_p_duty_hours = record.pj_o_duty_hours
        self._compute_pj_o_profit()
        self._compute_pj_o_profitrate()

    # 受注条件マスタ情報⇒実績へCopy
    @api.multi
    def action_CopyFromOrder_o(self):
        for record in self:
            self.update({
                'pj_o_member_orderisprogress': self.pj_order_id.pj_o_member_orderisprogress,
                'pj_o_member_orderdateaccpt': self.pj_order_id.pj_o_member_orderdateaccpt,
                'pj_o_price_type':self.pj_order_id.pj_o_price_type,
                'pj_o_price_unit':self.pj_order_id.pj_o_price_unit,
                'pj_o_price_purchase':self.pj_order_id.pj_o_price_purchase,
                'pj_o_payofftype': self.pj_order_id.pj_o_payofftype,
                'pj_o_normal_dutyhours':self.pj_order_id.pj_o_normal_dutyhours,
                'pj_o_is_duty': self.pj_order_id.pj_o_is_duty,
                'pj_o_duty_lowerlimit': self.pj_order_id.pj_o_duty_lowerlimit,
                'pj_o_duty_upperlimit': self.pj_order_id.pj_o_duty_upperlimit,
                'pj_o_price_lowerlimit': self.pj_order_id.pj_o_price_lowerlimit,
                'pj_o_price_upperlimit': self.pj_order_id.pj_o_price_upperlimit,
                'pj_o_amount': self.pj_order_id.pj_o_amount,
                'pj_o_cost': self.pj_order_id.pj_o_cost,
            })
        self.onchange_hours_o()

    # 入力変更後　強制再計算
    @api.onchange('pj_p_manhour','pj_p_duty_hours')
    def onchange_hours_p(self):
        self._compute_pj_p_payoffhour()
        self._compute_pj_p_excess_deduct()
        self._compute_pj_p_amount()
        self._compute_pj_p_subtotal()
        self._compute_pj_p_tax()
        self._compute_pj_p_amount_subtotal()
        self._compute_pj_o_profit()
        self._compute_pj_o_profitrate()


    #  粗利の計算
    @api.depends('pj_p_amount_subtotal', 'pj_o_amount_subtotal')
    def _compute_pj_o_profit(self):
        for pj in self:
            if pj.pj_p_amount_subtotal and pj.pj_o_amount_subtotal:
                pj.pj_o_profit = pj.pj_o_amount_subtotal - pj.pj_p_amount_subtotal

    #  粗利率の計算
    @api.depends('pj_p_amount_subtotal', 'pj_o_amount_subtotal')
    def _compute_pj_o_profitrate(self):
        for pj in self:
            if pj.pj_p_amount_subtotal and pj.pj_o_amount_subtotal:
                pj.pj_o_profitrate = (pj.pj_o_amount_subtotal - pj.pj_p_amount_subtotal) / pj.pj_o_amount_subtotal

    # 発注条件マスタ情報⇒実績へCopy
    @api.multi
    def action_CopyFromOrder_p(self):
        for record in self:
            self.update({
                'pj_p_member_orderisprogress': self.pj_order_id.pj_p_member_orderisprogress,
                'pj_p_member_orderdateaccpt': self.pj_order_id.pj_p_member_orderdateaccpt,
                'pj_p_price_type':self.pj_order_id.pj_p_price_type,
                'pj_p_price_unit':self.pj_order_id.pj_p_price_unit,
                'pj_p_price_purchase':self.pj_order_id.pj_p_price_purchase,
                'pj_p_payofftype': self.pj_order_id.pj_p_payofftype,
                'pj_p_normal_dutyhours':self.pj_order_id.pj_p_normal_dutyhours,
                'pj_p_is_duty': self.pj_order_id.pj_p_is_duty,
                'pj_p_duty_lowerlimit': self.pj_order_id.pj_p_duty_lowerlimit,
                'pj_p_duty_upperlimit': self.pj_order_id.pj_p_duty_upperlimit,
                'pj_p_price_lowerlimit': self.pj_order_id.pj_p_price_lowerlimit,
                'pj_p_price_upperlimit': self.pj_order_id.pj_p_price_upperlimit,
                'pj_p_amount': self.pj_order_id.pj_p_amount,
                'pj_p_cost': self.pj_order_id.pj_p_cost,
            })
        self.onchange_hours_p()

    # 締め処理ロック
    @api.one
    def rock(self):
        self.write({
            'pj_state': 'done',
        })

    # 締め処理ロック解除
    @api.one
    def unlock(self):
        self.write({
            'pj_state': 'wip'
        })


# # 確認締め
# @api.multi
# def toggle_confirm(self):
#     for record in self:
#         self.update({
#             'pj_p_member_orderisprogress': self.pj_order_id.pj_p_member_orderisprogress,
#         })

