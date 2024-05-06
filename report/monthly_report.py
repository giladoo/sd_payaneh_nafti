# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http


# ########################################################################################
class ReportSdPayanehNaftiMonthly(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.monthly_report_template'
    _description = 'Monthly Report'

    # ########################################################################################
    def get_report_values(self, docids, data=None):
        return self._get_report_values(docids, data)
    @api.model
    def _get_report_values(self, docids, data=None):
        errors = []
        doc_data_list = []
        row_data_lines_all = []
        row_data_lines_all_temp = []
        PAGE_LINES = 40
        calendar = self.env.context.get('lang')
        form_data = data.get('form_data')
        year = form_data.get('year')
        month = form_data.get('month')

        if calendar == 'fa_IR':
            first_day = jdatetime.date(int(year), int(month), 1)
            next_month = first_day.replace(day=28) + timedelta(days=5)
            last_day = (next_month - timedelta(days=next_month.day)).togregorian()
            first_day = first_day.togregorian()
            s_first_day = jdatetime.date.fromgregorian(date=first_day).strftime("%Y/%m/%d")
            s_last_day = jdatetime.date.fromgregorian(date=last_day).strftime("%Y/%m/%d")

        else:
            date_format = '%Y-%m-%d'
            start_date = datetime.strptime(f'{year}-{month}-1', date_format).date()
            first_day = start_date.replace(day=1)
            next_month = first_day.replace(day=28) + timedelta(days=5)
            last_day = next_month - timedelta(days=next_month.day)
            s_first_day = first_day.strftime("%Y-%m-%d")
            s_last_day = last_day.strftime("%Y-%m-%d")
        input_records = self.env['sd_payaneh_nafti.input_info'].search([('loading_date', '>=', first_day),
                                                                        ('loading_date', '<=', last_day)])
        input_dict = list([{
            'registration_no': rec.registration_no.registration_no,
            'contract_type': rec.registration_no.contract_type or '',
            'letter_no': rec.registration_no.letter_no or '',
            'order_no': rec.registration_no.order_no or '',
            'buyer': rec.registration_no.buyer.name or '',
            'amount': rec.registration_no.amount or 0,
            'unit': rec.registration_no.unit or 0,
            'loading_type': rec.registration_no.loading_type or '',
            'loading_date': rec.loading_date or '',
            'final_gsv_l': rec.final_gsv_l,
            'final_mt': rec.final_mt,

                            } for rec in input_records])



        # print(f'===========\n'
        #       f'{input_dict[0]}\n')

        if len(input_records) == 0:
            return{
                'errors': [_(f'No record have found for selected time duration: {s_first_day} to {s_last_day}')],
                }
        docids = [input_records.ids]

        registration_nos = sorted(list({rec.registration_no.registration_no for rec in input_records }))
        # print(f'\nregistration_codes:{registration_nos}\n')
        row_data_temp = []
        final_gsv_b_list_types = []

        for index, reg_no in enumerate(registration_nos):
            data = [rec for rec in input_records if rec.registration_no.registration_no == reg_no]
            d = data[0]
            reg = d.registration_no
            unit = reg.unit
            loading_type = reg.loading_type
            contract_type = reg.contract_type
            # final_gsv_l = [rec.final_gsv_l for rec in input_records if rec.registration_no.registration_no == reg_no]
            final_gsv_l = [rec['final_gsv_l'] for rec in input_dict if rec['registration_no'] == reg_no]
            # excel: EXTRA Data, FO~GW
            # it calculates round(rec.final_gsv_l / 158.987, 2) for each day of the month, and then it calculate the sum.
            final_gsv_b_list = []
            final_gsv_b_list_stock = []
            final_gsv_b_list_general = []
            final_gsv_b_list_internal = []
            final_gsv_b_list_export = []

            for day_date in self._daterange(first_day, last_day + timedelta(days=1)):
                # print(day_date.strftime("%Y-%m-%d"))
                final_gsv_b_list.append(round(sum(list([rec['final_gsv_l'] for rec in input_dict
                                         if rec['registration_no'] == reg_no and
                                                        rec['loading_date'] == day_date ])) / 158.987, 2))
                final_gsv_b_list_types.append(
                    {'final_gsv_b': round(sum(list([rec['final_gsv_l'] for rec in input_dict
                                     if rec['registration_no'] == reg_no and
                                     rec['loading_date'] == day_date])) / 158.987, 2),
                     'final_gsv_l': sum(list([rec['final_gsv_l'] for rec in input_dict
                                          if rec['registration_no'] == reg_no and rec['loading_date'] == day_date])),
                     'final_mt': round(sum(list([rec['final_mt'] for rec in input_dict
                                          if rec['registration_no'] == reg_no and rec['loading_date'] == day_date])), 3),
                     'contract_type': contract_type,
                     'loading_type': loading_type,
                     }
                )


            final_gsv_b = final_gsv_b_list
            # final_gsv_b = [round(rec.final_gsv_l / 158.987, 3) for rec in input_records if rec.registration_no.registration_no == reg_no]
            # final_gsv_b = [round(rec.final_gsv_b, 3) for rec in input_records if rec.registration_no.registration_no == reg_no]

            # final_mt = [rec.final_mt for rec in input_records if rec.registration_no.registration_no == reg_no]
            final_mt = [rec['final_mt'] for rec in input_dict if rec['registration_no'] == reg_no]

            # for d in data:
            # unit = dict(reg._fields['unit']._description_selection(self.env)).get(reg.unit)
            # loading_type = dict(reg._fields['loading_type']._description_selection(self.env)).get(reg.loading_type)
            # contract_type = dict(reg._fields['contract_type']._description_selection(self.env)).get(reg.contract_type)

            final_gsv_l_sum = round(sum(final_gsv_l)) or 0
            final_gsv_b_sum = round(sum(final_gsv_b), 2) or 0
            # final_gsv_b_sum1 = round(sum(final_gsv_b), 3) or 0
            final_mt_sum = round(sum(final_mt), 3) or 0
            # print(final_gsv_b)

            row_data_lines_all.append((index + 1,
                                   d.registration_no.letter_no or '',
                                   d.registration_no.contract_no or '',
                                   d.registration_no.order_no or '',
                                   d.registration_no.buyer.name or '',
                                   d.registration_no.amount or 0,
                                   self.type_name(unit, calendar),
                                   self.type_name(loading_type, calendar),
                                   self.type_name(contract_type, calendar),
                                   #     todo: show rounded number with filling, 3333.5 > 3333.500
                                   final_gsv_l_sum,
                                       final_gsv_b_sum,
                                       final_mt_sum,
                                   # f'{final_gsv_b_sum:.2f}',
                                   # f'{final_mt_sum:.3f}' ,
                                   len(data) or 0,
                                       # final_gsv_b_sum1,
                                   ))
            row_data_lines_all_temp.append({'index': index + 1,
                                            'contract_type': contract_type,
                                            'loading_type': loading_type,
                                            'unit': unit,
                                            'final_gsv_l_sum': final_gsv_l_sum,
                                            'final_gsv_b_sum': final_gsv_b_sum,
                                            'final_mt_sum': final_mt_sum,
                                            'count': len(data) or 0,
                                            # 'final_gsv_b_sum': final_gsv_b_sum1,

                                            })

        final_gsv_l_stock_1 = [rec[9] for rec in row_data_lines_all if rec[8] == 'stock']
        row_data_lines_split = [row_data_lines_all[x:x + PAGE_LINES] for x in range(0, len(row_data_lines_all), PAGE_LINES)]
        # row_data_lines_all_temp_split = [row_data_lines_all_temp[x:x + 50] for x in range(0, len(row_data_lines_all_temp), 50)]

        row_data_lines  = row_data_lines_split[0]
            # final_gsv_l_stock_1: {sum(final_gsv_l_stock_1)}


        #  todo: calculate each one based on the final_gsv_b_list_export and oter lists


        # final_gsv_l_general = [int(rec.final_gsv_l) for rec in input_records if rec.registration_no.contract_type == 'general']
        # final_gsv_l_internal = [int(rec.final_gsv_l) for rec in input_records if rec.registration_no.loading_type == 'internal']
        # final_gsv_l_export = [int(rec.final_gsv_l) for rec in input_records if rec.registration_no.loading_type == 'export']

        final_gsv_l_stock = [rec['final_gsv_l'] for rec in final_gsv_b_list_types if rec['contract_type'] == 'stock']
        final_gsv_l_general = [rec['final_gsv_l'] for rec in final_gsv_b_list_types if rec['contract_type'] == 'general']
        final_gsv_l_internal = [rec['final_gsv_l'] for rec in final_gsv_b_list_types if rec['loading_type'] == 'internal']
        final_gsv_l_export = [rec['final_gsv_l'] for rec in final_gsv_b_list_types if rec['loading_type'] == 'export']

        # final_gsv_b_stock = [round(rec.final_gsv_b, 13) for rec in input_records if rec.registration_no.contract_type == 'stock']
        # final_gsv_b_general = [round(rec.final_gsv_b, 13) for rec in input_records if rec.registration_no.contract_type == 'general']
        # final_gsv_b_internal = [round(rec.final_gsv_b, 13) for rec in input_records if rec.registration_no.loading_type == 'internal']
        # final_gsv_b_export = [round(rec.final_gsv_b, 13) for rec in input_records if rec.registration_no.loading_type == 'export']

        final_gsv_b_stock = [rec['final_gsv_b'] for rec in final_gsv_b_list_types if rec['contract_type'] == 'stock']
        final_gsv_b_general = [rec['final_gsv_b'] for rec in final_gsv_b_list_types if rec['contract_type'] == 'general']
        final_gsv_b_internal = [rec['final_gsv_b'] for rec in final_gsv_b_list_types if rec['loading_type'] == 'internal']
        final_gsv_b_export = [rec['final_gsv_b'] for rec in final_gsv_b_list_types if rec['loading_type'] == 'export']



        # final_mt_stock = [rec.final_mt for rec in input_records if rec.registration_no.contract_type == 'stock']
        # final_mt_general = [rec.final_mt for rec in input_records if rec.registration_no.contract_type == 'general']
        # final_mt_internal = [rec.final_mt for rec in input_records if rec.registration_no.loading_type == 'internal']
        # final_mt_export = [rec.final_mt for rec in input_records if rec.registration_no.loading_type == 'export']

        final_mt_stock = [rec['final_mt'] for rec in final_gsv_b_list_types if rec['contract_type'] == 'stock']
        final_mt_general = [rec['final_mt'] for rec in final_gsv_b_list_types if rec['contract_type'] == 'general']
        final_mt_internal = [rec['final_mt'] for rec in final_gsv_b_list_types if rec['loading_type'] == 'internal']
        final_mt_export = [rec['final_mt'] for rec in final_gsv_b_list_types if rec['loading_type'] == 'export']

        tank_count_stock = len([1 for rec in input_records if rec.registration_no.contract_type == 'stock'])
        tank_count_general = len([1 for rec in input_records if rec.registration_no.contract_type == 'general'])
        tank_count_internal = len([1 for rec in input_records if rec.registration_no.loading_type == 'internal'])
        tank_count_export = len([1 for rec in input_records if rec.registration_no.loading_type == 'export'])

        footer_data = {
            'final_gsv_l_stock': round(sum(final_gsv_l_stock)),
            'final_gsv_b_stock': round(sum(final_gsv_b_stock), 2),
            'final_mt_stock': round(sum(final_mt_stock), 3),
            'tank_count_stock': tank_count_stock,

            'final_gsv_l_general': round(sum(final_gsv_l_general)),
            'final_gsv_b_general': round(sum(final_gsv_b_general), 2),
            'final_mt_general': round(sum(final_mt_general), 3),
            'tank_count_general': tank_count_general,

            'final_gsv_l_internal': round(sum(final_gsv_l_internal)),
            'final_gsv_b_internal': round(sum(final_gsv_b_internal), 2),
            'final_mt_internal': round(sum(final_mt_internal), 3),
            'tank_count_internal': tank_count_internal,

            'final_gsv_l_export': round(sum(final_gsv_l_export)),
            'final_gsv_b_export': round(sum(final_gsv_b_export), 2),
            'final_mt_export': round(sum(final_mt_export), 3),
            'tank_count_export': tank_count_export,

        }

        company_logo = f'/web/image/res.partner/{1}/image_128/'
        doc_data_list = [('', '')]
        # errors = ['test error']
        all_page_date = list([[rec, footer_data] for rec in row_data_lines_split])
        return {
            'docs': input_records[0] if input_records else '',
            'doc_ids': docids,
            'doc_model': 'sd_payaneh_nafti.input_info',
            # 'document_no': document_no,
            'doc_data_list': doc_data_list,
            # 'row_data_lines': row_data_lines,
            # 'footer_data': footer_data,
            'all_page_date': all_page_date,
            'page_count': len(all_page_date),
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

    def _daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)
