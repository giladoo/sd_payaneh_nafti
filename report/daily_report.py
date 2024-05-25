# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http


# ########################################################################################
class ReportSdPayanehNaftiDaily(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.daily_report_template'
    _description = 'Daily Report'

    # ########################################################################################
    @api.model
    def _get_report_values(self, docids, data=None):
        errors = []
        doc_data_list = []
        row_data_lines = []
        footer_data = {
            'total_gsv_l': 0,
            'total_tanks': 0,
            'total_remain': 0,
            'total_remain_tanks': 0,
        }
        context = self.env.context
        time_z = pytz.timezone(context.get('tz'))
        date_time = datetime.now(time_z)
        date_time = self.date_converter(date_time, context.get('lang'))

        form_data = data.get('form_data')
        start_date = form_data.get('start_date')
        date_format = '%Y-%m-%d'
        start_date = datetime.strptime(start_date, date_format).date()

        input_records = self.env['sd_payaneh_nafti.input_info'].search([('loading_date', '=', start_date),
                                                                        ('state', 'in', ['done', 'finished']),])
        calendar = context.get('lang')
        if calendar == 'fa_IR':
            s_start_date = jdatetime.date.fromgregorian(date=start_date).strftime("%Y/%m/%d")
        else:
            s_start_date = start_date.strftime("%Y/%m/%d")
        if len(input_records) == 0:
            return {
                'errors': [_(f'No record have found for selected date: {s_start_date} ')],
            }
        docids = [input_records.ids]

        # print(f'\ncalendar:{calendar}\n')
        # print(f'\ninput_records:{input_records}\n')

        registration_nos = sorted(list({rec.registration_no.registration_no for rec in input_records}))
        # print(f'\nregistration_codes:{registration_nos}\n')

        for index, reg_no in enumerate(registration_nos):
            data = [rec for rec in input_records if rec.registration_no.registration_no == reg_no]
            final_gsv_l = [rec.final_gsv_l for rec in input_records if rec.registration_no.registration_no == reg_no]
            final_gsv_b = [rec.final_gsv_b for rec in input_records if rec.registration_no.registration_no == reg_no]
            final_mt = [rec.final_mt for rec in input_records if rec.registration_no.registration_no == reg_no]
            # for d in data:
            d = data[0]
            if calendar == 'fa_IR':
                d_start_date = jdatetime.date.fromgregorian(date=d.registration_no.start_date).strftime("%Y/%m/%d")
                d_end_date = jdatetime.date.fromgregorian(date=d.registration_no.end_date).strftime("%Y/%m/%d")
            else:
                d_start_date = d.registration_no.start_date.strftime("%Y/%m/%d")
                d_end_date = d.registration_no.end_date.strftime("%Y/%m/%d")

            reg_inputs_all = self.env['sd_payaneh_nafti.input_info'].search([('registration_no', '=', d.registration_no.id),
                                                                             ('loading_date', '<=', start_date),
                                                                             ('state', 'in', ['done', 'finished']),])

            final_gsv_b_all = [rec.final_gsv_b for rec in reg_inputs_all ]
            sum_final_gsv_b = round(sum(final_gsv_b))
            tanks_count = len(data)
            remain_amount = d.registration_no.amount - round(sum(final_gsv_b_all))
            remain_tanks = round(remain_amount/200)
            row_data_lines.append((index + 1,
                                   d.registration_no.contract_no,
                                   d.registration_no.order_no if d.registration_no.order_no else '',
                                   d.registration_no.buyer.name,
                                   d_start_date,
                                   d_end_date,
                                   d.registration_no.destination.name,
                                   sum_final_gsv_b,
                                   tanks_count,
                                   remain_amount,
                                   remain_tanks,
                                   ))
            footer_data['total_gsv_l'] += sum(final_gsv_b)
            footer_data['total_tanks'] += tanks_count
            footer_data['total_remain'] += d.registration_no.amount - (sum(final_gsv_b_all))
            footer_data['total_remain_tanks'] += remain_amount/200

        footer_data['total_gsv_l'] = round(footer_data['total_gsv_l'])
        footer_data['total_remain'] = round(footer_data['total_remain'])
        footer_data['total_remain_tanks'] = round(footer_data['total_remain_tanks'])



        # print(footer_data)
            # print(f' | {index + 1: ^2}'
            #       f' | {reg_no: ^4}'
            #       f' | {d.registration_no.contract_no: ^8}'
            #       f' | {d.registration_no.order_no: ^4}'
            #       f' | {d_start_date: ^10}'
            #       f' | {d_end_date: ^10}'
            #       f' | {d.registration_no.buyer.name: ^30}'
            #       f' | {int(sum(final_gsv_b)): >10}'
            #       f' | {len(data): >4}'
            #       f' | {d.registration_no.amount - int(sum(final_gsv_b_all)) : >8}'
            #       f' | {int((d.registration_no.amount - int(sum(final_gsv_b_all)) )/200): >4}'
            #       )










        # if len(input_record) > 1:
        #     errors.append(_('[ERROR] There is more than one record'))
        # elif len(input_record) == 1:
        # for input_record in input_records:
        #     issue_date = input_record.loading_date
        #     if calendar == 'fa_IR':
        #         issue_date = jdatetime.date.fromgregorian(date=issue_date).strftime('%Y/%m/%d')
        #     tanker_no = {'plate_1': input_record.plate_1,
        #                  'plate_2': input_record.plate_2,
        #                  'plate_3': input_record.plate_3,
        #                  'plate_4': input_record.plate_4,
        #                  }
        #     contract_no = str(input_record.registration_no.contract_no)
        #     if input_record.registration_no.order_no:
        #         contract_no += '-' + str(input_record.registration_no.order_no)
        #
        #     doc_data = {
        #                 # 'buyer': str(input_record.buyer.name),
        #                 # 'contractor': str(input_record.contractor.name),
        #                 'document_no': input_record.document_no,
        #                 'contract_no': contract_no,
        #                 'user_name': self.env.user.name,
        #                 'tanker_no': tanker_no,
        #                 'driver': input_record.driver,
        #                 'contract_type': input_record.registration_no.contract_type,
        #                 'cargo_type': input_record.registration_no.cargo_type.name,
        #                 'front_container': input_record.front_container,
        #                 'middle_container': input_record.middle_container,
        #                 'back_container': input_record.back_container,
        #                 'total': input_record.total,
        #                 'issue_date': issue_date,
        #                 'loading_no': input_record.loading_no,
        #                 }
        #     doc_data_list.append((input_record, doc_data))
        # else:
        #     input_record = []
        #     errors.append(_('[ERROR] There is no record'))
        company_logo = f'/web/image/res.partner/{1}/image_128/'
        doc_data_list = [('', '')]
        return {
            'docs': input_records[0] if input_records else '',
            'doc_ids': docids,
            'doc_model': 'sd_payaneh_nafti.input_info',
            # 'document_no': document_no,
            'doc_data_list': doc_data_list,
            'row_data_lines': row_data_lines,
            'dates': [s_start_date, ],
            'footer_data': footer_data,

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

