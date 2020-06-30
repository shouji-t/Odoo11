# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class SsTax(models.Model):
    _name = 'ss.tax'
    _order = 'tax_date'

    tax_date = fields.Date('消費税改定日付')
    tax_rank = fields.Char('消費税ランク')
    tax_rate = fields.Float('消費税率' )

    # 消費税取得
    @api.model
    def _get_tax_rate(self, taxdate):
        if taxdate:
            tx = self.search([('tax_date','<', taxdate)], order='tax_date desc', limit=1)
            if tx:
                return tx.tax_rate / 100
            else:
                return 0.00

