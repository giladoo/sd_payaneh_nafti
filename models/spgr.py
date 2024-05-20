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
    _order = 'id desc'

    def _spgr_default(self, param):
        return self.search([], order="id desc", limit=1)[param]

    active = fields.Boolean(default=True)
    spgr = fields.Float(required=True, digits=[1, 4], default=lambda self: self._spgr_default('spgr'))
    spgr_date = fields.Date(required=True, default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz', 'Asia/Tehran'))) )
    api_a = fields.Float(digits=[1, 2], store=True, required=True,)
    centralized_container = fields.Selection([('a', 'A'),
                                              ('b', 'B'),
                                              ('c', 'C'),
                                              ('d', 'D'),
                                              ('e', 'E'),
                                              ('f', 'F'),
                                              ('g', 'G'),
                                              ('h', 'H'),
                                              ], required=True, tracking=True, default=lambda self: self._spgr_default('centralized_container'))
    vapour_pressure = fields.Float(required=True, default=lambda self: self._spgr_default('vapour_pressure'))
    salt_content = fields.Float(required=True, default=lambda self: self._spgr_default('salt_content'))
    mercaptans = fields.Integer(required=True, default=lambda self: self._spgr_default('mercaptans'))
    sulphur = fields.Float(required=True, digits=[1, 3], default=lambda self: self._spgr_default('sulphur'))

    # h2s = fields.Selection([], required=False, default=lambda self: self._spgr_default('h2s'))
    h2s = fields.Char(required=True, default=lambda self: self._spgr_default('h2s'))
    # water_content = fields.Selection([], required=False, default=lambda self: self._spgr_default('water_content'))
    water_content = fields.Char(required=True, default=lambda self: self._spgr_default('water_content'))

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

