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

class SsBudget(models.Model):
    _name = 'ss.budget'
    _rec_name = 'budget_year'

    # bu_id = fields.Many2one('ss.bu', '部署ID', required=True)
    department = fields.Many2one('hr.department', 'BU')
    department_cd = fields.Char('部門コード', related='department.x_department_cd', store=True)
    department_name = fields.Char('部門名', related='department.name', store=True)

    # Bu名称を取る
    # bu_name = fields.Char(related="bu_id.name", string="部署名称")

    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, readonly = True,
        default=lambda self: self.env.user.company_id.id)
    # 予算年度リストを表示する
    budget_year = fields.Selection([
                (num, str(num)) for num in
                range( ((datetime.now().year)-3), ((datetime.now().year)+10)) ], 
                '予算年度', default=datetime.now().year)

    status = fields.Char('状態')

    budget_earning1 = fields.Integer('予算_売上1月')
    budget_cost1 = fields.Integer('予算_原価1月')
    budget_charge1 = fields.Integer('予算_諸費用1月')
    budget_profit1 = fields.Integer('予算_粗利1月', readonly = True, store = True, compute='_compute_budget_profit1')
    budget_ratio1 = fields.Float('予算_粗利率1月', readonly = True, store = True, compute='_compute_budget_profit1')
    achieve_earning1 = fields.Integer('実績_売上1月', readonly = True)
    achieve_cost1 = fields.Integer('実績_原価1月', readonly = True)
    achieve_charge1 = fields.Integer('実績_諸費用1月', readonly = True)
    achieve_profit1 = fields.Integer('実績_粗利1月', readonly = True)
    achieve_ratio1 = fields.Float('実績_粗利率1月', readonly = True)

    budget_earning2 = fields.Integer('予算_売上2月')
    budget_cost2 = fields.Integer('予算_原価2月')
    budget_charge2 = fields.Integer('予算_諸費用2月')
    budget_profit2 = fields.Integer('予算_粗利2月', readonly = True, store = True, compute='_compute_budget_profit2')
    budget_ratio2 = fields.Float('予算_粗利率2月', readonly = True, store = True, compute='_compute_budget_profit2')
    achieve_earning2 = fields.Integer('実績_売上2月', readonly = True)
    achieve_cost2 = fields.Integer('実績_原価2月', readonly = True)
    achieve_charge2 = fields.Integer('実績_諸費用2月', readonly = True)
    achieve_profit2 = fields.Integer('実績_粗利2月', readonly = True)
    achieve_ratio2 = fields.Float('実績_粗利率2月', readonly = True)

    budget_earning3 = fields.Integer('予算_売上3月')
    budget_cost3 = fields.Integer('予算_原価3月')
    budget_charge3 = fields.Integer('予算_諸費用3月')
    budget_profit3 = fields.Integer('予算_粗利3月', readonly = True, store = True, compute='_compute_budget_profit3')
    budget_ratio3 = fields.Float('予算_粗利率3月', readonly = True, store = True, compute='_compute_budget_profit3')
    achieve_earning3 = fields.Integer('実績_売上3月', readonly = True)
    achieve_cost3 = fields.Integer('実績_原価3月', readonly = True)
    achieve_charge3 = fields.Integer('実績_諸費用3月', readonly = True)
    achieve_profit3 = fields.Integer('実績_粗利3月', readonly = True)
    achieve_ratio3 = fields.Float('実績_粗利率3月', readonly = True)

    # budget_earning_1q = fields.Integer('予算_売上1Q')
    # budget_cost_1q = fields.Integer('予算_原価1Q')
    # budget_charge_1q = fields.Integer('予算_諸費用1Q')
    # budget_profit_1q = fields.Integer('予算_粗利1Q', readonly = True, store = True, compute='_compute_budget_profit_1q')
    # budget_ratio_1q = fields.Float('予算_粗利率1Q', readonly = True, store = True, compute='_compute_budget_ratio_1q')
    # achieve_earning_1q = fields.Integer('実績_売上1Q', readonly = True)
    # achieve_cost_1q = fields.Integer('実績_原価1Q', readonly = True)
    # achieve_charge_1q = fields.Integer('実績_諸費用1Q', readonly = True)
    # achieve_profit_1q = fields.Integer('実績_粗利1Q', readonly = True)
    # achieve_ratio_1q = fields.Float('実績_粗利率1Q', readonly = True)

    budget_earning4 = fields.Integer('予算_売上4月')
    budget_cost4 = fields.Integer('予算_原価4月')
    budget_charge4 = fields.Integer('予算_諸費用4月')
    budget_profit4 = fields.Integer('予算_粗利4月', readonly = True, store = True, compute='_compute_budget_profit4')
    budget_ratio4 = fields.Float('予算_粗利率4月', readonly = True, store = True, compute='_compute_budget_profit4')
    achieve_earning4 = fields.Integer('実績_売上4月', readonly = True)
    achieve_cost4 = fields.Integer('実績_原価4月', readonly = True)
    achieve_charge4 = fields.Integer('実績_諸費用4月', readonly = True)
    achieve_profit4 = fields.Integer('実績_粗利4月', readonly = True)
    achieve_ratio4 = fields.Float('実績_粗利率4月', readonly = True)

    budget_earning5 = fields.Integer('予算_売上5月')
    budget_cost5 = fields.Integer('予算_原価5月')
    budget_charge5 = fields.Integer('予算_諸費用5月')
    budget_profit5 = fields.Integer('予算_粗利5月', readonly = True, store = True, compute='_compute_budget_profit5')
    budget_ratio5 = fields.Float('予算_粗利率5月', readonly = True, store = True, compute='_compute_budget_profit5')
    achieve_earning5 = fields.Integer('実績_売上5月', readonly = True)
    achieve_cost5 = fields.Integer('実績_原価5月', readonly = True)
    achieve_charge5 = fields.Integer('実績_諸費用5月', readonly = True)
    achieve_profit5 = fields.Integer('実績_粗利5月', readonly = True)
    achieve_ratio5 = fields.Float('実績_粗利率5月', readonly = True)

    budget_earning6 = fields.Integer('予算_売上6月')
    budget_cost6 = fields.Integer('予算_原価6月')
    budget_charge6 = fields.Integer('予算_諸費用6月')
    budget_profit6 = fields.Integer('予算_粗利6月', readonly = True, store = True, compute='_compute_budget_profit6')
    budget_ratio6 = fields.Float('予算_粗利率6月', readonly = True, store = True, compute='_compute_budget_profit6')
    achieve_earning6 = fields.Integer('実績_売上6月', readonly = True)
    achieve_cost6 = fields.Integer('実績_原価6月', readonly = True)
    achieve_charge6 = fields.Integer('実績_諸費用6月', readonly = True)
    achieve_profit6 = fields.Integer('実績_粗利6月', readonly = True)
    achieve_ratio6 = fields.Float('実績_粗利率6月', readonly = True)

    budget_earning7 = fields.Integer('予算_売上7月')
    budget_cost7 = fields.Integer('予算_原価7月')
    budget_charge7 = fields.Integer('予算_諸費用7月')
    budget_profit7 = fields.Integer('予算_粗利7月', readonly = True, store = True, compute='_compute_budget_profit7')
    budget_ratio7 = fields.Float('予算_粗利率7月', readonly = True, store = True, compute='_compute_budget_profit7')
    achieve_earning7 = fields.Integer('実績_売上7月', readonly = True)
    achieve_cost7 = fields.Integer('実績_原価7月', readonly = True)
    achieve_charge7 = fields.Integer('実績_諸費用7月', readonly = True)
    achieve_profit7 = fields.Integer('実績_粗利7月', readonly = True)
    achieve_ratio7 = fields.Float('実績_粗利率7月', readonly = True)

    budget_earning8 = fields.Integer('予算_売上8月')
    budget_cost8 = fields.Integer('予算_原価8月')
    budget_charge8 = fields.Integer('予算_諸費用8月')
    budget_profit8 = fields.Integer('予算_粗利8月', readonly = True, store = True, compute='_compute_budget_profit8')
    budget_ratio8 = fields.Float('予算_粗利率8月', readonly = True, store = True, compute='_compute_budget_profit8')
    achieve_earning8 = fields.Integer('実績_売上8月', readonly = True)
    achieve_cost8 = fields.Integer('実績_原価8月', readonly = True)
    achieve_charge8 = fields.Integer('実績_諸費用8月', readonly = True)
    achieve_profit8 = fields.Integer('実績_粗利8月', readonly = True)
    achieve_ratio8 = fields.Float('実績_粗利率8月', readonly = True)

    budget_earning9 = fields.Integer('予算_売上9月')
    budget_cost9 = fields.Integer('予算_原価9月')
    budget_charge9 = fields.Integer('予算_諸費用9月')
    budget_profit9 = fields.Integer('予算_粗利9月', readonly = True, store = True, compute='_compute_budget_profit9')
    budget_ratio9 = fields.Float('予算_粗利率9月', readonly = True, store = True, compute='_compute_budget_profit9')
    achieve_earning9 = fields.Integer('実績_売上9月', readonly = True)
    achieve_cost9 = fields.Integer('実績_原価9月', readonly = True)
    achieve_charge9 = fields.Integer('実績_諸費用9月', readonly = True)
    achieve_profit9 = fields.Integer('実績_粗利9月', readonly = True)
    achieve_ratio9 = fields.Float('実績_粗利率9月', readonly = True)

    budget_earning10 = fields.Integer('予算_売上10月')
    budget_cost10 = fields.Integer('予算_原価10月')
    budget_charge10 = fields.Integer('予算_諸費用10月')
    budget_profit10 = fields.Integer('予算_粗利10月', readonly = True, store = True, compute='_compute_budget_profit10')
    budget_ratio10 = fields.Float('予算_粗利率10月', readonly = True, store = True, compute='_compute_budget_profit10')
    achieve_earning10 = fields.Integer('実績_売上10月', readonly = True)
    achieve_cost10 = fields.Integer('実績_原価10月', readonly = True)
    achieve_charge10 = fields.Integer('実績_諸費用10月', readonly = True)
    achieve_profit10 = fields.Integer('実績_粗利10月', readonly = True)
    achieve_ratio10 = fields.Float('実績_粗利率10月', readonly = True)

    budget_earning11 = fields.Integer('予算_売上11月')
    budget_cost11 = fields.Integer('予算_原価11月')
    budget_charge11 = fields.Integer('予算_諸費用11月')
    budget_profit11 = fields.Integer('予算_粗利11月', readonly = True, store = True, compute='_compute_budget_profit11')
    budget_ratio11 = fields.Float('予算_粗利率11月', readonly = True, store = True, compute='_compute_budget_profit11')
    achieve_earning11 = fields.Integer('実績_売上11月', readonly = True)
    achieve_cost11 = fields.Integer('実績_原価11月', readonly = True)
    achieve_charge11 = fields.Integer('実績_諸費用11月', readonly = True)
    achieve_profit11 = fields.Integer('実績_粗利11月', readonly = True)
    achieve_ratio11 = fields.Float('実績_粗利率11月', readonly = True)

    budget_earning12 = fields.Integer('予算_売上12月')
    budget_cost12 = fields.Integer('予算_原価12月')
    budget_charge12 = fields.Integer('予算_諸費用12月')
    budget_profit12 = fields.Integer('予算_粗利12月', readonly = True, store = True, compute='_compute_budget_profit12')
    budget_ratio12 = fields.Float('予算_粗利率12月', readonly = True, store = True, compute='_compute_budget_profit12')
    achieve_earning12 = fields.Integer('実績_売上12月', readonly = True)
    achieve_cost12 = fields.Integer('実績_原価12月', readonly = True)
    achieve_charge12 = fields.Integer('実績_諸費用12月', readonly = True)
    achieve_profit12 = fields.Integer('実績_粗利12月', readonly = True)
    achieve_ratio12 = fields.Float('実績_粗利率12月', readonly = True)

    budget_earnings = fields.Integer('予算_売上合計', readonly = True, store = True, compute='_compute_budget_earnings')
    budget_costs = fields.Integer('予算_原価合計', readonly = True, store = True, compute='_compute_budget_costs')
    budget_charges = fields.Integer('予算_諸費用合計', readonly = True, store = True, compute='_compute_budget_charges')
    budget_profits = fields.Integer('予算_粗利合計', readonly = True, store = True, compute='_compute_budget_profit')
    budget_ratios = fields.Float('予算_総粗利率', readonly = True, store = True, compute='_compute_budget_ratios')
    achieve_earnings = fields.Integer('実績_売上合計', readonly = True)
    achieve_costs = fields.Integer('実績_原価合計', readonly = True)
    achieve_charges = fields.Integer('実績_諸費用合計', readonly = True)
    achieve_profits = fields.Integer('実績_粗利合計', readonly = True)
    achieve_ratios = fields.Float('実績_総粗利率', readonly = True)

    _sql_constraints = [
        ('unique_department',
         'unique(department, budget_year)', 'department budget_year should be unique per bu!')]

    # 予算_粗利　自動計算
    @api.depends('budget_earning1','budget_cost1','budget_charge1')
    def _compute_budget_profit1(self):
        self.budget_profit1 = self.budget_earning1 - self.budget_cost1 - self.budget_charge1
        if self.budget_earning1:
            self.budget_ratio1 = self.budget_profit1 / self.budget_earning1 * 100

    @api.depends('budget_earning2','budget_cost2','budget_charge2')
    def _compute_budget_profit2(self):
        self.budget_profit2 = self.budget_earning2 - self.budget_cost2 - self.budget_charge2
        if self.budget_earning2:
            self.budget_ratio2 = self.budget_profit2 / self.budget_earning2 * 100

    @api.depends('budget_earning3','budget_cost3','budget_charge3')
    def _compute_budget_profit3(self):
        self.budget_profit3 = self.budget_earning3 - self.budget_cost3 - self.budget_charge3
        if self.budget_earning3:
            self.budget_ratio3 = self.budget_profit3 / self.budget_earning3 * 100

    @api.depends('budget_earning4','budget_cost4','budget_charge4')
    def _compute_budget_profit4(self):
        self.budget_profit4 = self.budget_earning4 - self.budget_cost4 - self.budget_charge4
        if self.budget_earning4:
            self.budget_ratio4 = self.budget_profit4 / self.budget_earning4 * 100

    @api.depends('budget_earning5','budget_cost5','budget_charge5')
    def _compute_budget_profit5(self):
        self.budget_profit5 = self.budget_earning5 - self.budget_cost5 - self.budget_charge5
        if self.budget_earning5:
            self.budget_ratio5 = self.budget_profit5 / self.budget_earning5 * 100

    @api.depends('budget_earning6','budget_cost6','budget_charge6')
    def _compute_budget_profit6(self):
        self.budget_profit6 = self.budget_earning6 - self.budget_cost6 - self.budget_charge6
        if self.budget_earning6:
            self.budget_ratio6 = self.budget_profit6 / self.budget_earning6 * 100

    @api.depends('budget_earning7','budget_cost7','budget_charge7')
    def _compute_budget_profit7(self):
        self.budget_profit7 = self.budget_earning7 - self.budget_cost7 - self.budget_charge7
        if self.budget_earning7:
            self.budget_ratio7 = self.budget_profit7 / self.budget_earning7 * 100

    @api.depends('budget_earning8','budget_cost8','budget_charge8')
    def _compute_budget_profit8(self):
        self.budget_profit8 = self.budget_earning8 - self.budget_cost8 - self.budget_charge8
        if self.budget_earning8:
            self.budget_ratio8 = self.budget_profit8 / self.budget_earning8 * 100

    @api.depends('budget_earning9','budget_cost9','budget_charge9')
    def _compute_budget_profit9(self):
        self.budget_profit9 = self.budget_earning9 - self.budget_cost9 - self.budget_charge9
        if self.budget_earning9:
            self.budget_ratio9 = self.budget_profit9 / self.budget_earning9 * 100

    @api.depends('budget_earning10','budget_cost10','budget_charge10')
    def _compute_budget_profit10(self):
        self.budget_profit10 = self.budget_earning10 - self.budget_cost10 - self.budget_charge10
        if self.budget_earning10:
            self.budget_ratio10 = self.budget_profit10 / self.budget_earning10 * 100

    @api.depends('budget_earning11','budget_cost11','budget_charge11')
    def _compute_budget_profit11(self):
        self.budget_profit11 = self.budget_earning11 - self.budget_cost11 - self.budget_charge11
        if self.budget_earning11:
            self.budget_ratio11 = self.budget_profit11 / self.budget_earning11 * 100

    @api.depends('budget_earning12','budget_cost12','budget_charge12')
    def _compute_budget_profit12(self):
        self.budget_profit12 = self.budget_earning12 - self.budget_cost12 - self.budget_charge12
        if self.budget_earning12:
            self.budget_ratio12 = self.budget_profit12 / self.budget_earning12 * 100


    # 予算_売上合計　自動計算
    @api.depends('budget_earning1','budget_earning2','budget_earning3','budget_earning4',
                'budget_earning5','budget_earning6','budget_earning7','budget_earning8',
                'budget_earning9','budget_earning10','budget_earning11','budget_earning12') 
    def _compute_budget_earnings(self):
        self.budget_earnings = (self.budget_earning1 + self.budget_earning2 + self.budget_earning3 
                            + self.budget_earning4 + self.budget_earning5 + self.budget_earning6 
                            + self.budget_earning7 + self.budget_earning8 + self.budget_earning9 
                            + self.budget_earning10 + self.budget_earning11 + self.budget_earning12)

    # 予算_原価合計　自動計算
    @api.depends('budget_cost1','budget_cost2','budget_cost3','budget_cost4',
                'budget_cost5','budget_cost6','budget_cost7','budget_cost8',
                'budget_cost9','budget_cost10','budget_cost11','budget_cost12') 
    def _compute_budget_costs(self):
        self.budget_costs = (self.budget_cost1 + self.budget_cost2 + self.budget_cost3 
                            + self.budget_cost4 + self.budget_cost5 + self.budget_cost6 
                            + self.budget_cost7 + self.budget_cost8 + self.budget_cost9 
                            + self.budget_cost10 + self.budget_cost11 + self.budget_cost12)

    # 予算_諸費用合計　自動計算
    @api.depends('budget_charge1','budget_charge2','budget_charge3','budget_charge4',
                'budget_charge5','budget_charge6','budget_charge7','budget_charge8',
                'budget_charge9','budget_charge10','budget_charge11','budget_charge12') 
    def _compute_budget_charges(self):
        self.budget_charges = (self.budget_charge1 + self.budget_charge2 + self.budget_charge3 
                            + self.budget_charge4 + self.budget_charge5 + self.budget_charge6 
                            + self.budget_charge7 + self.budget_charge8 + self.budget_charge9 
                            + self.budget_charge10 + self.budget_charge11 + self.budget_charge12)

    # 予算_粗利合計　自動計算
    @api.depends('budget_profit1','budget_profit2','budget_profit3','budget_profit4',
                'budget_profit5','budget_profit6','budget_profit7','budget_profit8',
                'budget_profit9','budget_profit10','budget_profit11','budget_profit12')
    def _compute_budget_profit(self):
        self.budget_profits = (self.budget_profit1 + self.budget_profit2 + self.budget_profit3 
                            + self.budget_profit4 + self.budget_profit5 + self.budget_profit6 
                            + self.budget_profit7 + self.budget_profit8 + self.budget_profit9 
                            + self.budget_profit10 + self.budget_profit11 + self.budget_profit12)

    # 予算_粗利率　自動計算
    @api.depends('budget_earnings','budget_costs','budget_charges')
    def _compute_budget_ratios(self):
        if self.budget_earnings:
            self.budget_ratios = (self.budget_earnings - self.budget_costs - self.budget_charges) / self.budget_earnings * 100
