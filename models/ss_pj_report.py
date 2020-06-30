# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SsPjReport(models.Model):
    _name = "ss.pj.report"
    _description = "Ss Pj Statistics"
    _auto = False
    _rec_name = 'pj_cd'
    _order = 'pj_cd desc'

    # PJIDと名前
    id = fields.Integer('id')
    pj_cd = fields.Char(u'PJコード', readonly=True)
    pj_name = fields.Char(u'PJ名', readonly=True)

    active = fields.Boolean('Active', readonly=True)

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
    ], string=u'種別', readonly=True)

    # PJ担当者
    pj_user_id = fields.Many2one('res.users', string='PJ担当者', readonly=True)
    pj_user_name = fields.Char(u'PJ担当者名', readonly=True)
    pj_bu_id = fields.Many2one('hr.department', u'BU_id', readonly=True)
    pj_bu_cd = fields.Char(u'部門コード', readonly=True)
    pj_bu_name = fields.Char(u'部門名', readonly=True)

    pj_partner_c_id = fields.Many2one('res.partner', u'顧客', readonly= True)
    pj_partner_c_cd = fields.Char('顧客コード', readonly= True)
    pj_partner_s_id = fields.Many2one('res.partner', u'仕入先', readonly= True)
    pj_partner_s_cd = fields.Char('仕入先コード', readonly= True)

    # PJ管理
    pj_state = fields.Selection([
        ('new', u'新規'),
        ('run', u'稼働中'),
        ('cancel', u'終止'),
        ('end', u'終了'),
    ], string='稼働状態', readonly=True)
    #
    pj_startdate = fields.Date(u'PJ開始日', readonly=True)
    pj_enddate = fields.Date(u'PJ予定終了日', readonly=True)

    pj_amount_total = fields.Integer(string=u'合計金額', readonly=True)
    pj_cost_total = fields.Integer(string=u'原価金額', readonly=True)
    pj_profit_total = fields.Integer(string=u'粗利', readonly=True)
    pj_profitrate_total = fields.Float(string=u'粗利率', readonly=True)
    pj_note = fields.Text(u'備考', readonly=True)
    pj_amount = fields.Integer(u'売上', readonly=True)
    #

    pj_member_id = fields.Many2one('hr.employee', string=u'要員', readonly=True)
    pj_member_cd = fields.Char(string='従業員コード', readonly=True)
    pj_member_type = fields.Selection([
        ('employee', u'社員'),
        ('bp', u'BP'),
        ('personal', u'個人'),
    ], string=u'要員区分')
    pj_o_price_type = fields.Selection([
        ('month', u'月給'),
        ('hour', u'時給'),
    ], string=u'単価区分', default='month', required=True)
    # pj_price_unit = fields.Integer(u'売価', readonly=True)
    # pj_price_purchase = fields.Integer(u'原価', readonly=True)
    # pj_payofftype = fields.Selection([
    #     ('fix', u'固定'),
    #     ('updown', u'上下割'),
    #     ('middle', u'中間割'),
    # ], string=u'精算条件', readonly=True)
    # pj_fraction = fields.Selection([
    #     ('truncation', u'切り捨て'),
    #     ('roundedup', u'切り上げ'),
    # ], string=u'端数計算', readonly=True)
    # pj_normal_dutyhours = fields.Integer(u'標準時数', readonly=True)
    # pj_is_duty = fields.Boolean(u'精算', readonly=True)
    # pj_duty_lowerlimit = fields.Integer(u'精算下限', readonly=True)
    # pj_duty_upperlimit = fields.Integer(u'精算上限', readonly=True)
    # pj_price_lowerlimit = fields.Integer(u'下限単価', readonly=True)
    # pj_price_upperlimit = fields.Integer(u'上限単価', readonly=True)
    # pj_manhour_contract = fields.Float(u'標準工数', default=1)
    # pj_amount = fields.Integer(u'売上', compute='_compute_pj_amount', readonly=True)
    # pj_cost = fields.Integer(u'原価', compute='_compute_pj_cost', readonly=True)
    # pj_profit = fields.Integer(string=u'粗利', readonly=True)
    # pj_profitrate = fields.Float(string=u'粗利率', readonly=True)

    #####################################################
    def _select(self):
        select_str = """
            SELECT s.id as id,
                   s.pj_cd as pj_cd,
                   s.pj_name as pj_name,
                   s.active as active,
                   s.pj_note as pj_note,
                   s.pj_type as pj_type,
                   s.pj_user_id as pj_user_id,
                   s.pj_user_name as pj_user_name,
                   s.pj_bu_id as pj_bu_id,
                   s.pj_bu_cd as pj_bu_cd,
                   s.pj_bu_name as pj_bu_name,
                   s.pj_partner_id as pj_partner_c_id,
                   s.pj_partner_cd as pj_partner_c_cd,
                   s.pj_state as pj_state,
                   s.pj_startdate as pj_startdate,
                   s.pj_enddate as pj_enddate,
                   s.pj_amount_total as pj_amount_total,
                   s.pj_cost_total as pj_cost_total,
                   s.pj_profit as pj_profit_total,
                   s.pj_profitrate as pj_profitrate_total,
                   o.pj_member_id as pj_member_id,
                   o.pj_member_cd as pj_member_cd,
                   o.pj_member_type as pj_member_type,
                   o.pj_partner_s_id as pj_partner_s_id,
                   o.pj_partner_s_cd as pj_partner_s_cd,
                   o.pj_o_price_type as pj_o_price_type,
                   o.pj_o_duty_lowerlimit as pj_o_duty_lowerlimit,
                   o.pj_o_duty_upperlimit as pj_o_duty_upperlimit,
                   o.pj_o_price_lowerlimit as pj_o_price_lowerlimit,
                   o.pj_o_price_upperlimit as pj_o_price_upperlimit,
                   o.pj_o_manhour_contract as pj_o_manhour_contract,
                   o.pj_o_amount as pj_amount
        """
        return select_str

    def _from(self):
        from_str = """
            ss_pj as s
                join ss_order as o on(s.id = o.pj_id)
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
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))
#
# class SaleOrderReportProforma(models.AbstractModel):
#     _name = 'report.sale.report_saleproforma'
#
#     @api.multi
#     def get_report_values(self, docids, data=None):
#         docs = self.env['sale.order'].browse(docids)
#         return {
#             'doc_ids': docs.ids,
#             'doc_model': 'sale.order',
#             'docs': docs,
#             'proforma': True
#         }
