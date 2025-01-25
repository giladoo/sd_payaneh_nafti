# -*- coding: utf-8 -*-
from datetime import  datetime, timedelta
# import random

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from colorama import Fore

class SdPayanehNaftiContractors(models.Model):
    _name = 'sd_payaneh_nafti.contractors'
    _description = 'sd_payaneh_nafti.contractors'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(required=True, tracking=True,)
    description = fields.Char()


