# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
import jdatetime
import pytz
from odoo.exceptions import ValidationError, UserError
from . import get_calendare as gc
# #############################################################################
class SdPayanehNaftiReportExportContractMonthly(models.TransientModel):
    _name = 'sd_payaneh_nafti.report.export_contract_monthly_report'
    _description = 'Export Contract Monthly Report'

    month = fields.Selection(lambda self: gc.get_months_pr() if self.env.context.get('lang') == 'fa_IR' else gc.get_months(),
                             string='Month', required=True,
                             default=lambda self: self._month_selector())
    year = fields.Selection(lambda self: gc.get_years_pr() if self.env.context.get('lang') == 'fa_IR' else gc.get_years(),
                            string='Year', required=True,
                            default=lambda self: self._year_selector())

    registration_no = fields.Many2one('sd_payaneh_nafti.contract_registration', required=True,
                                      domain=[('loading_type', '=', 'export')])

    # start_date = fields.Date(required=True, default=lambda self: date.today() )
    # calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
    #                             default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')

    # #############################################################################
    def contract_monthly_report(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        return self.env.ref('sd_payaneh_nafti.contract_monthly_report').report_action(self, data=data)

    def _year_selector(self):
        # todo: timezone is needed to make sure date after 8 pm is correct
        this_date = datetime.now(pytz.timezone(self.env.context.get('tz')))
        if self.env.context.get('lang') == 'fa_IR':
            s_this_year = jdatetime.date.fromgregorian(date=this_date).strftime("%Y")
        else:
            s_this_year = this_date.strftime("%Y")
        return s_this_year
    def _month_selector(self):
        # todo: timezone is needed to make sure date after 8 pm is correct
        this_date = datetime.now(pytz.timezone(self.env.context.get('tz')))
        if self.env.context.get('lang') == 'fa_IR':
            s_this_month = jdatetime.date.fromgregorian(date=this_date).strftime("%m")
        else:
            s_this_month = this_date.strftime("%m")
        return s_this_month
