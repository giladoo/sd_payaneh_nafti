# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http


# ########################################################################################
class ReportSdPayanehNaftiLockerLogSheet(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.locker_log_sheet_template'
    _description = 'Locker Log Report'

    # ########################################################################################
    def get_report_values(self, docids, data=None):
        return self._get_report_values(docids, data)
    @api.model
    def _get_report_values(self, docids, data=None):
        print(f"\n >>>>> self: {self} docids: {docids} data: {data}")
        errors = []
        doc_data_list = []
        row_data_lines = []

        lang = self.env.context.get('lang')
        # form_data = data.get('form_data')
        # year = form_data.get('year')
        # month = form_data.get('month')
        #
        # if calendar == 'fa_IR':
        #     first_day = jdatetime.date(int(year), int(month), 1)
        #     next_month = first_day.replace(day=28) + timedelta(days=5)
        #     last_day = (next_month - timedelta(days=next_month.day)).togregorian()
        #     first_day = first_day.togregorian()
        #     s_first_day = jdatetime.date.fromgregorian(date=first_day).strftime("%Y/%m/%d")
        #     s_last_day = jdatetime.date.fromgregorian(date=last_day).strftime("%Y/%m/%d")
        #
        # else:
        #     date_format = '%Y-%m-%d'
        #     start_date = datetime.strptime(f'{year}-{month}-1', date_format).date()
        #     first_day = start_date.replace(day=1)
        #     next_month = first_day.replace(day=28) + timedelta(days=5)
        #     last_day = next_month - timedelta(days=next_month.day)
        #     s_first_day = first_day.strftime("%Y-%m-%d")
        #     s_last_day = last_day.strftime("%Y-%m-%d")

        locker_logs = self.env['sd_payaneh_nafti.locker_log'].browse(docids)
        data = {}
        for rec in locker_logs:
            issue_date = self.date_converter(rec.issue_date, lang)
            data[rec.id] = {'issue_date': issue_date['date']}



        # errors = ['test error']
        return {
            'docs': locker_logs if locker_logs else '',
            'data': data,
            'errors': errors,
            }

    # ########################################################################################
    def date_converter(self, date_time, lang):
        if lang == 'fa_IR':
            date_time = jdatetime.datetime.fromgregorian(datetime=date_time)
            date_time = {'date': date_time.strftime("%Y/%m/%d"),
                  'time': date_time.strftime("%H:%M:%S")}
        else:
            date_time = {'date': date_time.strftime("%Y/%m/%d"),
                        'time': date_time.strftime("%H:%M:%S")}
        return date_time

