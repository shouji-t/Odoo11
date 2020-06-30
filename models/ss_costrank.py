# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class SsCostRank(models.Model):
    _name = 'ss.costrank'
    _order = 'rank_cd'

    rank_cd = fields.Char(string='原価ランク')
    rank_cost = fields.Integer('原価')
    rank_note = fields.Char(string='注記')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.user.company_id.id)

