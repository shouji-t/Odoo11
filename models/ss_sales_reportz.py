# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SsSalesReport(models.Model):
    _name = "ss.sales.reportz"
    _description = "Ss Sales Z"
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

    ## Purchase 発注
    pj_p_price_unit = fields.Integer(u'売価')
    pj_p_price_purchase = fields.Integer(u'原価')
    pj_p_manhour_contract = fields.Float(u'標準工数')
    pj_p_manhour = fields.Float(u'当月工数')
    pj_p_duty_hours = fields.Float(u'当月時間')
    pj_p_payoffhour = fields.Float(u'精算時間')
    pj_p_excess_deduct = fields.Integer(u'超過・控除')
    pj_p_adjustment = fields.Integer(u'調整額')

    # # 小計項目を追加する
    pj_p_subtotal = fields.Integer(u'小計')
    pj_p_tax = fields.Integer(u'消費税')
    pj_p_carfare = fields.Integer(u'業務費用')

    pj_p_amount_subtotal = fields.Integer(u'売上合計', readonly=True)
    pj_p_amount_inprogress = fields.Integer(u'仕掛品累計金額', readonly=True)

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
                   s.pj_p_price_type as pj_p_price_type,
                   s.pj_p_manhour_contract as pj_p_manhour_contract,
                   s.pj_p_manhour as pj_p_manhour,
                   s.pj_p_carfare as pj_p_carfare,
                   s.pj_p_excess_deduct as pj_p_excess_deduct,
                   s.pj_p_amount_subtotal as pj_p_amount_subtotal,
                   s.pj_p_amount_inprogress as pj_p_amount_inprogress
        """
        return select_str

    def _from(self):
        from_str = """
            ss_sales s
        """
        return from_str

    def _group_by(self):
        group_by_str = """
        """
        return group_by_str

    @api.model_cr
    def init(self):
        # self._table = sale_reportz
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT s.* 
            FROM ss_sales s WHERE pj_partner_s_cd > 'Z000')
            """ % (self._table))
