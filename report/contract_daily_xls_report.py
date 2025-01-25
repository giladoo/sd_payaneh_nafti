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
class ReportSdPayanehNaftiContractDailyXlsReport(models.AbstractModel):
    _name = 'report.sd_payaneh_nafti.contract_daily_xls_report_template'
    _inherit = 'report.report_xlsx.abstract'

    # ########################################################################################
    def generate_xlsx_report(self, workbook, data, p):
        report = self.env['report.sd_payaneh_nafti.contract_daily_report_template']
        self.create_excel(workbook, report.get_report_values([], data))

        # ########################################################################################

    def create_excel(self, workbook, report_data ):
        if report_data.get('errors'):
            raise ValidationError(report_data['errors'])
        sheet = workbook.add_worksheet(f'گزارش روزانه قرارداد')
        bold = workbook.add_format({'bold': True})
        center = workbook.add_format({'align': 'center'})
        right = workbook.add_format({'align': 'right'})
        bold_center = workbook.add_format({'bold': True,
                                           'size': 9,
                                           'align': 'center',
                                           'bg_color': '#bbbbbb',
                                           })
        format_left_to_right = workbook.add_format({"reading_order": 1})
        format_right_to_left = workbook.add_format({"reading_order": 2})
        num_format_3 = workbook.add_format({"num_format": '0.000'})
        num_format_3_bold = workbook.add_format({"num_format": '0.000','bold': True,})
        num_format_4 = workbook.add_format({"num_format": '0.0000'})
        num_format_4_bold = workbook.add_format({"num_format": '0.0000','bold': True,})
        sheet.set_column('A:Z', 10)
        sheet.set_column('B:B', 15)
        sheet.set_column('W:W', 15)
        sheet.right_to_left()
        row = iter(list(range(300)))
        col = 0
        doc_data = report_data.get('doc_data_list')[0][1]
        inputs = doc_data.get('inputs')
        pages_footer = doc_data.get('pages')
        page_count = doc_data.get('page_count')
        total = doc_data.get('total')
        contract_record = report_data.get('docs')

        sheet.write(next(row), col + 2, 'گزارش روزانه بارگیری نفتكش هاي زمینی میعانات گازی', bold)
        next(row)
        row_no = next(row)
        sheet.write(row_no, col + 1, 'خریدار:', bold)
        sheet.write(row_no, col + 2, contract_record.buyer.name, bold)

        row_no = next(row)
        sheet.write(row_no, col + 1, 'مقصد:', bold)
        sheet.write(row_no, col + 2, contract_record.destination.name, bold)

        row_no = next(row)
        sheet.write(row_no, col + 1, 'تاریخ بارگیری:', bold)
        sheet.write(row_no, col + 2, report_data['report_date'], bold)

        row_no = next(row)
        sheet.write(row_no, col + 1, 'شماره نامه:', bold)
        sheet.write(row_no, col + 2, contract_record.letter_no, bold)

        row_no = next(row)
        sheet.write(row_no, col + 1, 'شماره قرارداد:', bold)
        sheet.write(row_no, col + 2, contract_record.contract_no, bold)

        sheet.write(row_no, col + 1, 'شماره حواله:', bold)
        sheet.write(row_no, col + 2, contract_record.order_no, bold)

        row_no = next(row)
        sheet.write(row_no, col + 1, 'واحد:', bold)
        sheet.write(row_no, col + 2, doc_data.get('unit'), bold)

        row_no = next(row)
        sheet.write(row_no, col + 1, 'مقدار:', bold)
        sheet.write(row_no, col + 2, contract_record.amount, bold)

        row_no = next(row)
        sheet.write(row_no, col + 1, 'تحویل شده:', bold)
        sheet.write(row_no, col + 2, doc_data.get('used_amounts'), bold)

        row_no = next(row)
        sheet.write(row_no, col + 1, 'باقی مانده:', bold)
        sheet.write(row_no, col + 2, doc_data.get('remain_amounts'), bold)
        next(row)
        next(row)
        col_index = 1

        for index, page_data in enumerate(inputs):
            row_no = next(row)
            sheet.write(row_no, col, f'page {index + 1} of {len(inputs)}' )
            row_no = next(row)
            for r in range(row_no, row_no + 3):
                for c in range(col, col + 23):
                    sheet.write(r, c, '', bold_center)
            sheet.write(row_no, col, 'ردیف', bold_center)
            sheet.write(row_no, col + 1, 'پلاک', bold_center)
            sheet.write(row_no, col + 2, 'مخزن', bold_center)
            sheet.write(row_no, col + 3, 'SP.GR', bold_center)
            sheet.write(row_no + 1, col + 3, '60/60', bold_center)
            sheet.write(row_no, col + 4, 'API', bold_center)
            sheet.write(row_no, col + 5, 'T', bold_center)
            sheet.write(row_no + 1, col + 5, '(C)', bold_center)
            sheet.write(row_no, col + 6, 'T', bold_center)
            sheet.write(row_no + 1, col + 6, '(F)', bold_center)
            sheet.write(row_no, col + 7, 'P', bold_center)
            sheet.write(row_no + 1, col + 7, '(بار)', bold_center)
            sheet.write(row_no, col + 8, 'P', bold_center)
            sheet.write(row_no + 1, col + 8, '(PSI)', bold_center)
            sheet.write(row_no, col + 9, 'نوع', bold_center)
            sheet.write(row_no + 1, col + 9, 'بارگیری', bold_center)
            sheet.write(row_no, col + 10, 'میتر', bold_center)
            sheet.write(row_no, col + 11, 'توالایزر آغازین', bold_center)
            sheet.write(row_no + 1, col + 11, 'وزن خالی نفتکش', bold_center)
            sheet.write(row_no, col + 12, 'توالایزر پایانی', bold_center)
            sheet.write(row_no + 1, col + 12, 'وزن پر نفتکش', bold_center)
            sheet.write(row_no, col + 13, 'اختلاف توتالایزر', bold_center)
            sheet.write(row_no + 1, col + 13, 'وزن خالص', bold_center)
            sheet.write(row_no, col + 14, 'K-FACTOR', bold_center)
            sheet.write(row_no, col + 15, 'C.T.L 6A', bold_center)
            sheet.write(row_no, col + 16, 'C.P.L 6A', bold_center)
            sheet.write(row_no, col + 17, 'T.O.V', bold_center)
            sheet.write(row_no + 1, col + 17, '(Litter) ', bold_center)
            sheet.write(row_no + 2, col + 17, '60C ', bold_center)
            sheet.write(row_no, col + 18, 'G.S.V', bold_center)
            sheet.write(row_no + 1, col + 18, '(Litter)', bold_center)
            sheet.write(row_no + 2, col + 18, '60C', bold_center)
            sheet.write(row_no, col + 19, 'G.S.V', bold_center)
            sheet.write(row_no + 1, col + 19, '(BBLS)', bold_center)
            sheet.write(row_no + 2, col + 19, '60C', bold_center)
            sheet.write(row_no, col + 20, 'TAB. 13', bold_center)
            sheet.write(row_no, col + 21, 'M. Tons', bold_center)
            sheet.write(row_no, col + 22, 'Loading No', bold_center)
            next(row)
            next(row)
            row_no = next(row)
            for line_rec in page_data:
                # print(f'>>>>>>>>>   line  \n {line_rec}')

                sheet.write(row_no, col, col_index, center )
                # sheet.write(row_no, col + 1, f'[ {line_rec.plate_2} {line_rec.plate_3} {line_rec.plate_4} ][ {line_rec.plate_1} ]', format_right_to_left)
                sheet.write(row_no, col + 1, f'[ {line_rec.plate_1} ] [ {line_rec.plate_2} {line_rec.plate_3} {line_rec.plate_4} ]',)
                sheet.write(row_no, col + 2, line_rec.centralized_container, center)
                sheet.write(row_no, col + 3, line_rec.sp_gr, center)
                sheet.write(row_no, col + 4, line_rec.api_a, center)
                sheet.write(row_no, col + 5, line_rec.temperature, center)
                sheet.write(row_no, col + 6, line_rec.temperature_f, center)
                sheet.write(row_no, col + 7, line_rec.pressure, center)
                sheet.write(row_no, col + 8, line_rec.pressure_psi, center)
                sheet.write(row_no, col + 9, 'باسکول' if line_rec.weighbridge == 'yes' else 'میتر', center)
                sheet.write(row_no, col + 10, '#' if line_rec.weighbridge == 'yes' else line_rec.meter_no, center)
                sheet.write(row_no, col + 11, line_rec.tanker_empty_weight if line_rec.weighbridge == 'yes' else line_rec.totalizer_start, )
                sheet.write(row_no, col + 12, line_rec.tanker_full_weight if line_rec.weighbridge == 'yes' else line_rec.totalizer_end, )
                sheet.write(row_no, col + 13, line_rec.tanker_pure_weight if line_rec.weighbridge == 'yes' else line_rec.totalizer_difference, )
                sheet.write_number(row_no, col + 14, line_rec.correction_factor, num_format_4 )
                sheet.write(row_no, col + 15, round(line_rec.ctl, 5) )
                sheet.write(row_no, col + 16, round(line_rec.cpl, 5) )
                sheet.write(row_no, col + 17, line_rec.final_tov_l, )
                sheet.write(row_no, col + 18, line_rec.final_gsv_l, )
                sheet.write(row_no, col + 19, int(line_rec.final_gsv_b), )
                sheet.write(row_no, col + 20, round(line_rec.tab_13, 5) )
                sheet.write_number(row_no, col + 21, line_rec.final_mt, num_format_3 )
                sheet.write(row_no, col + 22, line_rec.loading_no, )

                col_index += 1
                row_no = next(row)
            for i in range(index + 1):
                sheet.merge_range(row_no, col + 8, row_no, col + 12, f' جمع صفحه {i + 1} اختلاف توتالایزر از بارگیری میتر ', bold )
                sheet.write(row_no, col + 13, pages_footer[i].get('totalizer_diff_sum') , bold)
                sheet.merge_range(row_no, col + 15, row_no, col + 16, f' جمع صفحه {i + 1} ', bold )

                sheet.write(row_no, col + 17, pages_footer[i].get('final_tov_l_sum'), bold )
                sheet.write(row_no, col + 18, pages_footer[i].get('final_gsv_l_sum') , bold)
                sheet.write(row_no, col + 19, int(pages_footer[i].get('final_gsv_b_sum')) , bold)
                sheet.write_number(row_no, col + 21, pages_footer[i].get('final_mt_sum'), num_format_3_bold )
                row_no = next(row)
                if i + 1 == page_count:
                    sheet.merge_range(row_no, col + 8, row_no, col + 12, 'جمع كل اختلاف توتالایزر از بارگیری میتر' , bold)
                    sheet.write(row_no, col + 13, total.get('totalizer_diff_sum'), bold)
                    sheet.merge_range(row_no, col + 15, row_no, col + 16, 'جمع كل' , bold)

                    sheet.write(row_no, col + 17, total.get('final_tov_l_sum'), bold)
                    sheet.write(row_no, col + 18, total.get('final_gsv_l_sum'), bold)
                    sheet.write(row_no, col + 19, int(total.get('final_gsv_b_sum')), bold)
                    sheet.write_number(row_no, col + 21, total.get('final_mt_sum'), num_format_3_bold)

            next(row)
            next(row)
            row_no = next(row)


