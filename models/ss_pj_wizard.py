from odoo import models, fields, api, exceptions
from calendar import monthrange
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class PjWizard(models.TransientModel):
    _name = 'ss.pj.wizard'
    pj_ids = fields.Many2many('ss.pj', string='PJs')
    pj_account_date = fields.Char(
        u'経理年月', compute='_compute_pj_account_date')
    pj_long_date = fields.Date(u'経理年月', required=True)

    @api.depends('pj_long_date')
    def _compute_pj_account_date(self):
        for record in self:
            if record.pj_long_date:
                # 月末を計算する　(閏年も含めて)
                stringDate = datetime.strptime(record.pj_long_date, '%Y-%m-%d')
                year = int(stringDate.strftime('%Y'))
                month = int(stringDate.strftime('%m'))
                last_day = str(monthrange(year, month)[1])
                record.pj_long_date = stringDate.strftime('%Y-%m-' + last_day)

    # フォーム初期値

    @api.model
    def default_get(self, field_names):
        defaults = super(PjWizard, self).default_get(field_names)
        defaults['pj_ids'] = self.env.context['active_ids']
        # for pj_id in defaults['pj_ids']:
        #     dates = []
        #     dates.append(self.env['ss.pj'].browse(pj_id).pj_startdate)
        #     _logger.info("records pj_startdate %s", dates)
        return defaults

    # 決定ボタン
    @api.multi
    def do_create(self):
        self.ensure_one()
        if not (self.pj_ids):
            raise exceptions.ValidationError('データがない')

        pj_order = self.env['ss.pj.order']
        pj_order_line = self.env['ss.pj.order.line']

        for pj_id in self.env.context['active_ids']:
            ss_pj = self.env['ss.pj'].browse(pj_id)

            # pj.orderのレコードを作成する
            created_pj_order = pj_order.create({'pj': pj_id,
                                                'pj_long_date': self.pj_long_date,
                                                'pj_cd': ss_pj.pj_cd,
                                                'pj_name': ss_pj.pj_name,
                                                'pj_type': ss_pj.pj_type,
                                                'pj_user_id': ss_pj.pj_user_id.id,
                                                'pj_register_date': ss_pj.pj_register_date,
                                                'pj_register_user_id': ss_pj.pj_register_user_id.id,
                                                'pj_permitted_date': ss_pj.pj_permitted_date,
                                                'pj_permitted_user_id': ss_pj.pj_permitted_user_id.id,
                                                'pj_closed_date': ss_pj.pj_closed_date,
                                                'pj_closed_user_id': ss_pj.pj_closed_user_id.id,
                                                'pj_bu_cd': ss_pj.pj_bu_cd.id,
                                                'pj_partner_id': ss_pj.pj_partner_id.id,
                                                'pj_partner_cd': ss_pj.pj_partner_cd,
                                                'pj_state': ss_pj.pj_state,
                                                'pj_startdate': ss_pj.pj_startdate,
                                                'pj_enddate': ss_pj.pj_enddate,
                                                'pj_total_months': ss_pj.pj_total_months,
                                                'pj_receipted_date': ss_pj.pj_receipted_date,
                                                'pj_receipted_user_id': ss_pj.pj_receipted_user_id.id,
                                                'pj_amount_total': ss_pj.pj_amount_total,
                                                'pj_cost_total': ss_pj.pj_cost_total,
                                                'pj_note': ss_pj.pj_note
                                                })
            _logger.info('pj_orderの作成 id: %s | PJコード: %s | 経理年月: %s',
                         created_pj_order.pj, created_pj_order.pj_cd, created_pj_order.pj_long_date)

            # pj.orderのlinesレコードを取る
            pj_lines = self.env['ss.pj.line'].search([('pj_id', '=', pj_id)])

            # pj.order.lineレコード作成する
            for pj_line in pj_lines:
                created_pj_order_line = pj_order_line.create({
                    'pj_order_id': created_pj_order.id,
                    'pj_id': pj_line.pj_id.id,
                    'sequence': pj_line.sequence,
                    'pj_member_id': pj_line.pj_member_id.id,
                    'pj_member_type': pj_line.pj_member_type,
                    'pj_price_type': pj_line.pj_price_type,
                    'pj_price_unit': pj_line.pj_price_unit,
                    'pj_price_purchase': pj_line.pj_price_purchase,
                    'pj_payofftype': pj_line.pj_payofftype,
                    'pj_fraction': pj_line.pj_fraction,
                    'pj_is_duty': pj_line.pj_is_duty,
                    'pj_normal_dutyhours': pj_line.pj_normal_dutyhours,
                    'pj_normal_hourlywage': pj_line.pj_normal_hourlywage,
                    'pj_duty_lowerlimit': pj_line.pj_duty_lowerlimit,
                    'pj_duty_upperlimit': pj_line.pj_duty_upperlimit,
                    'pj_price_lowerlimit': pj_line.pj_price_lowerlimit,
                    'pj_price_upperlimit': pj_line.pj_price_upperlimit,
                    'pj_manhour_contract': pj_line.pj_manhour_contract,
                    # ss.pj.order.lineフィールドを初期値にする
                    'pj_amount': pj_line.pj_amount,
                    'pj_cost': pj_line.pj_cost,
                    'pj_manhour': pj_line.pj_manhour_contract,
                    'pj_duty_hours': 0,
                    'pj_hours_lowerlimit': pj_line.pj_duty_lowerlimit,
                    'pj_hours_upperlimit': pj_line.pj_duty_upperlimit,
                    'pj_payoffhour': 0,
                    'pj_excess_deduct': 0,
                    'pj_adjustment': 0,
                    'pj_subtotal': 0,
                    'pj_tax': 0,
                    'pj_carfare': 0,
                    'pj_amount_subtotal': 0
                })
                _logger.info('pj_order_lineの作成 id: %s | pj_member_id: %s',
                             created_pj_order_line.pj_order_id, created_pj_order_line.pj_member_id)
