# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http
import logging
import json


# ########################################################################################
class ReportSdPayanehNaftiMeterReport(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.meter_report_template'
    _description = 'Meter Report'

    # ########################################################################################
    def get_report_values(self, docids=None, data=None):
        return self._get_report_values(docids, data)

    # ########################################################################################
    @api.model
    def _get_report_values(self, docids, data=None):
        errors = []
        context = self.env.context
        calendar = context.get('lang')

        time_z = pytz.timezone(context.get('tz'))
        date_time = datetime.now(time_z)
        date_time = self.date_converter(date_time, context.get('lang'))
        form_data = data.get('form_data')
        date_format = '%Y-%m-%d'
        meter_report_date = form_data.get('meter_report_date')
        meter_comment = form_data.get('meter_comment')
        meter_report_date = datetime.strptime(meter_report_date, date_format).date()
        # meter_data = self.env['sd_payaneh_nafti.meter_data'].search([('report_date', '=', start_date)], order='meter')
        if calendar == 'fa_IR':
            s_start_date = jdatetime.date.fromgregorian(date=meter_report_date).strftime("%Y/%m/%d")
        else:
            s_start_date = meter_report_date.strftime("%Y/%m/%d")

        this_date_input = self.env['sd_payaneh_nafti.input_info'].search(
            [('loading_info_date', '=', meter_report_date), ('state', 'in', ['done', 'finished']), ])
        if len(this_date_input) == 0:
            return {
                'errors': [_(f'No record have found for selected date: {s_start_date} ')],
            }
        # for rec in this_date_input:
            # print(f'{rec.document_no} : {rec.totalizer_difference}    meter: {rec.meter_no}')

        meter_no_list = ['1', '2', '3', '4', '5', '6', '7', '8', '0']
        meter_data = []
        meter_inputs = []
        meter_amount_sum = 0
        truck_count_sum = 0
        meter_data_inputs = list(filter(lambda r: r.weighbridge == 'no', this_date_input))
        for meter_no in meter_no_list:
            meter_inputs.append((meter_no, sorted(list([ii for ii in meter_data_inputs if ii.meter_no == meter_no]),
                                                  key=lambda i: i.totalizer_start)))
            truck_count = len(list([ii.totalizer_start for ii in meter_data_inputs if ii.meter_no == meter_no]))
            truck_count_sum = truck_count_sum + truck_count
            totalizer_start = sorted(list([ii.totalizer_start for ii in meter_data_inputs if ii.meter_no == meter_no]))
            totalizer_end = sorted(list([ii.totalizer_end for ii in meter_data_inputs if ii.meter_no == meter_no]))
            first_totalizer = min(totalizer_start) if totalizer_start else 0
            last_totalizer = max(totalizer_end) if totalizer_end else 0
            meter_amounts = last_totalizer - first_totalizer
            meter_amount_sum = meter_amount_sum + meter_amounts
            data = {'meter_no': int(meter_no),
                    'first_totalizer': first_totalizer,
                    'last_totalizer': last_totalizer,
                    'meter_amounts': meter_amounts,
                    'truck_count': truck_count,
                    }
            meter_data.append(data)

        totalizer_weighbridge = list([t for t in this_date_input if t.weighbridge == 'yes'])
        totalizer_weighbridge = sorted(totalizer_weighbridge, key=lambda r: (r.meter_no, r.totalizer_start))
        totalizer_weighbridge_count = len(totalizer_weighbridge)
        totalizer_weighbridge_sum = sum(list([r.totalizer_difference for r in totalizer_weighbridge]))
        totalizer_sum = sum(list([t.totalizer_difference for t in this_date_input]))

        metre_weighbridget_deff = meter_amount_sum + totalizer_weighbridge_sum - totalizer_sum

        #         logging.error(f'''
        #         len this_date_input:       {len(this_date_input)}
        #         metre_weighbridget_deff:   {metre_weighbridget_deff}
        #         meter_amount_sum:          {meter_amount_sum}
        #         totalizer_weighbridge_sum: {totalizer_weighbridge_sum}
        #         totalizer_sum:             {totalizer_sum}
        #
        # ''')
        # if calendar == 'fa_IR':
        # report_date_show = jdatetime.date.fromgregorian(date=this_date_input[0].loading_date).strftime('%Y/%m/%d')
        return {
            'docs': this_date_input[0] if this_date_input else '',
            'doc_ids': docids,
            'doc_model': 'sd_payaneh_nafti.input_info',
            'meter_data': meter_data,
            'meter_inputs': meter_inputs,
            'meter_comment': meter_comment,
            'report_date_show': s_start_date,
            'meter_amount_sum': meter_amount_sum,
            'totalizer_weighbridge': totalizer_weighbridge,
            'totalizer_weighbridge_count': totalizer_weighbridge_count,
            'totalizer_weighbridge_sum': totalizer_weighbridge_sum,
            'totalizer_sum': totalizer_sum,
            'truck_count_sum': truck_count_sum,
            'metre_weighbridget_deff': metre_weighbridget_deff,
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


