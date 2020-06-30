# -*- coding: utf-8 -*-
###############################################################################
#
#    MIRAIt Service Design Corp
#    Copyright (C) 2018-TODAY (<http://www.msdcorp.co.jp>).
#    Sales Support Management System
#
###############################################################################

from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError

class SsEmployee(models.Model):
    _inherit = "hr.employee"

    x_employee_cd = fields.Char('従業員コード', default='NEW', copy=False, index=True)
    x_kata = fields.Char('かたかな')
    x_member_type = fields.Selection([
        ('employee', u'社員'),
        ('bp', u'BP'),
        ('personal', u'個人'),
    ], string=u'要員区分')
    x_cost = fields.Integer('原価')

    # x_department_cd = fields.Char('部門コード')
    # hr.departmentのx_department_cdフィールドを取るため
    x_department_cd = fields.Char('部門コード', related='department_id.x_department_cd', store=True)
    x_department_name = fields.Char('部門名', related='department_id.name', readonly = True, store=True)
    x_partner_id = fields.Many2one('res.partner', u'仕入先', domain=[('supplier', '=', True)])
    x_partner_cd = fields.Char('仕入先コード', related='x_partner_id.x_partner_cd', readonly= True, store=True)
    x_kinmu_kubun = fields.Many2one('ss.kubun', '勤務区分')

    # PJ要員管理
    x_member_state = fields.Boolean(u'有効', Default=True)

    # 従業員IDを生成する
    # Company 処理追加　
    # 一括(XXX)の処理追加
    @api.multi
    def action_SetNewEmployeeCd(self):
        for record in self:
            if record.x_member_type == 'employee':
                if '一括' in record.name:
                    number = self.env['ir.sequence'].next_by_code('ss.employee.employee.yikatsu')
                else:
                    number = self.env['ir.sequence'].next_by_code('ss.employee.employee')
            elif record.x_member_type == 'bp':
                if '一括' in record.name:
                    number = self.env['ir.sequence'].next_by_code('ss.employee.bp.yikatsu')
                else:
                    number = self.env['ir.sequence'].next_by_code('ss.employee.bp')
            elif record.x_member_type == 'personal':
                number = self.env['ir.sequence'].next_by_code('ss.employee.personal')

            # 要員番号
            record.x_employee_cd = str(record.company_id.id) + '00-' + str(number).zfill(4)

    @api.constrains('x_employee_cd')
    def _check_employee_cd(self):
        for employee in self:
            if employee.x_employee_cd != 'NEW':
                # raise ValidationError(('要員採番してください。'))
                emp = self.env['hr.employee'].search(['&',('x_employee_cd','=', employee.x_employee_cd),('id','<>', employee.id)])
                if emp :
                    raise ValidationError(('要員コード重複エラー'))

    # 仕入先ID　仕入先CD
    # 社員or
    @api.constrains('x_partner_id')
    def _check_partner_id(self):
        for employee in self:
            if not employee.x_partner_cd:
                if (employee.x_member_type == 'employee' or employee.x_member_type == 'personal'):
                    employee.x_partner_cd = 'Z000'
                    partner = self.env['res.partner'].search([('x_partner_cd','=', employee.x_partner_cd)])
                    if partner:
                        employee.x_partner_id = partner.id
                else:
                    raise ValidationError(('仕入先を入力してください'))
