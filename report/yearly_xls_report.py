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
class ReportSdPayanehNaftiMonthlyXlsReport(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.monthly_xls_report_template'
    _inherit = 'report.report_xlsx.abstract'


    # ########################################################################################
    def generate_xlsx_report(self, workbook, data, p):
        report = self.env['report.sd_payaneh_nafti.monthly_report_template']
        self.create_excel(workbook, report.get_report_values([], data))

    # ########################################################################################
    def create_excel(self, workbook, report_data ):
        if report_data.get('errors'):
            raise ValidationError(report_data['errors'])


        sheet = workbook.add_worksheet(f'گزارش ماهیانه')
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
        row_no = next(row)
        sheet.write(row_no, col + 1, 'گزارش ماهیانه', bold)
        sheet.write(row_no, col + 3, report_data['dates'][0], bold)
        sheet.write(row_no, col + 5, report_data['dates'][1], bold)
        next(row)
        row_no = next(row)


        sheet.write(row_no, col, f' ردیف ', bold_center_bg)
        sheet.write(row_no, col + 1, 'شماره نامه', bold_center_bg)
        sheet.write(row_no, col + 2, 'شماره قرارداد', bold_center_bg)
        sheet.write(row_no, col + 3, 'شماره حواله', bold_center_bg)
        sheet.write(row_no, col + 4, 'خریدار ', bold_center_bg)
        sheet.write(row_no, col + 5, 'مقدار ', bold_center_bg)
        sheet.write(row_no, col + 6, 'واحد ', bold_center_bg)
        sheet.write(row_no, col + 7, 'نوع ارسال ', bold_center_bg)
        sheet.write(row_no, col + 8, 'نوع فروش', bold_center_bg)
        sheet.write(row_no, col + 9, 'G.S.V. LITER', bold_center_bg)
        sheet.write(row_no, col + 10, 'G.S.V. BBLS', bold_center_bg)
        sheet.write(row_no, col + 11, 'M.T.', bold_center_bg)
        sheet.write(row_no, col + 12, 'تعداد تانکر', bold_center_bg)


        # return

        for row_data_line in report_data['row_data_lines']:
            col = 0
            row_no = next(row)

            sheet.write(row_no, col, row_data_line[0], bold_center)
            sheet.write(row_no, col + 1, row_data_line[1], bold_center)
            sheet.write(row_no, col + 2, row_data_line[2], bold_center)
            sheet.write(row_no, col + 3, row_data_line[3], bold_center)
            sheet.write(row_no, col + 4, row_data_line[4], bold_center)
            sheet.write(row_no, col + 5, row_data_line[5], bold_center)
            sheet.write(row_no, col + 6, row_data_line[6], bold_center)
            sheet.write(row_no, col + 7, row_data_line[7], bold_center)
            sheet.write(row_no, col + 8, row_data_line[8], bold_center)
            sheet.write(row_no, col + 9, row_data_line[9], bold_center)
            sheet.write(row_no, col + 10, row_data_line[10], bold_center)
            sheet.write(row_no, col + 11, row_data_line[11], bold_center)
            sheet.write(row_no, col + 12, row_data_line[12], bold_center)


