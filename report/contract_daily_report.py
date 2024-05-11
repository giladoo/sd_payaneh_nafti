# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http


# ########################################################################################
class ReportSdPayanehNaftiContractDailyReport(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.contract_daily_report_template'
    _description = 'Contract Daily Report'

    # ########################################################################################
    def get_report_values(self, docids=None, data=None):
        return self._get_report_values(docids, data)

    # ########################################################################################
    @api.model
    def _get_report_values(self, docids=None, data=None):
        errors = []
        doc_data_list = []
        PAGE_LINES = 25
        date_format = '%Y-%m-%d'
        context = self.env.context
        time_z = pytz.timezone(context.get('tz'))
        date_time = datetime.now(time_z)
        calendar = context.get('lang')
        date_time = self.date_converter(date_time, context.get('lang'))

        if docids:
            contract_record = self.env['sd_payaneh_nafti.contract_registration'].browse(docids[0])
            registration_no = contract_record.registration_no
            loading_type = contract_record.loading_type
            # contract_no = input_record.contract_no
            report_date = date.today()

        else:
            form_data = data.get('form_data')
            loading_type = form_data.get('loading_type')
            registration_no = form_data.get('registration_no')[1]
            contract_record = self.env['sd_payaneh_nafti.contract_registration'].search([
                ('registration_no', '=', registration_no)])
            # calendar = form_data.get('calendar')
            docids = [contract_record.id]
            report_date = form_data.get('report_date') if 'report_date' in form_data.keys() else False
            report_date = datetime.strptime(report_date, date_format).date()
        # REPORT DATE
        g_start_date = report_date.strftime("%Y%m%d")

        if calendar == 'fa_IR':
            first_day = jdatetime.date.fromgregorian(date=report_date).replace(day=1)
            next_month = first_day.replace(day=28) + timedelta(days=5)
            last_day = (next_month - timedelta(days=next_month.day)).togregorian()
            first_day = first_day.togregorian
            report_day = report_date
            # report_date = jdatetime.date.fromgregorian(date=report_date).strftime('%Y/%m/%d')
            s_start_date = jdatetime.date.fromgregorian(date=report_date).strftime("%Y/%m/%d")

        else:
            first_day = report_date.replace(day=1)
            next_month = first_day.replace(day=28) + timedelta(days=5)
            last_day = next_month - timedelta(days=next_month.day)
            report_day = report_date
            s_start_date = report_date.strftime("%Y/%m/%d")

        input_records = self.env['sd_payaneh_nafti.input_info'].search([('registration_no', '=', registration_no)], order='id')
        if len(input_records) == 0:
            return {
                'errors': [_(f'No record have found for contract {registration_no} on selected date: {s_start_date} ')],
            }

        # for contract in contract_record:
        # todo: you need to create a reprot dataset for  multi record selection

        input_records_behind_date = tuple(filter(lambda rec: rec.request_date <= report_day, input_records))
        registration = input_records[0].registration_no
        if loading_type == 'internal':
            unit = dict(registration._fields['unit']._description_selection(self.env)).get(registration.unit)
        else:
            unit = registration.unit
        #     todo: it shows metric_tone which needed to show Metric Tone

        # print(f'>>>>>>>>>\n unit: {unit} registration.unit: {registration.unit} '
        #       f'\n {registration._fields["unit"]}')

        if registration.unit == 'barrel':
            used_amounts = sum([ua.final_gsv_b for ua in input_records_behind_date])
        elif registration.unit == 'metric_ton':
            used_amounts = sum([ua.final_mt for ua in input_records_behind_date])
        else:
            used_amounts = 0
        used_amounts = int(used_amounts)
        amount = registration.amount if registration.init_amount == 0 else registration.init_amount
        remain_amounts = int(amount - used_amounts)
        # print(f'=========>  \n registration: {registration} '
        #                   f'\n len, input_records_behind_date: {len(input_records_behind_date)}'
        #                   f'\n registration.unit: {registration.unit}'
        #                   f'\n amount: {amount}'
        #                   f'\n remain_amount: {remain_amounts}'
        #                   f'\n used_amounts: {used_amounts}'
        #                   f'\n ')

        input_records_day = tuple(filter(lambda rec: rec.request_date == report_day, input_records))
        input_records_day = sorted(input_records_day, key=lambda rec: rec.loading_no)
        inputs_list = []
        pages = []
        total = {
            'totalizer_diff_sum': 0,
            'final_tov_l_sum': 0,
            'final_gsv_l_sum': 0,
            'final_gsv_b_sum': 0,
            'final_mt_sum': 0,
        }

        page_count = len(input_records_day) // PAGE_LINES + 1
        for index in range(page_count):
            inputs = input_records_day[index * PAGE_LINES:(index + 1) * PAGE_LINES]
            totalizer_diff_sum = sum([_input.totalizer_difference for _input in inputs if _input.weighbridge == 'no'])
            final_tov_l_sum = sum([_input.final_tov_l for _input in inputs])
            final_gsv_l_sum = sum([_input.final_gsv_l for _input in inputs])
            final_gsv_b_sum = sum([round(_input.final_gsv_l / 158.987, 3) for _input in inputs])
            # print(list([round(_input.final_gsv_l / 158.987, 3) for _input in inputs]))
            final_mt_sum = sum([_input.final_mt for _input in inputs])
            page = {
                'totalizer_diff_sum': totalizer_diff_sum,
                'final_tov_l_sum': int(final_tov_l_sum),
                'final_gsv_l_sum': int(final_gsv_l_sum),
                'final_gsv_b_sum': round(final_gsv_b_sum, 2),
                'final_mt_sum': final_mt_sum,
            }
            total['totalizer_diff_sum'] += totalizer_diff_sum
            total['final_tov_l_sum'] += int(final_tov_l_sum)
            total['final_gsv_l_sum'] += int(final_gsv_l_sum)
            total['final_gsv_b_sum'] += round(final_gsv_b_sum, 2)
            total['final_mt_sum'] += final_mt_sum
            inputs_list.append(inputs)
            pages.append(page)
        # errors = [f'No inputs'] if len(inputs_list[0]) == 0 else errors
        # inputs_list = [f'No inputs'] if len(inputs_list[0]) == 0 else inputs_list
        doc_data = {
                    'page_lines': PAGE_LINES,
                    'inputs': inputs_list,
                    'unit': unit,
                    'remain_amounts': remain_amounts,
                    'used_amounts': used_amounts,
                    'pages': pages,
                    'total': total,
                    'page_count': page_count,
                    'input_records_day': input_records_day,
                    # 'payaneh_agent': form_data.get('payaneh_agent'),
                    # 'observe_agent': form_data.get('observe_agent'),
                    # 'buyer_agent': form_data.get('buyer_agent')
                    }
        doc_data_list.append((contract_record, doc_data))


        print(f'''

contract_record:
{contract_record}
        
doc_data_list:
{doc_data_list}  
errors:
{errors}

# g_start_date:
# {g_start_date}  {type(g_start_date)}

''')

        company_logo = f'/web/image/res.partner/{1}/image_128/'
        return {
            'docs': contract_record,
            'doc_ids': docids,
            'doc_model': 'sd_payaneh_nafti.input_info',
            'report_date_g': g_start_date,
            'report_date': s_start_date,
            'loading_type': loading_type,

            'doc_data_list': doc_data_list,
            # 'input_record': input_record,
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

