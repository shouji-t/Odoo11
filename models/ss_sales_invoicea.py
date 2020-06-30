# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SsSalesInvoice(models.Model):
    _name = "ss.sales.invoicea"
    _description = "Ss Sales Invoice A"
    _auto = False

    id = fields.Integer('id')

    pj_order_id = fields.Many2one('ss.order', u'PJ要員')

    # 経理年月
    pj_account_date = fields.Char(u'経理年月')
    pj_long_date = fields.Date(u'経理年月')

    # PJ処理状態
    pj_process = fields.Selection([
        ('new', u'処理待ち'),
        ('proc', u'処理中'),
        ('done', u'処理済'),
    ], string='処理状態')

    pj_member_id = fields.Many2one('hr.employee', string=u'要員', readonly=True)
    pj_member_cd = fields.Char(string='従業員コード', readonly=True)
    pj_member_type = fields.Selection([
        ('employee', u'社員'),
        ('bp', u'BP'),
        ('personal', u'個人'),
    ], string=u'要員区分', readonly=True)

    pj_id = fields.Many2one('ss.pj', string='PJ', readonly=True)
    pj_cd = fields.Char(u'PJコード', readonly=True)
    pj_name = fields.Char(u'PJ名', readonly=True)

    # BU
    pj_bu_id = fields.Many2one('hr.department', u'BU', readonly=True)
    pj_bu_cd = fields.Char(u'部門コード', readonly=True)
    pj_bu_name = fields.Char(u'部門名', readonly=True)

    pj_partner_c_id = fields.Many2one('res.partner', u'顧客', readonly= True)
    pj_partner_c_cd = fields.Char('顧客コード', readonly= True)
    pj_partner_s_id = fields.Many2one('res.partner', u'仕入先', readonly= True)
    pj_partner_s_cd = fields.Char('仕入先コード', readonly= True)

    ## Order 受注
    pj_o_price_unit = fields.Integer(u'売価')
    pj_o_price_purchase = fields.Integer(u'原価')
    pj_o_manhour_contract = fields.Float(u'標準工数')
    pj_o_manhour = fields.Float(u'当月工数')
    pj_o_duty_hours = fields.Float(u'当月時間')
    pj_o_payoffhour = fields.Float(u'精算時間')
    pj_o_excess_deduct = fields.Integer(u'超過・控除')
    pj_o_adjustment = fields.Integer(u'調整額')

    # # 小計項目を追加する
    pj_o_subtotal = fields.Integer(u'小計')
    pj_o_tax = fields.Integer(u'消費税')
    pj_o_carfare = fields.Integer(u'業務費用')

    pj_o_amount_subtotal = fields.Integer(u'売上合計', readonly=True)
    pj_o_amount_inprogress = fields.Integer(u'仕掛品累計金額', readonly=True)

    pj_state = fields.Selection([
        ('wip', 'WIP'),
        ('done', 'Done'),
    ], default='wip')

    # pj_sales_order_count = fields.Integer(u'要員件数')
    x_edi = fields.Boolean('EDI')

    # pj_o_invoice_amount_subtotal = fields.Integer(u'合計金額', readonly=True, compute='_invoice_amount_all')
    # pj_invoice_pj_cd = fields.Char(u'PJコード', readonly=True, compute='invoice_pj_cd')

    # PJ合計金額
    # pj_o_invoice_amount_subtotal = fields.Integer(
    #     string=u'合計金額', readonly=True, compute='invoice_amount_all')

    #####################################################
    def _select(self):
        select_str = """
            SELECT s.id as id,
                   s.pj_order_id as pj_order_id,
                   s.pj_account_date as pj_account_date,
                   s.pj_long_date as pj_long_date,
                   s.pj_process as pj_process,
                   s.pj_member_id as pj_member_id,
                   s.pj_member_cd as pj_member_cd,
                   s.pj_member_type as pj_member_type,
                   s.pj_id as pj_id,
                   s.pj_cd as pj_cd,
                   s.pj_name as pj_name,
                   s.pj_bu_id as pj_bu_id,
                   s.pj_bu_cd as pj_bu_cd,
                   s.pj_bu_name as pj_bu_name,
                   s.pj_partner_id as pj_partner_id,
                   s.pj_partner_cd as pj_partner_cd,
                   s.pj_partner_s_id as pj_partner_s_id,
                   s.pj_partner_s_cd as pj_partner_s_cd,
                   s.pj_o_price_type as pj_o_price_type,
                   s.pj_o_manhour_contract as pj_o_manhour_contract,
                   s.pj_o_manhour as pj_o_manhour,
                   s.pj_o_carfare as pj_o_carfare,
                   s.pj_o_excess_deduct as pj_o_excess_deduct,
                   s.pj_o_amount_subtotal as pj_o_amount_subtotal,
                   s.pj_o_amount_inprogress as pj_o_amount_inprogress
                   s.pj_state as pj_state
        """
        return select_str

    def _from(self):
        from_str = """
            ss_sales s
        """
        return from_str

    # def _group_by(self):
    #     group_by_str = """
    #         s.pj_cd
    #     """
    #     return group_by_str

    # @api.model_cr
    # def init(self):
    #     # self._table = sale_invoicea
    #     tools.drop_view_if_exists(self.env.cr, self._table)
    #     self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
    #         SELECT
    #             ROW_NUMBER() OVER(ORDER BY pj_cd ASC) AS id,
    #             s.pj_cd AS pj_cd,
    #             s.pj_name AS pj_name,
    #             s.pj_account_date AS pj_account_date,
    #             s.pj_partner_c_id AS pj_partner_c_id,
    #             s.pj_process as pj_process,
    #             SUM(s.pj_o_manhour) AS pj_o_manhour,
    #             SUM(s.pj_o_duty_hours) AS pj_o_duty_hours,
    #             SUM(s.pj_o_payoffhour) AS pj_o_payoffhour,
    #             SUM(s.pj_o_excess_deduct) AS pj_o_excess_deduct,
    #             SUM(s.pj_o_carfare) AS pj_o_carfare,
    #             SUM(s.pj_o_amount_subtotal) AS pj_o_amount_subtotal,
    #             COUNT(*) AS pj_sales_order_count
    #         FROM
    #             ss_sales s
    #         WHERE
    #             pj_partner_c_id in (SELECT id FROM res_partner WHERE x_edi = False)
    #         GROUP BY
    #             pj_cd,
    #             pj_name,
    #             pj_account_date,
    #             pj_partner_c_id,
    #             pj_process )
    #         """ % (self._table))
    @api.model_cr
    def init(self):
        # self._table = sale_invoicea
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
                SELECT s.* 
                FROM ss_sales s )
                """ % (self._table))

    # #  フォーム合計の計算
    # # @api.depends('pj_o_amount_subtotal')
    # def invoice_amount_all(self):
    #     for pj in self:
    #         amount_untaxed = amount_tax = 0.0
    #         for line in pj.pj_order_id:
    #             amount_untaxed += line.pj_o_amount
    #         pj.update({
    #             'pj_o_invoice_amount_subtotal': amount_untaxed + amount_tax,
    #         })


