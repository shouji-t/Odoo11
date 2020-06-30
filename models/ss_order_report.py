# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SsOrderReport(models.Model):
    _name = "ss.order.report"
    _description = "Ss Order Statistics"
    _auto = False
    _rec_name = 'pj_member_id'
    _order = 'pj_member_id desc'




    #####################################################
    def _select(self):
        select_str = """
            SELECT s.id as id,
                   s.pj_cd as pj_cd,
                   s.pj_name as pj_name,
                   s.pj_note as pj_note,
                   s.pj_type as pj_type,
                   s.pj_user_id as pj_user_id,
                   s.pj_user_name as pj_user_name,
                   s.pj_bu_id as pj_bu_id,
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
                   o.pj_member_id as pj_member_id,
                   o.pj_member_cd as pj_member_cd,
                   o.pj_member_type as pj_member_type,
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
