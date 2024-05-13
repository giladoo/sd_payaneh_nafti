# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http


# ########################################################################################
class ReportSdPayanehNaftiannual(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.annual_report_template'
    _description = 'annual Report'

    month_list = [('01', 'فروردین'), ('02', 'اردیبهشت'), ('03', 'خرداد'), ('04', 'تیر'),
     ('05', 'مرداد'), ('06', 'شهریور'), ('07', 'مهر'), ('08', 'آبان'),
     ('09', 'آذر'), ('10', 'دی'), ('11', 'بهمن'), ('12', 'اسفند'), ]
    # ########################################################################################
    def get_report_values(self, docids, data=None):
        return self._get_report_values(docids, data)
    @api.model
    def _get_report_values(self, docids, data=None):
        errors = []
        doc_data_list = []
        row_data_lines = []
        # context = self.env.context
        # time_z = pytz.timezone(context.get('tz'))
        # date_time = datetime.now(time_z)
        # date_time = self.date_converter(date_time, context.get('lang'))

        calendar = self.env.context.get('lang')
        form_data = data.get('form_data')
        year = form_data.get('year')
        month = form_data.get('month')

        if calendar == 'fa_IR':
            first_day = jdatetime.date(int(year), 1, 1)
            next_year = jdatetime.date(int(year) + 1, 1, 1)
            last_day = (next_year - timedelta(days=1)).togregorian()
            first_day = first_day.togregorian()
            s_first_day = jdatetime.date.fromgregorian(date=first_day).strftime("%Y/%m/%d")
            s_last_day = jdatetime.date.fromgregorian(date=last_day).strftime("%Y/%m/%d")

        else:
            # todo: needs to calculate
            date_format = '%Y-%m-%d'
            start_date = datetime.strptime(f'{year}-{month}-1', date_format).date()
            first_day = start_date.replace(day=1)
            next_month = first_day.replace(day=28) + timedelta(days=5)
            last_day = next_month - timedelta(days=next_month.day)
            s_first_day = first_day.strftime("%Y-%m-%d")
            s_last_day = last_day.strftime("%Y-%m-%d")


        month_s_1, month_e_1 = self.month_start_end(last_day, -11, calendar)
        month_s_2, month_e_2 = self.month_start_end(last_day, -10, calendar)
        month_s_3, month_e_3 = self.month_start_end(last_day, -9, calendar)
        month_s_4, month_e_4 = self.month_start_end(last_day, -8, calendar)
        month_s_5, month_e_5 = self.month_start_end(last_day, -7, calendar)
        month_s_6, month_e_6 = self.month_start_end(last_day, -6, calendar)
        month_s_7, month_e_7 = self.month_start_end(last_day, -5, calendar)
        month_s_8, month_e_8 = self.month_start_end(last_day, -4, calendar)
        month_s_9, month_e_9 = self.month_start_end(last_day, -3, calendar)
        month_s_10, month_e_10 = self.month_start_end(last_day, -2, calendar)
        month_s_11, month_e_11 = self.month_start_end(last_day, -1, calendar)
        month_s_12, month_e_12 = self.month_start_end(last_day, 0, calendar)

        # print(f'==========>\n month_s_1: {month_s_1} month_e_1: {month_e_1} ')
        # print(f'==========>\n month_s_1: {month_s_2} month_e_1: {month_e_2} ')

        month_list_names = list([rec[1] for rec in self.month_list])

        input_records = self.env['sd_payaneh_nafti.input_info'].search([('loading_date', '>=', first_day),
                                                                        ('loading_date', '<=', last_day)])
        if len(input_records) == 0:
            return{
                'errors': [_(f'No record have found for selected time duration: {s_first_day} to {s_last_day}')],
                }
        docids = [input_records.ids]

        input_records_1 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_1 and rec.loading_date <= month_e_1])
        input_records_2 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_2 and rec.loading_date <= month_e_2])
        input_records_3 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_3 and rec.loading_date <= month_e_3])
        input_records_4 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_4 and rec.loading_date <= month_e_4])
        input_records_5 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_5 and rec.loading_date <= month_e_5])
        input_records_6 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_6 and rec.loading_date <= month_e_6])
        input_records_7 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_7 and rec.loading_date <= month_e_7])
        input_records_8 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_8 and rec.loading_date <= month_e_8])
        input_records_9 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_9 and rec.loading_date <= month_e_9])
        input_records_10 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_10 and rec.loading_date <= month_e_10])
        input_records_11 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_11 and rec.loading_date <= month_e_11])
        input_records_12 = list([rec for rec in input_records
                                if rec.loading_date >= month_s_12 and rec.loading_date <= month_e_12])
        input_records_months = [(month_list_names[0], input_records_1),
                                (month_list_names[1], input_records_2),
                                (month_list_names[2], input_records_3),
                                (month_list_names[3], input_records_4),
                                (month_list_names[4], input_records_5),
                                (month_list_names[5], input_records_6),
                                (month_list_names[6], input_records_7),
                                (month_list_names[7], input_records_8),
                                (month_list_names[8], input_records_9),
                                (month_list_names[9], input_records_10),
                                (month_list_names[10], input_records_11),
                                (month_list_names[11], input_records_12),
                                ]
        table_data = []
        for month, input_record in input_records_months:
            final_mt = round(sum([int(rec.final_mt) for rec in input_record]))
            final_gsv_b = round(sum([int(rec.final_gsv_b) for rec in input_record]))


            table_data.append({'month': month,
                               'final_gsv_b': final_gsv_b,
                               'final_mt': final_mt,
                                'trucks': len(input_record),
                                })

        final_gsv_b_total = sum(list([rec['final_gsv_b'] for rec in table_data]))
        final_mt_total = sum(list([rec['final_mt'] for rec in table_data]))
        trucks_total = sum(list([rec['trucks'] for rec in table_data]))


        company_logo = f'/web/image/res.partner/{1}/image_128/'
        doc_data_list = [('', '')]
        # errors = ['test error']
        return {
            'docs': input_records[0] if input_records else '',
            'doc_ids': docids,
            'table_data': table_data,
            'final_gsv_b_total': final_gsv_b_total,
            'final_mt_total': final_mt_total,
            'trucks_total': trucks_total,
            'doc_model': 'sd_payaneh_nafti.input_info',
            # 'document_no': document_no,
            'doc_data_list': doc_data_list,
            'row_data_lines': row_data_lines,
            'dates': [s_first_day, s_last_day],
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

    # ########################################################################################
    def type_name(self, data, calendar):
        if calendar == 'fa_IR':
            if data == 'stock':
                r = 'بورس'
            elif data == 'general':
                r = 'عمومی'
            elif data == 'internal':
                r = 'داخلی'
            elif data == 'export':
                r = 'صادراتی'
            elif data == 'barrel':
                r = 'بشکه'
            elif data == 'metric_ton':
                r = 'متریک تن'
            else:
                r = ''
        else:
            if data == 'stock':
                r = 'Stock'
            elif data == 'general':
                r = 'General'
            elif data == 'internal':
                r = 'Internal'
            elif data == 'export':
                r = 'Export'
            elif data == 'barrel':
                r = 'Barrel'
            elif data == 'metric_ton':
                r = 'Metric Ton'
            else:
                r = ''
        return r






    # ########################################################################################
    def _table_record(self, items, start_date, first_day, last_day, record_type=False):
        day = len(list([item for item in items
                        if (not record_type or item.record_type.name == record_type)
                        and item.record_date == start_date]))

        month = len(list([item for item in items
                          if (not record_type or item.record_type.name == record_type)
                          and item.record_date <= start_date
                          and item.record_date >= first_day ]))

        total = len(list([item for item in items if (not record_type or item.record_type.name == record_type)]))
        return day, month, total

    # ########################################################################################
    def _table_record_sum_of_records(self, items, start_date, first_day, last_day, record_type=False):
        day = sum(list([item.man_hours for item in items
                        if (not record_type or item.record_type.name == record_type)
                        and item.record_date == start_date]))

        month = sum(list([item.man_hours for item in items
                          if (not record_type or item.record_type.name == record_type)
                          and item.record_date <= start_date
                          and item.record_date >= first_day ]))

        total = sum(list([item.man_hours for item in items if (not record_type or item.record_type.name == record_type)]))
        day = int(round(day, 0))
        month = int(round(month, 0))
        total = int(round(total, 0))
        return day, month, total


    def month_start_end(self, this_date, month=0, calendar='fa_IR'):
        format = "%Y/%m/%d"
        # this_date = datetime.now()
        if calendar == 'fa_IR':
            month_delta = month if month < 0 or month > -60 else 0
            first_day_j = jdatetime.date.fromgregorian(date=this_date).replace(day=1)

            year_j = first_day_j.year
            month_j = first_day_j.month

            if month_j + month_delta > 0:
                month = month_j + month_delta
                year = year_j

            elif month_j + month_delta <= -60:
                month = month_j + month_delta + 72
                year = year_j - 6

            elif month_j + month_delta <= -48:
                month = month_j + month_delta + 60
                year = year_j - 5

            elif month_j + month_delta <= -36:
                month = month_j + month_delta + 48
                year = year_j - 4

            elif month_j + month_delta <= -24:
                month = month_j + month_delta + 36
                year = year_j - 3

            elif month_j + month_delta <= -12:
                month = month_j + month_delta + 24
                year = year_j - 2

            elif month_j + month_delta <= 0:
                month = month_j + month_delta + 12
                year = year_j - 1

            first_day_j = jdatetime.date(day=1, month=month, year=year)
            the_prev_month_j = first_day_j.replace(day=28) + timedelta(days=8)
            the_prev_month = the_prev_month_j.togregorian()

            first_p_day_j = jdatetime.date.fromgregorian(date=the_prev_month).replace(day=1)

            next_month = first_day_j.replace(day=28) + timedelta(days=8)
            last_day_j = (next_month - timedelta(days=next_month.day))
            last_day = last_day_j.togregorian()
            first_day = first_day_j.togregorian()

        else:
            first_day = this_date.replace(day=1)
            next_month = first_day.replace(day=28) + timedelta(days=5)
            last_day = next_month - timedelta(days=next_month.day)
            format = "%Y-%m-%d"

        return (first_day, last_day)


