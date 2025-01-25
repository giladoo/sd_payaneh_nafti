# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http


# ########################################################################################
class ReportSdPayanehNaftiOutgateDaily(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.outgate_daily_report_template'
    _description = 'Outgate Daily Report'

    # ########################################################################################
    @api.model
    def _get_report_values(self, docids, data=None):
        # print(f'\n data: {data} \n')
        errors = []
        doc_data_list = []
        row_data_lines = []
        context = self.env.context
        time_z = pytz.timezone(context.get('tz'))
        date_time = datetime.now(time_z)
        date_time = self.date_converter(date_time, context.get('lang'))

        form_data = data.get('form_data')
        start_date = form_data.get('start_date')
        date_format = '%Y-%m-%d'
        start_date = datetime.strptime(start_date, date_format).date()
        calendar = form_data.get('calendar')

        input_records = self.env['sd_payaneh_nafti.input_info'].search([('loading_date', '=', start_date),
                                                                        ('state', 'in', ['done', 'finished']),
                                                                        ], order='loading_no')
        docids = [input_records.ids]

        if calendar == 'fa_IR':
            s_start_date = jdatetime.date.fromgregorian(date=start_date).strftime("%Y/%m/%d")

        else:
            s_start_date = start_date.strftime("%Y/%m/%d")
        if len(input_records) == 0:
            return {
                'errors': [_(f'No record have found for selected date: {s_start_date} ')],
            }

        registration_nos = sorted(list({rec.registration_no.registration_no for rec in input_records}))
        # print(f'\nregistration_codes:{registration_nos}\n')

        for index, rec in enumerate(input_records):
            plate = f'{rec.plate_1}-{rec.plate_2}{rec.plate_3}{rec.plate_4}'

            # print(f' | {index + 1: ^2}'
            #       f' | {rec.loading_no: ^8}'
            #       f' | {plate: ^10}'
            #       f' | {rec.driver: ^20}'
            #       f' | {rec.card_no: ^10}'
            #       f' | {rec.contractor.name: ^30}'
            #       f' | {rec.registration_no.buyer.name: ^30}'
            #       f' | {int(rec.final_gsv_l): ^10}'
            #       )

            row_data_lines.append((index + 1,
                                   rec.loading_no or '',
                                   plate or '',
                                   rec.driver.name or '',
                                   rec.card_no or '',
                                   rec.contractor.name or '',
                                   rec.registration_no.buyer.name or '',
                                   int(rec.final_gsv_l) or 0,

                                   ))







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
        # input_records  = ''
        return {
            'docs': input_records[0] if input_records else '',
            'doc_ids': docids,
            'doc_model': 'sd_payaneh_nafti.input_info',
            # 'document_no': document_no,
            'doc_data_list': doc_data_list,
            'row_data_lines': row_data_lines,
            'dates': [s_start_date, ],
            # 'footer_data': footer_data,

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

