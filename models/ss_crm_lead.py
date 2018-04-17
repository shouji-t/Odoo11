# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = "crm.lead"

    x_location = fields.Char('場所')
    x_status = fields.Char('状況')
    x_skill = fields.Text('技術キーワード')
    x_period = fields.Char('期間')
    x_member = fields.Integer('要員数')
    x_saleprice = fields.Char('売価（万円）')
    x_purchaseprice = fields.Char('仕入（万円）')
