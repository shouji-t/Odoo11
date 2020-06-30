# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    x_partner_cd = fields.Char('顧客コード', default='NEW', index=True)
    # x_shortname = fields.Char('略称')

    # SsPj class Many2one - David Tang
    # １対多項目のため、目的モデルで正反対の多対１関係を実装する
    #pj_ids = fields.One2many('ss.pj', 'partner_id', 'Pj')

    x_regdate = fields.Datetime('申請日', default=fields.Datetime.now, required=True)
    x_regstatus = fields.Selection([
        ('temp', u'仮'),
        ('regist', u'申請中'),
        ('process', u'処理中'),
        ('done', u'処理済'),
        ('cancel', u'廃棄')
    ], string='新規申請状態', default='temp')
    x_contract = fields.Boolean('契約書', default=False)
    x_order = fields.Boolean('注文書', default=False)
    x_purchase = fields.Boolean('発注書', default=False)
    x_edi = fields.Boolean('EDI', default=False)
    x_ediurl = fields.Char('EDIUrl')

# @api.constrains('x_partner_cd')
# def _check_partner_cd(self):
#  for record in self:
#      if record.x_partner_cd and  record.x_partner_cd:
#          raise ValidationError("コードが重複しております。")

    # 従業員IDを生成する
    @api.multi
    def action_SetNewPartnerCd(self):
        for record in self:
            if record.customer == 1:
                number = self.env['ir.sequence'].next_by_code('ss.partner.a')
                record.x_partner_cd = 'A' + str(number).zfill(3)
            elif record.supplier == 1:
                number = self.env['ir.sequence'].next_by_code('ss.partner.z')
                record.x_partner_cd = 'Z' + str(number).zfill(3)
