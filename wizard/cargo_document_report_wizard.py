# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError

# #############################################################################
class SdPayanehNaftiReportCargoDocument(models.TransientModel):
    _name = 'sd_payaneh_nafti.report.cargo_document_report'
    _description = 'Cargo Document'


    document_no = fields.Many2one('sd_payaneh_nafti.input_info',required=True,)

    # start_date = fields.Date(required=True, default=lambda self: date.today() )
    calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
                                default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')

    # #############################################################################
    def cargo_document_report(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}
        # read_form.get("document_no")
        # docids = read_form.get("document_no")[0]
        docids = self.env['sd_payaneh_nafti.input_info'].browse(read_form.get("document_no")[0])
        print(f'=======================\n docids: {docids}')
        return self.env.ref('sd_payaneh_nafti.cargo_document_report').report_action(docids, data=data)


    # #############################################################################
    def cargo_document_html_report(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}
        # print(f'\n {read_form.get("calendar")}')
        return self.env.ref('sd_payaneh_nafti.cargo_document_html_report').report_action(self, data=data)

