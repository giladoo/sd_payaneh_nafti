# -*- coding: utf-8 -*-
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http


# ########################################################################################
class ReportSdPayanehNaftiLoadingPermit(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.loading_permit_report_template'
    _description = 'Loading Permit'

    # ########################################################################################
    @api.model
    def _get_report_values(self, docids, data=None):
        errors = []
        doc_data_list = []
        context = self.env.context
        time_z = pytz.timezone(context.get('tz'))
        date_time = datetime.now(time_z)
        date_time = self.date_converter(date_time, context.get('lang'))
        if docids:
            input_records = self.env['sd_payaneh_nafti.input_info'].browse(docids)
            # document_no = input_record.document_no
            calendar = context.get('lang')
        else:
            form_data = data.get('form_data')
            document_no = form_data.get('document_no')[1]
            input_records = self.env['sd_payaneh_nafti.input_info'].search([('document_no', '=', document_no)])
            # calendar = form_data.get('calendar')
            calendar = context.get('lang')

            docids = [input_records.id]

        # if len(input_record) > 1:
        #     errors.append(_('[ERROR] There is more than one record'))
        # elif len(input_record) == 1:
        for input_record in input_records:
            if not input_record.loading_date:
                errors = [_(f'There is no Loading Data for {input_record.registration_no.registration_no} on {date_time.get("date", "")}')]
                continue
            #     raise ValidationError(_(f'There is no Loading Date for {input_record.registration_no.registration_no}'))
            issue_date = input_record.loading_date

            if calendar == 'fa_IR':
                issue_date = jdatetime.date.fromgregorian(date=issue_date).strftime('%Y/%m/%d')
            tanker_no = {'plate_1': input_record.plate_1,
                         'plate_2': input_record.plate_2,
                         'plate_3': input_record.plate_3,
                         'plate_4': input_record.plate_4,
                         }
            contract_no = str(input_record.registration_no.contract_no)
            if input_record.registration_no.order_no:
                contract_no += '-' + str(input_record.registration_no.order_no)
            reg = input_record.registration_no
            # contract_type = dict(reg._fields['contract_type'].selection).get(reg.contract_type)
            contract_type = dict(reg._fields['contract_type']._description_selection(self.env)).get(reg.contract_type)
            doc_data = {
                        # 'buyer': str(input_record.buyer.name),
                        # 'contractor': str(input_record.contractor.name),
                        'document_no': str(input_record.document_no),
                        'contract_no': contract_no,
                        'user_name': self.env.user.name,
                        'tanker_no': tanker_no,
                        'driver': input_record.driver.name,
                        'contract_type': contract_type,
                        'cargo_type': input_record.registration_no.cargo_type.name,
                        'front_container': input_record.front_container,
                        'middle_container': input_record.middle_container,
                        'back_container': input_record.back_container,
                        'total': input_record.total,
                        'issue_date': issue_date,
                        'loading_no': input_record.loading_no,
                        }
            doc_data_list.append((input_record, doc_data))
        # else:
        #     input_record = []
        #     errors.append(_('[ERROR] There is no record'))
        company_logo = f'/web/image/res.partner/{1}/image_128/'
        return {
            'docs': input_records[0],
            'doc_ids': docids,
            'doc_model': 'sd_payaneh_nafti.input_info',
            # 'document_no': document_no,
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

