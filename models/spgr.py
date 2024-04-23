# -*- coding: utf-8 -*-
from datetime import  datetime, timedelta
import pytz

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SdPayanehNaftiSpgr(models.Model):
    _name = 'sd_payaneh_nafti.spgr'
    _description = 'sd_payaneh_nafti.spgr'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'spgr'

    active = fields.Boolean(default=True)
    spgr = fields.Float(required=True, digits=[1, 4])
    spgr_date = fields.Date(required=True, default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz', 'Asia/Tehran'))) )
    api_a = fields.Float(digits=[1, 2], store=True)
    centralized_container = fields.Selection([('a', 'A'),
                                              ('b', 'B'),
                                              ('c', 'C'),
                                              ('d', 'D'),
                                              ('e', 'E'),
                                              ('f', 'F'),
                                              ('g', 'G'),
                                              ('h', 'H'),
                                              ], required=True, default='h', tracking=True)
    vapour_pressure = fields.Float(required=True)
    salt_content = fields.Float(required=True)
    mercaptans = fields.Float(required=True)
    h2s = fields.Selection([('trace', 'TRACE')], default='trace', required=True)
    sulphur = fields.Float(required=True)
    water_content = fields.Selection([('nil', 'NIL')], default='nil', required=True)

    description = fields.Char()

    @api.model
    def create(self, vals):
        if vals.get('spgr', 0) > 1.1:
            raise ValidationError(_(f'{vals.get("spgr")} is not accepted!'))
        active_records = self.search([('active', '=', True)])
        for rec in active_records:
            rec.active = False
        return super(SdPayanehNaftiSpgr, self).create(vals)

    @api.depends('spgr')
    @api.onchange('spgr')
    def change_spgr(self):
        if self.spgr > 1.1:
            raise ValidationError(_(f'{self.spgr} is not accepted!'))
        self.api_a = 141.5 / self.spgr - 131.5 if self.spgr != 0 else 0

