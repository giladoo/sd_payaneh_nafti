# -*- coding: utf-8 -*-
from datetime import  datetime, timedelta
# import random

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from colorama import Fore


class SdPayanehNaftiDestinations(models.Model):
    _name = 'sd_payaneh_nafti.destinations'
    _description = 'sd_payaneh_nafti.destinations'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required=True, translate=True, tracking=True)
    description = fields.Char()


