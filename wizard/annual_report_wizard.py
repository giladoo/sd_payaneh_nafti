# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
import jdatetime
from . import get_calendare as gc
import pytz
# #############################################################################
class SdPayanehNaftiReportAnnual(models.TransientModel):
    _name = 'sd_payaneh_nafti.report.annual_report'
    _description = 'Annual Report'

    month_start = fields.Selection(lambda self: gc.get_months_pr() if self.env.context.get('lang') == 'fa_IR' else gc.get_months(),
                             string='Month', required=False,
                             default=lambda self: self._month_selector())
    year_start = fields.Selection(lambda self: gc.get_years_pr() if self.env.context.get('lang') == 'fa_IR' else gc.get_years(),
                            string='Year', required=False,
                            default=lambda self: self._year_selector())

    month = fields.Selection(lambda self: gc.get_months_pr() if self.env.context.get('lang') == 'fa_IR' else gc.get_months(),
                             string='Month', required=False,
                             default=lambda self: self._month_selector())
    year = fields.Selection(lambda self: gc.get_years_pr() if self.env.context.get('lang') == 'fa_IR' else gc.get_years(),
                            string='Year', required=True,
                            default=lambda self: self._year_selector())

    start_date = fields.Date(required=True, default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz'))) )
    calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
                                default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')

    # #############################################################################
    def annual_report(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        return self.env.ref('sd_payaneh_nafti.annual_report').report_action(self, data=data)
    # #############################################################################
    def annual_xls_report(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        return self.env.ref('sd_payaneh_nafti.annual_xls_report').report_action(self, data=data)


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
