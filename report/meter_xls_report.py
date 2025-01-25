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
class ReportSdPayanehNaftiMeterXlsReport(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.meter_xls_report_template'
    _inherit = 'report.report_xlsx.abstract'


    # ########################################################################################
    def generate_xlsx_report(self, workbook, data, p):
        report = self.env['report.sd_payaneh_nafti.meter_report_template']
        self.create_excel(workbook, report.get_report_values([], data))
        # {
        #     'docs': this_date_input[0] if this_date_input else '',
        #     'doc_ids': docids,
        #     'doc_model': 'sd_payaneh_nafti.input_info',
        #     'meter_data': meter_data,
        #     'meter_comment': meter_comment,
        #     'report_date_show': s_start_date,
        #     'meter_amount_sum': meter_amount_sum,
        #     'totalizer_weighbridge_sum': totalizer_weighbridge_sum,
        #     'totalizer_sum': totalizer_sum,
        #     'truck_count_sum': truck_count_sum,
        #     'metre_weighbridget_deff': metre_weighbridget_deff,
        #     'errors': errors,
        # }
    # ########################################################################################
    def create_excel(self, workbook, report_data ):
        if report_data.get('errors'):
            raise ValidationError(report_data['errors'])
        sheet = workbook.add_worksheet(f'گزارش میتر')
        bold = workbook.add_format({'bold': True})
        center = workbook.add_format({'align': 'center'})
        right = workbook.add_format({'align': 'right'})
        bold_center_bg = workbook.add_format({'bold': True,
                                           'size': 12,
                                           'align': 'center',
                                           'bg_color': '#bbbbbb',
                                           })
        warning_bg = workbook.add_format({'bold': True,
                                           'bg_color': '#ffac00',
                                           })
        bold_center = workbook.add_format({'bold': True,
                                           'align': 'center',
                                           })
        format_left_to_right = workbook.add_format({"reading_order": 1})
        format_right_to_left = workbook.add_format({"reading_order": 2})
        num_format_3 = workbook.add_format({"num_format": '0.000'})
        num_format_3_bold = workbook.add_format({"num_format": '0.000','bold': True,})
        num_format_4 = workbook.add_format({"num_format": '0.0000'})
        num_format_4_bold = workbook.add_format({"num_format": '0.0000','bold': True,})
        sheet.set_column('A:Z', 15)
        sheet.right_to_left()
        row = iter(list(range(3000)))
        col = 0
        sheet.write(next(row), col + 1, 'گزارش میتر', bold)
        sheet.write(next(row), col + 1, report_data['report_date_show'], bold)
        next(row)
        row_no = next(row)
        sheet.write(row_no, col, 'میتر', bold_center_bg)
        sheet.write(row_no, col + 1, 'توتالایزر ابتدایی', bold_center_bg)
        sheet.write(row_no, col + 2, 'توتالایزر انتهایی', bold_center_bg)
        sheet.write(row_no, col + 3, 'مقدار میتر', bold_center_bg)
        sheet.write(row_no, col + 4, 'تعداد', bold_center_bg)
        row_no = next(row)
        for data in report_data['meter_data']:
            sheet.write(row_no, col, data['meter_no'] if data['meter_no'] else 'Master', center)
            sheet.write(row_no, col + 1, data['first_totalizer'], )
            sheet.write(row_no, col + 2, data['last_totalizer'], )
            sheet.write(row_no, col + 3, data['meter_amounts'], )
            sheet.write(row_no, col + 4, data['truck_count'], center)
            row_no = next(row)
        sheet.write(row_no, col, 'جمع خالص بارگیری شده از میتر', bold)
        sheet.write(row_no, col + 3, report_data['meter_amount_sum'], bold)
        sheet.write(row_no, col + 4, report_data['truck_count_sum'], bold_center)
        row_no = next(row)
        sheet.write(row_no, col, 'جمع خالص میتر در بارگیری از باسکول', bold)
        sheet.write(row_no, col + 3, report_data['totalizer_weighbridge_sum'], bold)
        sheet.write(row_no, col + 4, report_data['totalizer_weighbridge_count'], bold_center)
        row_no = next(row)
        sheet.write(row_no, col, 'مقدار اسناد بارگیری توسط میتر و باسکول', bold)
        sheet.write(row_no, col + 3, report_data['totalizer_sum'], bold)
        row_no = next(row)
        sheet.write(row_no, col, 'اختلاف بارگیری میتر و باسکول با اسناد صادر شده', bold)
        sheet.write(row_no, col + 3, report_data['metre_weighbridget_deff'], bold)

        next(row)
        next(row)
        next(row)
        for meter_no, meter_inputs in report_data['meter_inputs']:
            row_no = next(row)
            sheet.write(row_no, col, f' میتر {meter_no if meter_no else "Master"}', bold_center_bg)
            sheet.write(row_no, col + 1, 'توتالایزر ابتدایی', bold_center_bg)
            sheet.write(row_no, col + 2, 'توتالایزر انتهایی', bold_center_bg)
            sheet.write(row_no, col + 3,  'مقدار میتر', bold_center_bg)
            sheet.write(row_no, col + 4,  'اختلاف توتالایزر', bold_center_bg)
            sheet.write(row_no, col + 5, 'باسکول دارد', bold_center_bg)
            sheet.write(row_no, col + 6, 'وزن خالی نفتکش', bold_center_bg )
            sheet.write(row_no, col + 7, 'وزن پر نفتکش', bold_center_bg)
            sheet.write(row_no, col + 8, 'وزن خالص نفتکش', bold_center_bg)
            sheet.write(row_no, col + 9, 'شماره سند', bold_center_bg)
            sheet.write(row_no, col + 10, 'شماره قرارداد', bold_center_bg)
            row_no = next(row)
            totalizer_end = 'first'
            for index, meter_input in enumerate(meter_inputs):
                diff_s = False
                diff_e = False
                totalizer_difference = 0
                if totalizer_end != 'first' and totalizer_end != meter_input.totalizer_start:
                    diff_s = True
                    totalizer_difference = meter_input.totalizer_start - totalizer_end
                if index > 0 and index + 1 != len(meter_inputs) and meter_input.totalizer_end != meter_inputs[index + 1].totalizer_start:
                    diff_e = True

                sheet.write(row_no, col, meter_no, bold_center)
                sheet.write(row_no, col + 1, meter_input.totalizer_start, warning_bg if diff_s else '')
                sheet.write(row_no, col + 2, meter_input.totalizer_end, warning_bg if diff_e else '' )
                sheet.write(row_no, col + 3, meter_input.totalizer_difference, )
                sheet.write(row_no, col + 4, totalizer_difference, )
                sheet.write(row_no, col + 5, meter_input.weighbridge, center )
                sheet.write(row_no, col + 6, meter_input.tanker_empty_weight, )
                sheet.write(row_no, col + 7, meter_input.tanker_full_weight, )
                sheet.write(row_no, col + 8, meter_input.tanker_pure_weight, )
                sheet.write(row_no, col + 9, meter_input.document_no, )
                sheet.write(row_no, col + 10, meter_input.registration_no.registration_no, )
                totalizer_end = meter_input.totalizer_end
                row_no = next(row)


        row_no = next(row)
        sheet.write(row_no, col, f' باسکول ', bold_center_bg)
        sheet.write(row_no, col + 1, 'توتالایزر ابتدایی', bold_center_bg)
        sheet.write(row_no, col + 2, 'توتالایزر انتهایی', bold_center_bg)
        sheet.write(row_no, col + 3, 'مقدار میتر', bold_center_bg)
        sheet.write(row_no, col + 4, 'اختلاف توتالایزر', bold_center_bg)
        sheet.write(row_no, col + 5, 'باسکول دارد', bold_center_bg)
        sheet.write(row_no, col + 6, 'وزن خالی نفتکش', bold_center_bg)
        sheet.write(row_no, col + 7, 'وزن پر نفتکش', bold_center_bg)
        sheet.write(row_no, col + 8, 'وزن خالص نفتکش', bold_center_bg)
        sheet.write(row_no, col + 9, 'شماره سند', bold_center_bg)
        sheet.write(row_no, col + 10, 'شماره قرارداد', bold_center_bg)
        row_no = next(row)

        for index, meter_input in enumerate(report_data['totalizer_weighbridge']):
            diff_s = False
            diff_e = False
            totalizer_difference = 0


            sheet.write(row_no, col, meter_input.meter_no, bold_center)
            sheet.write(row_no, col + 1, meter_input.totalizer_start, warning_bg if diff_s else '')
            sheet.write(row_no, col + 2, meter_input.totalizer_end, warning_bg if diff_e else '' )
            sheet.write(row_no, col + 3, meter_input.totalizer_difference, )
            sheet.write(row_no, col + 4, totalizer_difference, )
            sheet.write(row_no, col + 5, meter_input.weighbridge, center )
            sheet.write(row_no, col + 6, meter_input.tanker_empty_weight, )
            sheet.write(row_no, col + 7, meter_input.tanker_full_weight, )
            sheet.write(row_no, col + 8, meter_input.tanker_pure_weight, )
            sheet.write(row_no, col + 9, meter_input.document_no, )
            sheet.write(row_no, col + 10, meter_input.registration_no.registration_no, )
            row_no = next(row)


        row_no = next(row)
        sheet.write(row_no, col + 1, '', warning_bg )
        sheet.write(row_no, col + 2, 'سلول نارنجی نشان دهنده اختلاف مابین پایان توتالایزیر یک سند و شروع تولاتایزر سند دیگر می باشد',  )

