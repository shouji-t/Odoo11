# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SsPjOrderReport(models.Model):
    _name = "ss.pj.order.report"
    _description = "Ss Pj Statistics"
    _auto = False
    _rec_name = 'pj_cd'
    _order = 'pj_cd desc'
    _inherit = "ss.pj.report"

    pj = fields.Many2one('ss.pj', u'pj', readonly=True)
    pj_amount_total = fields.Integer(readonly=True)

    # 経理年月
    pj_account_date = fields.Char(u'経理年月', readonly=True)
    pj_order_id = fields.Many2one('ss.pj.order', string='PJ Order Reference', readonly=True)

    pj_manhour = fields.Float(u'当月工数', readonly=True)
    pj_duty_hours = fields.Float(u'当月時間', readonly=True)
    pj_payoffhour = fields.Float(u'精算時間', readonly=True)
    pj_excess_deduct = fields.Integer(u'超過・控除', readonly=True)
    pj_adjustment = fields.Integer(u'調整額', readonly=True)

    # # 小計項目を追加する
    pj_subtotal = fields.Integer(u'小計', readonly=True)
    pj_tax = fields.Integer(u'消費税', readonly=True)

    pj_carfare = fields.Integer(u'業務費用', readonly=True)
    pj_amount_subtotal = fields.Integer(u'売上合計', readonly=True)

    #####################################################
    def _select(self):
        select_str = """
            SELECT s.id as id,
                   s.pj_account_date as pj_account_date,
                   s.pj_cd as pj_cd,
                   s.pj_name as pj_name,
                   s.pj_type as pj_type,
                   s.pj_user_id as pj_user_id,
                   s.pj_bu_cd as pj_bu_cd,
                   s.pj_bu_name as pj_bu_name,
                   s.pj_partner_id as pj_partner_id,
                   s.pj_partner_cd as pj_partner_cd,
                   s.pj_state as pj_state,
                   s.pj_startdate as pj_startdate,
                   s.pj_enddate as pj_enddate,
                   s.pj_amount_total as pj_amount_total,
                   s.pj_cost_total as pj_cost_total,
                   s.pj_profit as pj_profit_total,
                   s.pj_profitrate as pj_profitrate_total,

                   l.pj_member_id as pj_member_id,
                   l.pj_member_type as pj_member_type,
                   l.pj_price_type as pj_price_type,
                   l.pj_price_unit as pj_price_unit,
                   l.pj_price_purchase as pj_price_purchase,
                   l.pj_payofftype as pj_payofftype,
                   l.pj_normal_dutyhours as pj_normal_dutyhours,
                   l.pj_manhour_contract as pj_manhour_contract,
                   l.pj_amount as pj_amount,
                   l.pj_cost as pj_cost,
                   l.pj_profit as pj_profit,
                   l.pj_profitrate as pj_profitrate,

                   l.pj_manhour as pj_manhour,
                   l.pj_duty_hours as pj_duty_hours,
                   l.pj_payoffhour as pj_payoffhour,
                   l.pj_excess_deduct as pj_excess_deduct,
                   l.pj_adjustment as pj_adjustment,
                   l.pj_subtotal as pj_subtotal,
                   l.pj_tax as pj_tax,
                   l.pj_carfare as pj_carfare,
                   l.pj_amount_subtotal as pj_amount_subtotal
        """
        return select_str

    def _from(self):
        from_str = """
            ss_pj_order_line l
                  join ss_pj_order s on (l.pj_id=s.id)
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
