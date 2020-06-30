from odoo import models, fields, api, exceptions
from calendar import monthrange
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class SsSalesWizard(models.TransientModel):
    _name = 'ss.sales.wizard'
    pj_order_ids = fields.Many2many('ss.order', string='PJ要員')
    pj_account_date = fields.Char(u'経理年月', compute='_compute_pj_account_date')
    # pj_long_date = fields.Date(u'経理年月', required=True, default=datetime.datetime.today())
    pj_long_date = fields.Date(u'経理年月', required=True)

    @api.model_cr
    def init(self):
        for record in self:
            record.pj_long_date = datetime.datetime.today()
            self._compute_pj_account_date(self)

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
                record.pj_account_date = stringDate.strftime('%Y%m')

    # フォーム初期値
    @api.model
    def default_get(self, field_names):
        defaults = super(SsSalesWizard, self).default_get(field_names)
        defaults['pj_order_ids'] = self.env.context['active_ids']
        return defaults

    # 決定ボタン
    @api.multi
    def do_create(self):
        self.ensure_one()
        if not (self.pj_order_ids):
            raise exceptions.ValidationError('データがない')

        ss_sales = self.env['ss.sales']

        # for pj_order_id in self.env.context['active_ids']:
        for pj_order_id in self.pj_order_ids.ids:
            ss_id = self.env['ss.order'].browse(pj_order_id)

            # ss.salesのレコード2重作成チェック
            emp = False
            emp = ss_sales.search(['&',('pj_account_date','=', self.pj_account_date),
                                   '&',('pj_order_id','=', ss_id.id),('pj_cd','=', ss_id.pj_cd)])
            if emp:
                raise exceptions.ValidationError(('2重作成エラー! (') + ss_id.pj_member_cd + ' / ' + self.pj_account_date + ')')

            # ss.salesのレコードを作成する
            created_ss_sales = ss_sales.create({'pj_order_id': ss_id.id,
                                                'pj_long_date': self.pj_long_date,
                                                'pj_account_date': self.pj_account_date,
                                                'pj_process': 'new',
                                                'pj_o_member_orderno': ss_id.pj_o_member_orderno,
                                                'pj_o_member_orderdatefrom': ss_id.pj_o_member_orderdatefrom,
                                                'pj_o_member_orderdateto': ss_id.pj_o_member_orderdateto,
                                                'pj_o_member_orderdateto_forecase': ss_id.pj_o_member_orderdateto_forecase,
                                                'pj_o_member_orderamount': ss_id.pj_o_member_orderamount,
                                                'pj_o_price_type': ss_id.pj_o_price_type,
                                                'pj_o_price_unit': ss_id.pj_o_price_unit,
                                                'pj_o_price_purchase': ss_id.pj_o_price_purchase,
                                                'pj_o_payofftype': ss_id.pj_o_payofftype,
                                                'pj_o_normal_dutyhours': ss_id.pj_o_normal_dutyhours,
                                                'pj_o_normal_hourlywage': ss_id.pj_o_normal_hourlywage,
                                                'pj_o_is_duty': ss_id.pj_o_is_duty,
                                                'pj_o_duty_lowerlimit': ss_id.pj_o_duty_lowerlimit,
                                                'pj_o_duty_upperlimit': ss_id.pj_o_duty_upperlimit,
                                                'pj_o_price_lowerlimit': ss_id.pj_o_price_lowerlimit,
                                                'pj_o_price_upperlimit': ss_id.pj_o_price_upperlimit,
                                                'pj_o_manhour_contract': ss_id.pj_o_manhour_contract,
                                                'pj_o_amount': ss_id.pj_o_amount,
                                                'pj_o_cost': ss_id.pj_o_cost,
                                                'pj_o_profit': ss_id.pj_o_profit,
                                                'pj_o_profitrate': ss_id.pj_o_profitrate,
                                                'pj_o_manhour': ss_id.pj_o_manhour_contract,
                                                'pj_o_duty_hours': 0,
                                                'pj_o_hours_lowerlimit': ss_id.pj_o_duty_lowerlimit,
                                                'pj_o_hours_upperlimit': ss_id.pj_o_duty_upperlimit,
                                                'pj_o_payoffhour': 0,
                                                'pj_o_excess_deduct': 0,
                                                'pj_o_adjustment': 0,
                                                'pj_o_member_orderisprogress': ss_id.pj_o_member_orderisprogress,
                                                'pj_o_member_orderdateaccpt': ss_id.pj_o_member_orderdateaccpt,
                                                'pj_o_amount_inprogress': 0,
                                                'pj_o_subtotal': 0,
                                                'pj_o_tax': 0,
                                                'pj_o_carfare': 0,
                                                'pj_p_amount_subtotal': 0,
                                                'pj_p_member_orderno': ss_id.pj_p_member_orderno,
                                                'pj_p_member_orderdatefrom': ss_id.pj_p_member_orderdatefrom,
                                                'pj_p_member_orderdateto': ss_id.pj_p_member_orderdateto,
                                                'pj_p_member_orderdateto_forecase': ss_id.pj_p_member_orderdateto_forecase,
                                                'pj_p_member_orderamount': ss_id.pj_p_member_orderamount,
                                                'pj_p_price_type': ss_id.pj_p_price_type,
                                                'pj_p_price_unit': ss_id.pj_p_price_unit,
                                                'pj_p_price_purchase': ss_id.pj_p_price_purchase,
                                                'pj_p_payofftype': ss_id.pj_p_payofftype,
                                                'pj_p_normal_dutyhours': ss_id.pj_p_normal_dutyhours,
                                                'pj_p_normal_hourlywage': ss_id.pj_p_normal_hourlywage,
                                                'pj_p_is_duty': ss_id.pj_p_is_duty,
                                                'pj_p_duty_lowerlimit': ss_id.pj_p_duty_lowerlimit,
                                                'pj_p_duty_upperlimit': ss_id.pj_p_duty_upperlimit,
                                                'pj_p_price_lowerlimit': ss_id.pj_p_price_lowerlimit,
                                                'pj_p_price_upperlimit': ss_id.pj_p_price_upperlimit,
                                                'pj_p_manhour_contract': ss_id.pj_p_manhour_contract,
                                                'pj_p_amount': ss_id.pj_p_amount,
                                                'pj_p_cost': ss_id.pj_p_amount,
                                                'pj_p_duty_hours': 0,
                                                'pj_p_hours_lowerlimit': ss_id.pj_p_duty_lowerlimit,
                                                'pj_p_hours_upperlimit': ss_id.pj_p_duty_upperlimit,
                                                'pj_p_payoffhour': 0,
                                                'pj_p_excess_deduct': 0,
                                                'pj_p_adjustment': 0,
                                                'pj_p_subtotal': 0,
                                                'pj_p_tax': 0,
                                                'pj_p_carfare': 0,
                                                'pj_p_amount_subtotal': 0,
                                                'pj_p_amount_inprogress': 0,
                                                'pj_p_member_orderisprogress': ss_id.pj_p_member_orderisprogress,
                                                'pj_p_member_orderdateaccpt': ss_id.pj_p_member_orderdateaccpt
                                                })

