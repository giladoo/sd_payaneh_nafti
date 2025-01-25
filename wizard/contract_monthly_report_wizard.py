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
class SdPayanehNaftiReportContractMonthly(models.TransientModel):
    _name = 'sd_payaneh_nafti.report.contract_monthly_report'
    _description = 'Contract Monthly Report'

    month = fields.Selection(lambda self: gc.get_months_pr() if self.env.context.get('lang') == 'fa_IR' else gc.get_months(),
                             string='Month', required=True,
                             default=lambda self: self._month_selector())
    year = fields.Selection(lambda self: gc.get_years_pr() if self.env.context.get('lang') == 'fa_IR' else gc.get_years(),
                            string='Year', required=True,
                            default=lambda self: self._year_selector())
    days = fields.Selection(selection='_day_select')

    registration_no = fields.Many2one('sd_payaneh_nafti.contract_registration', required=True,
                                      domain=[('loading_type', '=', 'internal')])

    loading_type = fields.Selection([('internal', 'Internal'), ('export', 'Export')], default='internal', required=True)


    # start_date = fields.Date(required=True, default=lambda self: date.today() )
    # calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
    #                             default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')

    # #############################################################################

    # @api.onchange('year')
    def _day_select(self):
        lst = []
        if self.year == '1401':

            lst = [('a', 'A'), ]
        elif self.year == '1402':

            lst = [('a', 'A'), ('b', 'B'), ('c', 'C')]
        # print(f'\n+++++++++++++> _day_select lst: {lst}')
        return lst
    @api.onchange('year')
    def _day_select1(self):
        lst = []
        if self.year == '1401':

            lst = [('a', 'A'), ]
        elif self.year == '1402':

            lst = [('a', 'A'), ('b', 'B'), ('c', 'C')]
        # print(f'\n+++++++++++++>_day_select 1 lst: {lst}')
        return

    @api.onchange('registration_no')
    def _registration_no(self):
        pass



    @api.onchange('loading_type')
    def _reg_domain(self):
        domain = {}
        self.registration_no = False
        if self.loading_type == 'internal':
            domain = {'registration_no': [('loading_type', '=', 'internal')]}
        elif self.loading_type == 'export':
            domain = {'registration_no': [('loading_type', '=', 'export')]}
        return {'domain': domain}


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
