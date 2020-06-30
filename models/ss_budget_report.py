# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SsBudgetReport(models.Model):
    _name = "ss.budget.report"
    _description = "Ss Budget Statistics"
    _auto = False

    # 予算年度を表示する
    budget_year = fields.Char(u'予算年度')

    # bu
    department = fields.Char(u'部門', readonly=True)
    department_cd = fields.Char(u'部門コード', readonly=True)
    department_name = fields.Char(u'部門名', readonly=True)

    budget_earnings = fields.Integer('予算_売上合計', readonly = True)
    budget_costs = fields.Integer('予算_原価合計', readonly = True)
    budget_charges = fields.Integer('予算_諸費用合計', readonly = True)
    budget_profits = fields.Integer('予算_粗利合計', readonly = True)
    budget_ratios = fields.Float('予算_総粗利率', readonly = True)
    achieve_earnings = fields.Integer('実績_売上合計', readonly = True)
    achieve_costs = fields.Integer('実績_原価合計', readonly = True)
    achieve_charges = fields.Integer('実績_諸費用合計', readonly = True)
    achieve_profits = fields.Integer('実績_粗利合計', readonly = True)
    achieve_ratios = fields.Float('実績_総粗利率', readonly = True)

    # # 実績
    # pj_order_id = fields.Many2one('ss.order', u'PJ要員')
    #
    # # 経理年月
    # pj_account_date = fields.Char(u'経理年月')
    # pj_long_date = fields.Date(u'経理年月')
    #
    # # PJ処理状態
    # pj_process = fields.Selection([
    #     ('new', u'処理待ち'),
    #     ('proc', u'処理中'),
    #     ('done', u'処理済'),
    # ], string='処理状態')
    #
    # pj_member_id = fields.Many2one('hr.employee', string=u'要員', readonly=True)
    # pj_member_cd = fields.Char(string='従業員コード', readonly=True)
    # pj_member_type = fields.Selection([
    #     ('employee', u'社員'),
    #     ('bp', u'BP'),
    #     ('personal', u'個人'),
    # ], string=u'要員区分', readonly=True)
    #
    # pj_id = fields.Many2one('ss.pj', string='PJ', readonly=True)
    # pj_cd = fields.Char(u'PJコード', readonly=True)
    # pj_name = fields.Char(u'PJ名', readonly=True)
    #
    # # BU
    # pj_bu_id = fields.Many2one('hr.department', u'BU', readonly=True)
    # pj_bu_cd = fields.Char(u'BUコード', readonly=True)
    # pj_bu_name = fields.Char(u'BU名', readonly=True)
    #
    # pj_partner_c_id = fields.Many2one('res.partner', u'顧客', readonly= True)
    # pj_partner_c_cd = fields.Char('顧客コード', readonly= True)
    # pj_partner_s_id = fields.Many2one('res.partner', u'仕入先', readonly= True)
    # pj_partner_s_cd = fields.Char('仕入先コード', readonly= True)
    #
    # # PJ粗利 粗利率
    # pj_o_profit = fields.Integer(string=u'粗利')
    # pj_o_profitrate = fields.Float(string=u'粗利率')
    #
    # ## Order 受注
    # pj_o_manhour = fields.Float(u'当月工数')
    # pj_o_duty_hours = fields.Float(u'当月時間')
    # pj_o_hours_lowerlimit = fields.Float(u'当月下限')
    # pj_o_hours_upperlimit = fields.Float(u'当月上限')
    # pj_o_payoffhour = fields.Float(u'精算時間')
    # pj_o_excess_deduct = fields.Integer(u'超過・控除')
    # pj_o_adjustment = fields.Integer(u'調整額')
    # pj_o_adjustment_comment = fields.Char(u'調整理由')
    #
    # # # 小計項目を追加する
    # pj_o_subtotal = fields.Integer(u'小計')
    # pj_o_tax = fields.Integer(u'消費税')
    # pj_o_carfare = fields.Integer(u'業務費用')
    #
    # pj_o_amount_subtotal = fields.Integer(u'売上合計', readonly=True)
    # pj_o_amount_inprogress = fields.Integer(u'仕掛品累計金額', readonly=True)

    #####################################################
    # def _select(self):
    #     select_str = """
    #         SELECT s.budget_year as budget_year,
    #                s.department as department,
    #                s.department_cd as department_cd,
    #                s.department_name as department_name,
    #                s.budget_earnings as budget_earnings,
    #                s.budget_costs as budget_costs,
    #                s.budget_charges as budget_charges,
    #                s.budget_profits as budget_profits,
    #                s.budget_ratios as budget_ratios
    #     """
    #     return select_str

    def _select(self):
        select_str = """
            SELECT s.*
        """
        return select_str

    def _from(self):
        from_str = """
            ss_budget s
        """
        return from_str

    def _group_by(self):
        group_by_str = """
        """
        return group_by_str

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT s.* 
            FROM ss_budget s )
            """ % (self._table))
