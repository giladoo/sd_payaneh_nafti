# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
from datetime import timedelta
import jdatetime
from odoo.exceptions import ValidationError, UserError
import pytz
# #############################################################################
class SdPayanehNaftiReportOutgateDaily(models.TransientModel):
    _name = 'sd_payaneh_nafti.report.outgate_daily_report'
    _description = 'Outgate Daily Report'

    start_date = fields.Date(required=True, default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz'))) )
    calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
                                default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')

    # #############################################################################
    def outgate_daily_report(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        return self.env.ref('sd_payaneh_nafti.outgate_daily_report').report_action(self, data=data)


