# -*- coding: utf-8 -*-
from datetime import  datetime, timedelta
import pytz

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from colorama import Fore

class SdPayanehNaftiMeterData(models.Model):
    _name = 'sd_payaneh_nafti.meter_data'
    _description = 'sd_payaneh_nafti.meter_data'
    _rec_name = 'report_date'
    _order = 'report_date, meter'

    report_date = fields.Date(required=True,)
    meter = fields.Integer(required=True,)
    first_totalizer = fields.Integer(compute='_meter_amounts')
    last_totalizer = fields.Integer(compute='_meter_amounts')
    meter_amounts = fields.Integer(compute='_meter_amounts')
    description = fields.Char()

    def _meter_amounts(self):
        for rec in self:
            input_info = self.env['sd_payaneh_nafti.input_info'].search([('loading_date', '=', rec.report_date),
                                                                         ('meter_no', '=', rec.meter),])
            # todo: maximum number of totalizer is 99,999,999. It means that sometimes the totalizer_end would be
            #  less than totalizer_start. This is corrected on loading_info form. But it is needed to be corrected
            #  on meter reprot too.

            totalizer_start = list([ii.totalizer_start for ii in input_info])
            totalizer_end = list([ii.totalizer_end for ii in input_info])
            rec.first_totalizer = min(totalizer_start) if totalizer_start else 0
            rec.last_totalizer = max(totalizer_end) if totalizer_end else 0
            rec.meter_amounts = rec.last_totalizer - rec.first_totalizer

    @api.onchange('description')
    def _description_changed(self):
        self.write({'description': self.description})

class SdPayanehNaftiMeterComments(models.Model):
    _name = 'sd_payaneh_nafti.meter_comments'
    _description = 'sd_payaneh_nafti.meter_comments'
    _rec_name = 'comments'
    _order = 'comment_date desc'

    comment_date = fields.Date(default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz'))))
    comments = fields.Html()
