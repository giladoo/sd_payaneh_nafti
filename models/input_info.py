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


cpl_counter = 0
def _cpl_counter():
    global cpl_counter
    cpl_counter += 1
    return cpl_counter
class SdPayanehNaftiInputInfo(models.Model):
    _name = 'sd_payaneh_nafti.input_info'
    _description = 'sd_payaneh_nafti.input_info'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'document_no desc'
    _rec_name = 'document_no'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('loading_permit', 'Loading Permit'),
        ('loading_info', 'Loading Info'),
        ('cargo_document', 'Cargo Doc'),
        ('done', 'Done'),
        ('driver_block_list', 'Driver'),
        ('truck_black_list', 'Truck'),
        ('out_of_date', 'Out of Date'),
        ('amount_limit', 'Amount Limit'),
        ('finished', 'Finished'),
        ],
        string='Status', index=True, readonly=True, tracking=True,
        copy=False, default='draft', required=True, group_expand='_expand_groups', )
    shift = fields.Selection([
        ('shift_1', 'Shift 1'),
        ('shift_2', 'Shift 2'),
        ('shift_3', 'Shift 3'),
        ('shift_4', 'Shift 4'),
        ('shift_5', 'Shift 5'),
        ('shift_6', 'Shift 6'),

        ],
        string='Shift', index=True, tracking=True,
        copy=False, default=lambda self: self.shift_selector(), required=True, )
    remain_amount = fields.Float(compute='_remain_amount')
    remain_amount_approx = fields.Float(compute='_remain_amount')
    amount = fields.Float()
    document_no = fields.Integer(required=True, copy=False, readonly=True, tracking=True,
                                 default=lambda self: 0)
    # document_no = fields.Integer(required=True, copy=False, readonly=False, tracking=True,
    #                              default=lambda self: self.search([], order='document_no desc', limit=1).document_no + 1)
    request_date = fields.Date(default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz', 'Asia/Tehran'))),
                               required=True, tracking=True)
    registration_no = fields.Many2one('sd_payaneh_nafti.contract_registration', required=True, tracking=True,
                                      default=lambda self: self.env.context.get('registration_no', False))
    date_validation = fields.Boolean(related='registration_no.date_validation', store=False)
    contract_no = fields.Char(related='registration_no.contract_no', tracking=True,)
    order_no = fields.Char(related='registration_no.order_no')
    buyer = fields.Many2one(related='registration_no.buyer')
    contractors = fields.Many2many(related='registration_no.contractors')
    contractor = fields.Many2one('sd_payaneh_nafti.contractors', required=True, tracking=True,)
    driver = fields.Many2one('sd_payaneh_nafti.drivers', required=True, tracking=True,)
    driver_black_list = fields.Boolean(related='driver.black_list')
    card_no = fields.Char(related='driver.card_no')
    truck_no = fields.Many2one('sd_payaneh_nafti.trucks', required=True, tracking=True,)
    truck_black_list = fields.Boolean(related='truck_no.black_list')
    plate_1 = fields.Char(related='truck_no.plate_1',)
    plate_2 = fields.Char(related='truck_no.plate_2',)
    plate_3 = fields.Char(related='truck_no.plate_3',)
    plate_4 = fields.Char(related='truck_no.plate_4',)
    # front_container = fields.Integer(related='truck_no.front_container')
    # middle_container = fields.Integer(related='truck_no.middle_container')
    # back_container = fields.Integer(related='truck_no.back_container')
    front_container = fields.Integer(required=True, tracking=True,)
    middle_container = fields.Integer(required=True, tracking=True,)
    back_container = fields.Integer(required=True, tracking=True,)
    total = fields.Integer(compute='_total')
    centralized_container = fields.Selection([('a', 'A'),
                                              ('b', 'B'),
                                              ('c', 'C'),
                                              ('d', 'D'),
                                              ('e', 'E'),
                                              ('f', 'F'),
                                              ('g', 'G'),
                                              ('h', 'H'),
                                              ], required=True, tracking=True, )

    loading_no = fields.Char(copy=False, readonly=False, tracking=True, )
    # todo: timezone
    loading_date = fields.Date(copy=False, string='Loading Date', readonly=False, default=lambda self: self.request_date, tracking=True)
    loading_info_date = fields.Date(copy=False, tracking=True,
                                    default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz', 'Asia/Tehran'))))
    # driver = fields.Char(required=True,)

    sp_gr = fields.Float( string='SP. GR.', required=True, default=0.3, store=True, readonly=True, tracking=True)
    # sp_gr = fields.Many2one('sd_payaneh_nafti.spgr', string='SP. GR.', required=True, default=0.7252)
    temperature = fields.Float(string='Temp. (C)', required=True, default=30, tracking=True, digits=(12, 1))
    temperature_f = fields.Float(string='Temp. (F)', compute='_temperature_f', digits=(12, 1))
    pressure = fields.Float(string='Pressure (bar)', required=True, default=2.5, tracking=True)
    pressure_psi = fields.Integer(compute='_pressure_psi', digits=(2, 0))
    meter_no = fields.Selection([ ('1', '1'),
                                  ('2', '2'),
                                  ('3', '3'),
                                  ('4', '4'),
                                  ('5', '5'),
                                  ('6', '6'),
                                  ('7', '7'),
                                  ('8', '8'),
                                  ('0', 'Master'),
                                  ], required=False, tracking=True,)
    totalizer_lasts = fields.Html(required=False, readonly=True)
    totalizer_start = fields.Integer(required=False, tracking=True,)
    totalizer_end = fields.Integer(required=False, tracking=True, help="The last Totalizer End as start")
    totalizer_difference = fields.Integer(required=False, compute='_totalizer_difference')
    weighbridge = fields.Selection([('no', 'No'), ('yes', 'Yes')], default='no', tracking=True)
    tanker_empty_weight = fields.Integer(required=False, tracking=True,)
    tanker_full_weight = fields.Integer(required=False, tracking=True,)
    tanker_pure_weight = fields.Integer(required=False, compute='_tanker_pure_weight')
    evacuation_box_seal = fields.Char(required=False,  tracking=True)
    compartment_1 = fields.Char(required=False,  tracking=True)
    compartment_2 = fields.Char(required=False,  tracking=True)
    compartment_3 = fields.Char(required=False, tracking=True)
    correction_factor = fields.Float(digits=(12, 5), required=True, default=1.0, tracking=True)
    # api_box_locker = fields.Many2one('sd_payaneh_nafti.lockers')
    # compartment_locker_1 = fields.Many2one('sd_payaneh_nafti.lockers')
    # compartment_locker_2 = fields.Many2one('sd_payaneh_nafti.lockers')
    # compartment_locker_3 = fields.Many2one('sd_payaneh_nafti.lockers')

    api_a = fields.Float(string='API', compute='_api_a')
    ctl = fields.Float(string='CTL', compute='_ctl_cpl', )
    cpl = fields.Float(string='CPL', compute='_ctl_cpl', )
    tab_13 = fields.Float(string='TAB.13', digits=(12, 5), compute='_tab_13')
    # this variables are useless
    meter_tov_l = fields.Float(string='Meter T.O.V Liter')
    meter_gsv_l = fields.Float(string='Meter G.S.V Liter')
    meter_gsv_b = fields.Float(string='Meter G.S.V BBL', digits=[8, 4])
    meter_mt = fields.Float(string='Meter M.T.')
    wb_tov_l = fields.Float(string='WB T.O.V Liter')
    wb_gsv_l = fields.Float(string='WB G.S.V Liter')
    wb_gsv_b = fields.Float(string='WB G.S.V BBL', digits=[8, 4])
    wb_mt = fields.Float(string='WB M.T.')

    final_tov_l = fields.Float(string='Final T.O.V Liter', compute='_finals', digits=[8, 0])
    final_gsv_l = fields.Float(string='Final G.S.V Liter', compute='_finals', digits=[8, 0])
    final_gsv_b = fields.Float(string='Final G.S.V BBL', compute='_finals', )
    final_mt = fields.Float(string='Final M.T.', compute='_finals', digits=[8, 3])
    cpl_counter = fields.Integer(default=0)

    cqq = fields.Many2one('sd_payaneh_nafti.spgr')

    def shift_selector(self):
        shift = 1
        the_time = datetime.now(pytz.timezone(self.env.context.get('tz', 'Asia/Tehran'))).time()
        if the_time < the_time.replace(hour=7, minute=0, second=0, microsecond=0):
            shift = 1
        elif the_time < the_time.replace(hour=9, minute=30, second=0, microsecond=0):
            shift = 2
        elif the_time < the_time.replace(hour=12, minute=0, second=0, microsecond=0):
            shift = 3
        elif the_time < the_time.replace(hour=18, minute=0, second=0, microsecond=0):
            shift = 4
        elif the_time < the_time.replace(hour=21, minute=0, second=0, microsecond=0):
            shift = 5
        elif the_time >= the_time.replace(hour=21, minute=0, second=0, microsecond=0):
            shift = 6

        return f'shift_{shift}'
    @api.onchange('truck_no')
    def _truck_changed(self):
        self.front_container = self.truck_no.front_container
        self.middle_container = self.truck_no.middle_container
        self.back_container = self.truck_no.back_container

    @api.onchange('evacuation_box_seal')
    def onchange_evacuation_box_seal(self):
        locker = self.evacuation_box_seal
        if locker and len(locker) > 6:
            locker_base = locker[:3]
            locker_number = locker[3:]
            if locker_number.isdigit():
                locker_number = int(locker_number)
                self.compartment_1 = f'{locker_base}{locker_number + 1}'
                self.compartment_2 = f'{locker_base}{locker_number + 2}'
                self.compartment_3 = f'{locker_base}{locker_number + 3}'
            else:
                logging.error(f'[onchange_evacuation_box_seal]: {locker} : {locker_number} is not number ')
        else:
            logging.error(f'[onchange_evacuation_box_seal]: Length of [{locker}] is less than 6')

    @api.onchange('meter_no')
    def onchange_meter_no(self):
        last_input = self.search([('meter_no', '=', self.meter_no),
                                  ('totalizer_end', '>', 0)],
                                 order='document_no desc,totalizer_end desc', limit=5)
        if last_input:
            self.totalizer_start = last_input[0].totalizer_end
            totalizer_lasts = []
            totalizer_lasts.append(f'<div class="row border-top border-bottom mx-0 sd_ltr">'
                                   f'<div class="col px-1">Document No</div>'
                                   f'<div class="col px-1">Totalizer End</div>'
                                   f'</div>')
            for rec in last_input:
                totalizer_lasts.append(f'<div class="row border-bottom mx-0 sd_ltr">'
                                       f'<div class="col px-1">{rec.document_no}</div>'
                                       f'<div class="col px-1">{rec.totalizer_end:,}</div>'
                                       f'</div>')
            self.totalizer_lasts = ''.join(totalizer_lasts)
            self.totalizer_lasts = f'<div class="sd_ltr" style="font-family: sarif">{self.totalizer_lasts}<div>'

    @api.onchange('document_no')
    def onchange_document_no(self):
        self.set_spgr()

    @api.depends('registration_no',)
    @api.onchange('registration_no', 'front_container', 'middle_container', 'back_container')
    def _on_registration_change(self):
        self._remain_amount()

    @api.onchange('weighbridge')
    def _onchange_weighbridge(self):
        self._finals()
        self._weighbridge_change()

    @api.onchange('temperature')
    def _onchange_temperature(self):
        self._temperature_f()
        self._ctl_cpl()

    @api.onchange('sp_gr')
    def _onchange_spgr(self):
        self._api_a()
        self._tab_13()
        self._ctl_cpl()

    @api.onchange('pressure')
    def _onchange_pressure(self):
        self._pressure_psi()
        self._ctl_cpl()

    def set_spgr(self):
        # if not self.env.user.has_group('sd_payaneh_nafti.group_sd_payaneh_nafti_operators'):
        #     return
        spgr = self.env['sd_payaneh_nafti.spgr'].search([], order='id desc', limit=1)
        if len(spgr) == 1:
            self.sp_gr = spgr.spgr
            self.centralized_container = spgr.centralized_container
            self.cqq = spgr if (self.request_date > date(2024, 4, 19)) else False
        else:
            raise ValidationError(_('Add a "SP.GR." from the main menu'))

    @api.depends('shift')
    def _remain_amount(self):
        # print('============   _remain_amount  =============')
        # select registration_no of this records
        registration_list = []
        for rec in self:
            registration_list.append(rec.registration_no.id)

        all_inputs = self.search([('registration_no', 'in', registration_list)])
        for rec in self:
            final_gsv_b = 0
            final_mt = 0
            requested_approx_amount = 0

            # todo: this algorithm might be too slow. I calculate's the remain amount each time for each of the records.
            #   It can be done for each of them and be stored on the record.

            # In case of new record creation
            if rec.id and str(rec.id).isdigit():
                # inputs = self.search([('id', '!=', False), ('id', '<=', rec.id), ('registration_no', '=', rec.registration_no.id), ])
                inputs = list([re for re in all_inputs if re.id != False and re.id <= rec.id and re.registration_no.id == rec.registration_no.id])
            else:
                # inputs = self.search([('registration_no', '=', rec.registration_no.id),])
                inputs = list([re for re in all_inputs if re.registration_no.id == rec.registration_no.id ])

            #  if there is no loading info, calculate based on sum of the containers amount
            if not rec.final_mt:
                total = rec.front_container + rec.middle_container + rec.back_container
                # final_tov_l = round((rec.cpl * total * rec.correction_factor), 0 )
                final_gsv_l = round((rec.cpl * rec.ctl * total * rec.correction_factor), 0 )
                final_gsv_b = final_gsv_l / 158.987
                final_mt = round(final_gsv_b * rec.tab_13, 3)

            # calculate the used amounts basd on contract unit type; barrel or metric/tone
            if rec.registration_no.unit == 'barrel':
                used_amounts = sum([ua.final_gsv_b for ua in inputs])
                requested_approx_amount = final_gsv_b
            elif rec.registration_no.unit == 'metric_ton':
                used_amounts = sum([ua.final_mt for ua in inputs])
                requested_approx_amount = final_mt
            else:
                used_amounts = 0


            amount = rec.registration_no.amount if rec.registration_no.init_amount == 0 else rec.registration_no.init_amount
            rec.remain_amount = amount - used_amounts
            rec.remain_amount_approx = amount - used_amounts - requested_approx_amount
            if rec.state != 'finished':
                rec.amount = rec.final_gsv_b if rec.registration_no.unit == 'barrel' else rec.final_mt



    def _finals(self):
        # calculate the final amounts based on the totalizer or the tanker weight
        for rec in self:
            # print(f'=======> {rec.document_no} rec.cpl:{rec.cpl}  rec.ctl:{rec.ctl} ')
            if rec.weighbridge == 'yes':
                # final_mt = round(rec.tanker_pure_weight / 1000, 3)
                # final_gsv_b = final_mt / rec.tab_13
                # final_gsv_l = round(final_gsv_b * 158.987, 0)
                # final_tov_l = round((final_gsv_l / rec.ctl) / rec.cpl, 0)

                final_mt = round(rec.tanker_pure_weight / 1000, 3)
                final_gsv_l = round((rec.tanker_pure_weight / 6.28981) / rec.tab_13, 0)

                final_gsv_b = final_gsv_l / 158.987
                final_tov_l = round((final_gsv_l / rec.ctl) / rec.cpl, 0)
            else:
                final_tov_l = round((rec.cpl * rec.totalizer_difference * rec.correction_factor), 0 )
                final_gsv_l = round((rec.cpl * rec.ctl * rec.totalizer_difference * rec.correction_factor), 0 )
                final_gsv_b = final_gsv_l / 158.987
                final_mt = round(final_gsv_b * rec.tab_13, 3)

            rec.final_mt = final_mt
            rec.final_gsv_b = final_gsv_b
            rec.final_gsv_l = final_gsv_l
            rec.final_tov_l = final_tov_l

    def _temperature_f(self):
        # calculates the temperature based on Fahrenheit degree
        for rec in self:
            rec.temperature_f = rec.temperature * 9 / 5 + 32

    def _api_a(self):
        # calculates the API
        for rec in self:
            api_a = 141.5 / rec.sp_gr - 131.5 if rec.sp_gr else 0
            # The api calculation had changed on 1401 mehr Excel file. The document 3215 is the first one on 1401 mehr.
            rec.api_a = round(api_a, 2) if rec.registration_no.loading_type == 'internal' or rec.document_no < 3215 else round(api_a, 1)

    def _tab_13(self):
        # Calculates the TAB.13
        for rec in self:
            rec.tab_13 = ((141.3819577 / (rec.api_a + 131.5)) - 0.001199407795) * 0.1589872949


    def _pressure_psi(self):
        # Calculates the pressure based on PSI
        for rec in self:
            rec.pressure_psi = round(rec.pressure * 14.5038, 0)

    def _ctl_cpl(self):
        # takes the constant parameters from setting page
        k_0 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.k_0'))
        k_1 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.k_1'))
        k_2 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.k_2'))
        delta_60 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.delta_60'))
        tref = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.tref'))
        param_a = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_a'))
        param_b = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_b'))
        param_c = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_c'))
        param_d = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_d'))
        param_ai1 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_ai1'))
        param_ai2 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_ai2'))
        param_ai3 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_ai3'))
        param_ai4 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_ai4'))
        param_ai5 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_ai5'))
        param_ai6 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_ai6'))
        param_ai7 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_ai7'))
        param_ai8 = float(self.env['ir.config_parameter'].sudo().get_param('sd_payaneh_nafti.param_ai8'))

        # logging.error(f'%%%%%%%%%%%% > cpl_counter: {_cpl_counter()} k_0: {k_0} delta_60: {delta_60} ')
        # Calculates CPL and CTL which they will be used to calculate the other parameters
        for rec in self:
            try:
                temperature = round(rec.temperature, 0)
                temperature_f = rec.temperature_f

                rec_pi = (141.5 / (rec.api_a + 131.5)) * 999.016
                rec_a = (delta_60 / 2) * (((k_0 / rec_pi) + k_1) * (1 / rec_pi) + k_2)
                rec_b = ((2 * k_0) + (k_1 * rec_pi)) / ((k_0 + ((k_2 * rec_pi) + k_1) * rec_pi))
                rec_pi_star = rec_pi * (1 + ((math.exp((rec_a * (1 + (0.8 * rec_a)))) - 1) / (1 + rec_a * (1 + (0.6 * rec_a)) * rec_b)))
                alpha_60 = (((k_0 / rec_pi_star) + k_1) * (1 / rec_pi_star)) + k_2
                t_star_prime = ((temperature_f-32)/1.8)/630
                t_star_zegond = (param_ai1+((param_ai2+((param_ai3+((param_ai4+((param_ai5+((param_ai6+((param_ai7+(param_ai8*t_star_prime))*t_star_prime))*t_star_prime))*t_star_prime))*t_star_prime))*t_star_prime))*t_star_prime))*t_star_prime
                # t_star = ((temperature-((param_ai1+(param_ai2+(param_ai3+(param_ai4+(param_ai5+(param_ai6+(param_ai7+param_ai8*(temperature/630))*(temperature/630))*(temperature/630))*(temperature/630))*(temperature/630))*(temperature/630))*(temperature/630))*(temperature/630)))*1.8)+32
                # caculation sheet, T* column
                t_star = ((((
                                   (temperature_f-32) / 1.8) -
                           ((param_ai1+(param_ai2+(param_ai3+(param_ai4+(param_ai5+(param_ai6+
                                                                                    (param_ai7+param_ai8 * (((temperature_f-32) / 1.8) / 630)) *
                                                                                    (((temperature_f-32) / 1.8) / 630)
                                                                                    ) * (((temperature_f-32) / 1.8) / 630)
                                                                         ) *
                                                              (((temperature_f-32) / 1.8) / 630)
                                                              ) * (((temperature_f-32) / 1.8) / 630)
                                                   ) *(((temperature_f-32) / 1.8) / 630))*(((temperature_f-32) / 1.8) / 630)
                             ) * (((temperature_f-32) / 1.8) / 630)) ) *1.8)+32)
                
                delta_t = t_star - tref
                fp = math.exp((param_a+param_b*t_star+((param_c+param_d*t_star)/(rec_pi_star**2))))
                rec.ctl = round(math.exp((-(alpha_60 * delta_t)) * (1 + ((0.8 * alpha_60) * (delta_t + delta_60)))), 15)
                rec.cpl = round(1 / (1-((10 ** -5) * (fp * rec.pressure_psi))), 13)
                # print(f'\n'
                #       f'rec no: {rec.document_no}\n'
                #       f'rec_pi: {rec_pi}\n'
                #       f'rec_a: {rec_a}\n'
                #       f'rec_b: {rec_b}\n'
                #       f'rec_pi_star: {rec_pi_star}\n'
                #       f't_star: {t_star}\n'
                #       f'rec.ctl: {rec.ctl}\n'
                #       f'rec.cpl: {rec.cpl}\n'
                #       f'')
            except Exception as e:
                logging.error(f'_ctl_cpl : {e}')
                logging.error(f'_ctl_cpl : You might needed to save system parameters')
                rec.ctl = 1
                rec.cpl = 1
                raise ValidationError(_('You might needed to save system parameters.'
                                        '\n They get default values but you have to save them to res.config.system.'))

    def _weighbridge_change(self):
        # It makes sure the tanker weight or the totalizer amount would be zero whenever the weighbridge has changed.
        for rec in self:
            if rec.weighbridge == 'no':
                rec.write({'tanker_empty_weight': 0, 'tanker_full_weight': 0, })

    @api.onchange('front_container', 'middle_container', 'back_container')
    def _total(self):
        # It calculates the total amount of tanker containers
        for rec in self:
            rec.total = rec.front_container + rec.middle_container + rec.back_container

    @api.onchange('totalizer_end', 'totalizer_start')
    def _totalizer_difference(self):
        # It calculates the totalizer difference based on totalizer start amount and its end amount
        for rec in self:
            if rec.totalizer_end == 0:
                rec.totalizer_difference = 0
            elif rec.totalizer_end > rec.totalizer_start:
                rec.totalizer_difference = rec.totalizer_end - rec.totalizer_start
            else:
                rec.totalizer_difference = 100000000 + rec.totalizer_end - rec.totalizer_start

    @api.onchange('tanker_full_weight', 'tanker_empty_weight')
    def _tanker_pure_weight(self):
        # It calculates the loaded amount based on calculation of tanker full weight and its empty weight.
        for rec in self:
            rec.tanker_pure_weight = rec.tanker_full_weight - rec.tanker_empty_weight

    @api.constrains('document_no')
    def _check_document_no_unique(self):
        # It makes sure the document number is unique
        record_count = self.search_count([('document_no', '=', self.document_no), ('id', '!=', self.id)])
        if record_count > 0:
            raise ValidationError("Record already exists!")

    @api.model
    def create(self, vals):


        # todo: it is disabled for parallel data entry of excel and this system.
        if vals.get('document_no', 0) == 0:
            vals['document_no'] = self.env['ir.sequence'].next_by_code('sd_payaneh_nafti.input_info') or 0

            # todo: timezone, last ours of 29'th of Esfand might show a wrong date, maybe first of next year
            # vals['loading_no'] = str(jdatetime.date.today().year) + f"/{int(vals['document_no']):07d}"
        # doc_no = vals.get('document_no', 0)
        # if doc_no == 0 or doc_no < 10000 or doc_no > 99999:
        #     raise ValidationError(_('Document No'))

        # It helps to not generate new loading no if there is already exists.
        if vals.get('loading_no', '') == '':
            loading_no = self.env['ir.sequence'].next_by_code('sd_payaneh_nafti.loading_no') or 0
            vals['loading_no'] = str(jdatetime.date.today().year) + f"/{int(loading_no):07d}"

        spgr = self.env['sd_payaneh_nafti.spgr'].search([], order='id desc', limit=1)
        if len(spgr) == 1:
            vals['sp_gr'] = spgr.spgr
            vals['centralized_container'] = spgr.centralized_container
        else:
            raise ValidationError(_('Add a "SP.GR." from the main menu'))

        if vals.get('meter_no') and type(vals.get('meter_no')) == str and vals.get('meter_no').lower() == 'master':
            vals['meter_no'] = '0'
        return super(SdPayanehNaftiInputInfo, self).create(vals)

    def write(self, vals):
        # Changing the compartment_1 means that there are loading info entry. So, it moves the state to cargo_document.
        if vals.get('meter_no') or vals.get('compartment_locker_1'):
            vals['state'] = 'cargo_document'

        if not self.env.is_admin() and self.state == 'finished':
            raise ValidationError(_('Finished record is not editable!'))

        doc_no = vals.get('document_no', None)
        if doc_no is not None and (doc_no == 0 or doc_no > 99999):
            raise ValidationError(_('Document No'))

        return super(SdPayanehNaftiInputInfo, self).write(vals)

    def get_contract_registration(self):
        # On the input_info form, there is a button named "Contract" which it shows the related contract of this input
        #   info.
        self.ensure_one()
        form_id = self.env.ref('sd_payaneh_nafti.sd_payaneh_nafti_contract_registration_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Inputs',
            'views': [ [form_id, 'form']],
            'view_mode': 'form',
            'res_id': self.registration_no.id,
            'res_model': 'sd_payaneh_nafti.contract_registration',
            'context': "{'create': False}"
        }

    def loading_permit(self):
        # In input info for, there is a button named "Loading Permit" which updates some fields.
        for rec in self:
            # loading_no = self.env['ir.sequence'].next_by_code('sd_payaneh_nafti.loading_no') or 0
            #
            # loading_no = str(jdatetime.date.today().year) + f"/{int(loading_no):07d}"
            loading_date = datetime.now(pytz.timezone(self.env.context.get('tz', 'Asia/Tehran'))).date()
            rec.write({'state': 'loading_permit', 'loading_date': loading_date })

    def print_loading_permit(self):

        if self.state == 'loading_permit':
            self.write({'state': 'loading_info'})
        data = {'form_data': {'document_no': (0, self.document_no)}}
        return self.env.ref('sd_payaneh_nafti.loading_permit_report').report_action(self, data=data)

    def loading_info(self):
        data = {'form_data': {'document_no': (0, self.document_no)}}
        loading_info_form = self.env.ref('sd_payaneh_nafti.sd_payaneh_nafti_input_info_form_loading_info')
        # print(f'\n loading info: self: {self} loading_info_form: {loading_info_form}')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Loading Info',
            'views': [[loading_info_form.id, 'form']],
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'res_model': 'sd_payaneh_nafti.input_info',
            # 'context': "{'create': False}"
        }

    def print_cargo_document(self):
        data = {'form_data': {'document_no': (0, self.document_no), 'calendar': 'fa_IR'}}
        return self.env.ref('sd_payaneh_nafti.cargo_document_report').report_action(self, data=data)

    def input_done(self):
        for rec in self:
            rec.write({'state': 'done'})


    def input_finished(self):
        for rec in self:
            rec.write({'state': 'finished'})

    @api.model
    def get_requests(self):
        # today_date = date.today()
        today_date = datetime.now(pytz.timezone(self.env.context.get('tz', 'Asia/Tehran'))).date()
        # print(f'------------> today_date: {today_date}')

        open_requests = self.search([('state', 'not in', ['done', 'finished'])])
        this_day_requests = self.search([('request_date', '=', today_date)])

        # todo: amount is not comparable between contracts with different unit type.
        #   amount for barrel is calculated based on final_bbl
        #   amount for metric tone is calculated based on final_mt
        #   so the remain amount of this two type of contracts should not be sum up.
        this_day_loaded = self.search([('loading_info_date', '=', today_date)])
        one_day_ago_loaded = self.search([('loading_info_date', '=', today_date - timedelta(days=1))])
        two_days_ago_loaded = self.search([('loading_info_date', '=', today_date- timedelta(days=2))])
        three_days_ago_loaded = self.search([('loading_info_date', '=', today_date- timedelta(days=3))])
        this_day_requests_amount = round(sum([rec.amount for rec in this_day_loaded ]), 2)
        this_day_requests_amount = 0

        this_day_requests_count = len(this_day_requests)
        new_requests = len([rec for rec in open_requests if rec.state == 'draft'])
        loading_permit = len([rec for rec in open_requests if rec.state == 'loading_permit'])
        loading_info = len([rec for rec in open_requests if rec.state == 'loading_info'])


        cargo_document = len([rec for rec in open_requests if rec.state == 'cargo_document'])


        data = {
            'open_requests': len(open_requests),
            'this_day_requests_count': this_day_requests_count,
            'one_day_ago_count': len(one_day_ago_loaded),
            'two_days_ago_count': len(two_days_ago_loaded),
            'three_days_ago_count': len(three_days_ago_loaded),
            'this_day_requests_amount': this_day_requests_amount,
            'new_requests': new_requests,
            'loading_permit': loading_permit,
            'loading_info': loading_info,
            'cargo_document': cargo_document,
        }
        return json.dumps(data)



class SdPayanehNaftiPlate1(models.Model):
    _name = 'sd_payaneh_nafti.plate1'
    _description = 'sd_payaneh_nafti.plate1'

    name = fields.Char(translate=True)


class SdPayanehNaftiPlate2(models.Model):
    _name = 'sd_payaneh_nafti.plate2'
    _description = 'sd_payaneh_nafti.plate2'

    name = fields.Char(translate=True)


class SdPayanehNaftiPlate3(models.Model):
    _name = 'sd_payaneh_nafti.plate3'
    _description = 'sd_payaneh_nafti.plate3'

    name = fields.Char(translate=True)

class SdPayanehNaftiPlate4(models.Model):
    _name = 'sd_payaneh_nafti.plate4'
    _description = 'sd_payaneh_nafti.plate4'

    name = fields.Char(translate=True)


