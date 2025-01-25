# -*- coding: utf-8 -*-
from datetime import  datetime, timedelta
import json

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
from colorama import Fore
import jdatetime
import math
import logging
import pytz


class SdPayanehNaftiPlate1(models.Model):
    _name = 'sd_payaneh_nafti.plate1'
    _description = 'sd_payaneh_nafti.plate1'

    name = fields.Char(translate=True, tracking=True)


class SdPayanehNaftiPlate2(models.Model):
    _name = 'sd_payaneh_nafti.plate2'
    _description = 'sd_payaneh_nafti.plate2'

    name = fields.Char(translate=True, tracking=True)


class SdPayanehNaftiPlate3(models.Model):
    _name = 'sd_payaneh_nafti.plate3'
    _description = 'sd_payaneh_nafti.plate3'

    name = fields.Char(translate=True, tracking=True)

class SdPayanehNaftiPlate4(models.Model):
    _name = 'sd_payaneh_nafti.plate4'
    _description = 'sd_payaneh_nafti.plate4'

    name = fields.Char(translate=True, tracking=True)


