# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError

# #############################################################################
class SdPayanehNaftiReportLoadingPermit(models.TransientModel):
    _name = 'sd_payaneh_nafti.report.loading_permit_report'
    _description = 'Loading Permit'


    document_no = fields.Many2one('sd_payaneh_nafti.input_info',required=True,)

    # start_date = fields.Date(required=True, default=lambda self: date.today() )
    calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
                                default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')

    # #############################################################################
    def loading_permit_report(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        return self.env.ref('sd_payaneh_nafti.loading_permit_report').report_action(self, data=data)

    # #############################################################################
    def loading_permit_html_report(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        return self.env.ref('sd_payaneh_nafti.loading_permit_html_report').report_action(self, data=data)


