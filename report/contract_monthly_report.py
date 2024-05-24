# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http

BBL_FACTOR = 158.987


# ########################################################################################
class ReportSdPayanehNaftiContractMonthly(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.contract_monthly_report_template'
    _description = 'Loading Permit'

    # ########################################################################################
    @api.model
    def _get_report_values(self, docids, data=None):
        errors = []
        row_data_lines = []
        header = {}
        footer_data = {
            'total_gsv_l': 0,
            'total_gsv_b': 0,
            'total_mt': 0,
            'total_tankers': 0,
        }

        calendar = self.env.context.get('lang')
        form_data = data.get('form_data')
        registration_no = form_data.get('registration_no')[1]
        year = form_data.get('year')
        month = form_data.get('month')
        loading_type = form_data.get('loading_type')
        # input_records_all = self.env['sd_payaneh_nafti.input_info'].search([('registration_no', '=', registration_no)],order='loading_date')
        # first_loading_date = input_records_all[0].loading_date
        # last_loading_date = input_records_all[-1].loading_date

        if calendar == 'fa_IR':
            first_day = jdatetime.date(int(year), int(month), 1)
            next_month = first_day.replace(day=28) + timedelta(days=5)
            last_day = (next_month - timedelta(days=next_month.day)).togregorian()
            first_day = first_day.togregorian()
            s_first_day = jdatetime.date.fromgregorian(date=first_day).strftime("%Y/%m/%d")
            s_last_day = jdatetime.date.fromgregorian(date=last_day).strftime("%Y/%m/%d")
            g_first_day = first_day.strftime("%Y%m%d")
            g_last_day = last_day.strftime("%Y%m%d")

        else:
            date_format = '%Y-%m-%d'
            start_date = datetime.strptime(f'{year}-{month}-1', date_format).date()
            first_day = start_date.replace(day=1)
            next_month = first_day.replace(day=28) + timedelta(days=5)
            last_day = next_month - timedelta(days=next_month.day)
            s_first_day = first_day.strftime("%Y-%m-%d")
            s_last_day = last_day.strftime("%Y-%m-%d")
            g_first_day = first_day.strftime("%Y%m%d")
            g_last_day = last_day.strftime("%Y%m%d")
        date_of_range = [first_day + timedelta(days=delta) for delta in range((last_day - first_day).days + 1)]

        input_records = self.env['sd_payaneh_nafti.input_info'].search([('request_date', '>=', first_day),
                                                                        ('request_date', '<=', last_day),
                                                                        ('registration_no', '=', registration_no)],)
        # r_1674 = list([(rec, rec.registration_no, rec.document_no) for rec in input_records if registration_no == 1674])
        # print('+++++++++++++++++++++')
        # for r in r_1674:
        #     print(r)
        # print()
        if len(input_records) == 0:
            return{
                'errors': [_(f'No record have found for selected time duration: {s_first_day} to {s_last_day}')],
                }
        docids = [input_records.ids]
        registration = input_records[0].registration_no
        if calendar == 'fa_IR':
            s_start_date = jdatetime.date.fromgregorian(date=registration.start_date).strftime("%Y/%m/%d")
            s_end_date = jdatetime.date.fromgregorian(date=registration.end_date).strftime("%Y/%m/%d")

        else:
            s_start_date = registration.start_date.strftime("%Y-%m-%d")
            s_end_date = registration.end_date.strftime("%Y-%m-%d")
        if loading_type == 'internal':
            unit = dict(registration._fields['unit']._description_selection(self.env)).get(registration.unit)
        else:
            unit = dict(registration._fields['unit'].selection).get(registration.unit)

        header = {
            'contract_no': registration.contract_no + (f'-{registration.order_no}' if registration.order_no else ''),
            'amount': registration.amount,
            'unit': unit,
            'buyer': registration.buyer.name,
            'destination': registration.destination.name,
            'contractors': ' / '.join([rec.name for rec in registration.contractors]),
        }

        for index, rec_date in enumerate(date_of_range):
            if calendar == 'fa_IR':
                s_rec_date = jdatetime.date.fromgregorian(date=rec_date).strftime("%Y/%m/%d")
            else:
                s_rec_date = rec_date.strftime("%Y/%m/%d")

            data = [rec for rec in input_records if rec.loading_date == rec_date]
            final_gsv_l = [rec.final_gsv_l for rec in input_records if rec.loading_date == rec_date]
            final_mt = [rec.final_mt for rec in input_records if rec.loading_date == rec_date]
            d = data[0] if len(data) > 0 else 0
            total_gsv_l = int(sum(final_gsv_l))
            final_gsv_b = round(total_gsv_l / BBL_FACTOR, 2)
            # total_gsv_b = round(sum(final_gsv_b), 2)
            total_gsv_b = final_gsv_b
            total_mt = round(sum(final_mt), 3)
            total_tankers = len(final_mt)

            row_data_lines.append((index + 1,
                               s_rec_date,
                               d.sp_gr if d else "",
                               total_gsv_l,
                               total_gsv_b,
                               total_mt,
                               total_tankers,
                               ))
            footer_data['total_gsv_l'] += total_gsv_l
            footer_data['total_gsv_b'] += total_gsv_b
            footer_data['total_mt'] += total_mt
            footer_data['total_tankers'] += total_tankers

        footer_data['total_gsv_b'] = round(footer_data['total_gsv_b'], 2)
        footer_data['total_mt'] = round(footer_data['total_mt'], 3)
        input_records_past = self.env['sd_payaneh_nafti.input_info'].search([('registration_no', '=', registration_no),
                                                                             ('loading_date', '<', first_day)],)
        final_gsv_l_past = [rec.final_gsv_l for rec in input_records_past]
        # final_gsv_b_past = [rec.final_gsv_b for rec in input_records_past]
        final_gsv_b_past = [rec.final_gsv_b for rec in input_records_past]
        final_mt_past = [rec.final_mt for rec in input_records_past]

        footer_data['total_gsv_l_past'] = int(sum(final_gsv_l_past))
        footer_data['total_gsv_b_past'] = round(sum(final_gsv_b_past), 2)
        footer_data['total_mt_past'] = round(sum(final_mt_past), 3)
        footer_data['total_tankers_past'] = len(final_mt_past)

        footer_data['total_gsv_l_all'] = footer_data['total_gsv_l'] + footer_data['total_gsv_l_past']
        footer_data['total_gsv_b_all'] = round(footer_data['total_gsv_b'] + footer_data['total_gsv_b_past'], 2)
        footer_data['total_mt_all'] = round(footer_data['total_mt'] + footer_data['total_mt_past'], 3)
        footer_data['total_tankers_all'] = footer_data['total_tankers'] + footer_data['total_tankers_past']

        #     # for d in data:
        #     print(f' | {index + 1: ^2}'
        #           f' | {s_rec_date: ^8}'
        #           f' | {d.sp_gr if d else "": ^6}'
        #           f' | {int(sum(final_gsv_l)): >10}'
        #           f' | {round(sum(final_gsv_b), 2): >10}'
        #           f' | {round(sum(final_mt), 3): >10}'
        #           f' | {len(final_mt): >3}'
        #           )









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
            'header': header,
            'row_data_lines': row_data_lines,
            'footer_data': footer_data,
            'loading_type': loading_type,

            'doc_data_list': doc_data_list,
            'registration_no': registration.registration_no,
            'g_date': f'{g_first_day}_{g_last_day}',
            'dates': [s_start_date, s_end_date],

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

