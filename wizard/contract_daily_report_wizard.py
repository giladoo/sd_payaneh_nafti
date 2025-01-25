# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
import pytz
# #############################################################################
class SdPayanehNaftiReportContractDaily(models.TransientModel):
    _name = 'sd_payaneh_nafti.report.contract_daily'
    _description = 'Contract Daily Report Wizard'

    registration_no = fields.Many2one('sd_payaneh_nafti.contract_registration', required=True,
                                      domain=[('loading_type', '=', 'internal')])

    loading_type = fields.Selection([('internal', 'Internal'), ('export', 'Export')], default='internal', required=True)

    # report_date = fields.Date(required=True, default=lambda self: datetime.strptime('2022-11-21', '%Y-%m-%d').date() )
    report_date = fields.Date(required=True, default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz'))) )

    calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
                                default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')
    payaneh_agent = fields.Char(required=True, default='payaneh_agent')
    observe_agent = fields.Char(required=True, default='observe_agent')
    buyer_agent = fields.Char(required=True, default='buyer_agent')
    # #############################################################################

    @api.onchange('loading_type','report_date')
    def _reg_domain(self):
        domain = {}
        self.registration_no = False
        # todo: only show the registrations that have a loading on that day
        # the_day_inputs = self.env['sd_payaneh_nafti.']
        if self.loading_type == 'internal':

            domain = {'registration_no': [('loading_type', '=', 'internal')]}
        elif self.loading_type == 'export':
            domain = {'registration_no': [('loading_type', '=', 'export')]}
        return {'domain': domain}

    def cargo_document_report(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}
        return self.env.ref('sd_payaneh_nafti.contract_daily_report').report_action(self, data=data)
    def cargo_document_xls_report(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}
        return self.env.ref('sd_payaneh_nafti.contract_daily_xls_report').report_action(self, data=data)

    # @api.depends('report_date')
    # @api.onchange('report_date')
    # def registration_default(self):
    #     regs = self.registration_no.search([('loading_date', '=', self.report_date)])
    #     return
