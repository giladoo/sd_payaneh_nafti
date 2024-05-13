# -*- coding: utf-8 -*-
from datetime import  datetime, timedelta
# import random

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from colorama import Fore
from odoo.modules.module import get_module_resource
import base64
from PIL import Image
class SdPayanehNaftiTrucks(models.Model):
    _name = 'sd_payaneh_nafti.trucks'
    _description = 'sd_payaneh_nafti.trucks'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    black_list = fields.Boolean(tracking=True)
    plate_1 = fields.Char(required=True, tracking=True,)
    plate_2 = fields.Char(required=True, tracking=True,)
    plate_3 = fields.Char(required=True, tracking=True,)
    plate_4 = fields.Char(required=True, tracking=True,)
    card_no = fields.Char(tracking=True)
    front_container = fields.Integer(required=True, tracking=True, default=12000)
    middle_container = fields.Integer(required=True, tracking=True, default=8000)
    back_container = fields.Integer(required=True, tracking=True, default=12000)
    total = fields.Integer(compute='_total')
    description = fields.Html()

    @api.onchange('front_container', 'middle_container', 'back_container')
    def _total(self):
        # It calculates the total amount of tanker containers
        for rec in self:
            rec.total = rec.front_container + rec.middle_container + rec.back_container
    @api.constrains('name')
    def _check_project_unique(self):
        record_count = self.search_count([('name', '=', self.name),
                                           ('id', '!=', self.id)])
        if record_count > 0:
            raise ValidationError("Record already exists!")

    @api.model
    def create(self, vals):
        vals['name'] = f'[ {vals.get("plate_4")}  {vals.get("plate_3")}  {vals.get("plate_2")} ]  [ {vals.get("plate_1")} ]'
        return super(SdPayanehNaftiTrucks, self).create(vals)

    def write(self, vals):
        vals['name'] = f'[ {vals.get("plate_4", self.plate_4)}  {vals.get("plate_3", self.plate_3)}  {vals.get("plate_2", self.plate_2)} ]  [ {vals.get("plate_1", self.plate_1)} ] '
        return super(SdPayanehNaftiTrucks, self).write(vals)

    @api.onchange('plate_1')
    def _plate1(self):
        a = self.plate_1
        if a and (not a.isdigit() or ( a.isdigit() and (int(a) > 100 or int(a) < 11))):
            raise ValidationError(_(f'[{a}] Not acceptable'))
    @api.onchange('plate_2')
    def _plate2(self):
        a = self.plate_2
        if a and (not a.isdigit() or ( a.isdigit() and (int(a) > 1000 or int(a) < 111))):
            raise ValidationError(_(f'[{a}] Not acceptable'))

    @api.onchange('plate_3')
    def _plate3(self):
        a = self.plate_3
        letters = [ 'ع', 'ن', ]
        if a and (a.isdigit() or a not in letters ) :
            raise ValidationError(_(f'[{a}] Not in \n{letters}'))

    @api.onchange('plate_4')
    def _plate4(self):
        a = self.plate_4
        if a and (not a.isdigit() or ( a.isdigit() and (int(a) > 100 or int(a) < 11))):
            raise ValidationError(_(f'[{a}] Not acceptable'))


