# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class SsBu(models.Model):
    _name = 'ss.bu'

    bu_id = fields.Char('部署ID')
    name = fields.Char('部署名称')

    #Ssbudget class Many2one - David Tang
    #１対多項目のため、目的モデルで正反対の多対１関係を実装する
    budget_ids = fields.One2many('ss.budget', 'bu_id', 'Budgets in this bu')

    _sql_constraints = [
        ('unique_bu_id',
         'unique(bu_id)', 'bu_id should be unique per bu!')]

    #選択リストにbu_idを表示させる
    @api.multi
    def name_get(self):
        result = []
        for bu in self:
            result.append((bu.id, bu.bu_id))
        return result
