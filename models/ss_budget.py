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
    department = fields.Many2one('hr.department', 'BUコード')
    department_name = fields.Char('BU名', related='department.name')

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

    # budget_earnings = fields.Integer('予算_売上合計')
    # budget_profits = fields.Integer('予算_粗利合計')
    # achieve_earnings = fields.Integer('実績_売上合計')
    # achieve_profits = fields.Integer('実績_粗利合計')

    budget_earning1 = fields.Integer('予算_売上1月')
    budget_profit1 = fields.Integer('予算_粗利1月')
    achieve_earning1 = fields.Integer('実績_売上1月', readonly = True)
    achieve_profit1 = fields.Integer('実績_粗利1月', readonly = True)
    budget_earning2 = fields.Integer('予算_売上2月')
    budget_profit2 = fields.Integer('予算_粗利2月')
    achieve_earning2 = fields.Integer('実績_売上2月', readonly = True)
    achieve_profit2 = fields.Integer('実績_粗利2月', readonly = True)
    budget_earning3 = fields.Integer('予算_売上3月')
    budget_profit3 = fields.Integer('予算_粗利3月')
    achieve_earning3 = fields.Integer('実績_売上3月', readonly = True)
    achieve_profit3 = fields.Integer('実績_粗利3月', readonly = True)
    budget_earning4 = fields.Integer('予算_売上4月')
    budget_profit4 = fields.Integer('予算_粗利4月')
    achieve_earning4 = fields.Integer('実績_売上4月', readonly = True)
    achieve_profit4 = fields.Integer('実績_粗利4月', readonly = True)
    budget_earning5 = fields.Integer('予算_売上5月')
    budget_profit5 = fields.Integer('予算_粗利5月')
    achieve_earning5 = fields.Integer('実績_売上5月', readonly = True)
    achieve_profit5 = fields.Integer('実績_粗利5月', readonly = True)
    budget_earning6 = fields.Integer('予算_売上6月')
    budget_profit6 = fields.Integer('予算_粗利6月')
    achieve_earning6 = fields.Integer('実績_売上6', readonly = True)
    achieve_profit6 = fields.Integer('実績_粗利6', readonly = True)

    budget_earning7 = fields.Integer('予算_売上7月')
    budget_profit7 = fields.Integer('予算_粗利7月')
    achieve_earning7 = fields.Integer('実績_売上7月', readonly = True)
    achieve_profit7 = fields.Integer('実績_粗利7月', readonly = True)
    budget_earning8 = fields.Integer('予算_売上8月')
    budget_profit8 = fields.Integer('予算_粗利8月')
    achieve_earning8 = fields.Integer('実績_売上8月', readonly = True)
    achieve_profit8 = fields.Integer('実績_粗利8月', readonly = True)
    budget_earning9 = fields.Integer('予算_売上9月')
    budget_profit9 = fields.Integer('予算_粗利9月')
    achieve_earning9 = fields.Integer('実績_売上9月', readonly = True)
    achieve_profit9 = fields.Integer('実績_粗利9月', readonly = True)
    budget_earning10 = fields.Integer('予算_売上10月')
    budget_profit10 = fields.Integer('予算_粗利10月')
    achieve_earning10 = fields.Integer('実績_売上10月', readonly = True)
    achieve_profit10 = fields.Integer('実績_粗利10月', readonly = True)
    budget_earning11 = fields.Integer('予算_売上11月')
    budget_profit11 = fields.Integer('予算_粗利11月')
    achieve_earning11 = fields.Integer('実績_売上11月', readonly = True)
    achieve_profit11 = fields.Integer('実績_粗利11月', readonly = True)
    budget_earning12 = fields.Integer('予算_売上12月')
    budget_profit12 = fields.Integer('予算_粗利12月')
    achieve_earning12 = fields.Integer('実績_売上12月', readonly = True)
    achieve_profit12 = fields.Integer('実績_粗利12月', readonly = True)

    budget_earnings = fields.Integer('予算_売上合計', readonly = True, store = True, compute='_compute_budget_earning')
    budget_profits = fields.Integer('予算_粗利合計', readonly = True, store = True, compute='_compute_budget_profit')
    achieve_earnings = fields.Integer('実績_売上合計', readonly = True)
    achieve_profits = fields.Integer('実績_粗利合計', readonly = True)

    budget_expenses = fields.Integer('予算_諸費用')
    achieve_expenses = fields.Integer('実績_諸費用', readonly = True)

    _sql_constraints = [
        ('unique_department',
         'unique(department, budget_year)', 'department budget_year should be unique per bu!')]

    # 予算_売上合計　自動計算
    @api.depends('budget_earning1','budget_earning2','budget_earning3','budget_earning4',
                'budget_earning5','budget_earning6','budget_earning7','budget_earning8',
                'budget_earning9','budget_earning10','budget_earning11','budget_earning12') 
    def _compute_budget_earning(self):
        self.budget_earnings = (self.budget_earning1 + self.budget_earning2 + self.budget_earning3 
                            + self.budget_earning4 + self.budget_earning5 + self.budget_earning6 
                            + self.budget_earning7 + self.budget_earning8 + self.budget_earning9 
                            + self.budget_earning10 + self.budget_earning11 + self.budget_earning12)

    # 予算_粗利合計　自動計算
    @api.depends('budget_profit1','budget_profit2','budget_profit3','budget_profit4',
                'budget_profit5','budget_profit6','budget_profit7','budget_profit8',
                'budget_profit9','budget_profit10','budget_profit11','budget_profit12')
    def _compute_budget_profit(self):
        self.budget_profits = (self.budget_profit1 + self.budget_profit2 + self.budget_profit3 
                            + self.budget_profit4 + self.budget_profit5 + self.budget_profit6 
                            + self.budget_profit7 + self.budget_profit8 + self.budget_profit9 
                            + self.budget_profit10 + self.budget_profit11 + self.budget_profit12)
