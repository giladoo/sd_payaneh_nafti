# -*- coding: utf-8 -*-
from datetime import  datetime, timedelta
from time import time

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from colorama import Fore

class SdPayanehNaftiLockers(models.Model):
    _name = 'sd_payaneh_nafti.lockers'
    _description = 'sd_payaneh_nafti.lockers'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'


    name = fields.Char(required=True,)
    input_info = fields.Many2one('sd_payaneh_nafti.input_info')
    locker_log = fields.Many2one('sd_payaneh_nafti.locker_log')
    # input_info_ids = fields.One2many('sd_payaneh_nafti.input_info', 'lockers')
    locker_type = fields.Many2one('sd_payaneh_nafti.locker_type')
    batch_id = fields.Many2one('sd_payaneh_nafti.locker_batch')
    batch_state = fields.Selection(related='batch_id.state')
    batch_group = fields.Char()

    def compair_lockers(self,):
        buttons = self.env.context.get('buttons', 'buttons')

        if buttons == 'compair':
            input_locker_list = ['evacuation_box_seal', 'compartment_1', 'compartment_2', 'compartment_3', ]
            lockers = self.search_read([], ['input_info'],)
            lockers_ids = list(set([rec.get('input_info')[0] for rec in lockers]))
            input_locker_diff = self.env['sd_payaneh_nafti.input_info'].search_read([('id', 'not in', lockers_ids)], ['document_no'] + input_locker_list)
            for input_info in input_locker_diff:
                locker = self.search_read([('name', '=', input_info.get('evacuation_box_seal'))], ['input_info'])

                print(f"{input_info.get('document_no'):6} > {input_info.get('evacuation_box_seal'):12}, "
                      f"Locker {locker[0]['input_info'][1] if len(locker) else '':6}")

        elif buttons == 'groups':
            print(f"\n#################     GROUPS    ###################")
            chunk_list = 10000
            active_ids = self.search([('batch_group', '=', False)]).ids
            print(f"\n len active_ids: {len(active_ids)}")
            active_ids_lists = [active_ids[i:i + chunk_list] for i in range(0, len(active_ids), chunk_list)]
            st1 = time()
            for active_ids_list in active_ids_lists:
                st2 = time()
                records = self.search([('id', 'in', active_ids_list)])
                for rec in records:
                    if rec.name[0:3] in ['SPT', 'spt']:
                        rec.batch_group = 'SPT'
                    elif rec.name[0:3] == 'C+-':
                        rec.batch_group = 'C+-'
                    elif rec.name[0:4] == 'C5+-':
                        rec.batch_group = 'C5+-'
                    elif rec.name[0:2] == 'FF':
                        rec.batch_group = 'FF'
                    elif rec.name[0:2] == 'FK':
                        rec.batch_group = 'FK'
                    elif rec.name[0:2] == 'FH':
                        rec.batch_group = 'FH'
                    else:
                        rec.batch_group = rec.name[0:3]
                print(f">>>> len: {len(active_ids_list)} time: {round(time() - st2)}")
            print(f"\n len ALL: {len(active_ids)} time: {round(time() - st1)}")


class SdPayanehNaftiLockerLog(models.Model):
    _name = 'sd_payaneh_nafti.locker_log'
    _description = 'sd_payaneh_nafti.locker_log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'subject'

    subject = fields.Char(required=True, )
    issue_date = fields.Date(required=True, default=lambda self: fields.date.today())
    lockers = fields.One2many('sd_payaneh_nafti.lockers', 'locker_log', required=True, )
    description = fields.Html()
    file_name = fields.Char()
    attachment = fields.Binary()



class SdPayanehNaftiLockerType(models.Model):
    _name = 'sd_payaneh_nafti.locker_type'
    _description = 'sd_payaneh_nafti.locker_type'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, translate=True)
    code = fields.Selection([('tanker', 'Tanker'), ('meter', 'Meter'), ('report', 'Report'), ], default='tanker')
    sequence = fields.Integer(default=100)


class SdPayanehNaftiLockerBatch(models.Model):
    _name = 'sd_payaneh_nafti.locker_batch'
    _description = 'sd_payaneh_nafti.locker_batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'start_no'

    state = fields.Selection([('draft', 'Draft'),('published', 'Published'),
                              ('paused', 'Paused'), ('canceled', 'Canceled') ], default='draft')
    sequence = fields.Integer(default=100)
    start_no = fields.Char(required=True)
    end_no = fields.Char(required=True)
    count = fields.Integer(compute='_calculate_count')
    free_lockers = fields.Integer(compute='_calculate_count')
    is_inuse = fields.Boolean(default=False)
    receive_date = fields.Date(required=True, default=lambda self: fields.date.today())
    letter_no = fields.Char(required=True,)
    file_name = fields.Char()
    description = fields.Text()
    attachment = fields.Binary()

    @api.onchange('start_no', 'end_no')
    @api.depends('count')
    def _calculate_count(self):
        lockers_model = self.env['sd_payaneh_nafti.lockers']

        for rec in self:
            if not rec.start_no or not rec.end_no:
                rec.count = 0
                rec.free_lockers = 0
                continue
            used_lockers = lockers_model.search_count([('batch_id', '=', rec.id), ('input_info', '!=', False), ])
            rec.is_inuse = True if used_lockers > 0 else False
            if rec.start_no and rec.end_no and len(rec.start_no) != len(rec.end_no):
                rec.count = 0
                rec.free_lockers = 0
                continue
            start_no_prefix, start_no_number = self._get_prefix_number(rec.start_no)
            end_no_prefix, end_no_number = self._get_prefix_number(rec.end_no)
            if start_no_prefix != end_no_prefix:
                rec.count = 0
                rec.free_lockers = 0

            else:
                rec.count = end_no_number - start_no_number + 1
                rec.free_lockers = rec.count - used_lockers

    def _get_prefix_number(self, value=''):
        if value:
            index = next(i for i, c in enumerate(value) if c.isdigit())
            prefix, number = value[:index], int(value[index:])
        else:
            prefix = ''
            number = 0
        return prefix, number

    def lockers_button(self):
        lockers_model = self.env['sd_payaneh_nafti.lockers']
        locker_btn = self.env.context.get('locker_btn', 'state_btn')
        lockers = lockers_model.search([('batch_id', '=', self.id)])
        # used_lockers = list([rec for rec in lockers if rec.input_info != False])
        if locker_btn == 'publish':
            if self.state == 'draft' and not self.count:
                raise ValidationError(_("There is no locker to create."))


            self.state = 'published'

        elif locker_btn == 'cancel':
            if self.is_inuse:
                raise ValidationError(_("Some lockers are in use"))
            self.state = 'canceled'

        elif locker_btn == 'draft':
            if self.is_inuse:
                raise ValidationError(_("Some lockers are in use"))
            self.state = 'draft'

        elif locker_btn == 'pause':
            self.state = 'paused'

    def write(self, vals):
        lockers_model = self.env['sd_payaneh_nafti.lockers']
        if vals.get('start_no', False) or vals.get('end_no', False):
            lockers = lockers_model.search([('batch_id', '=', self.id)])
            for rec in lockers:
                rec.unlink()

        if vals.get('state', '') == 'published':
            lockers_count = lockers_model.search_count([('batch_id', '=', self.id)])
            if lockers_count == 0:
                start_no_prefix, start_no_number = self._get_prefix_number(self.start_no)
                end_no_prefix, end_no_number = self._get_prefix_number(self.end_no)
                locker_len = len(self.start_no)
                prefix_len = len(start_no_prefix)
                number_len = locker_len - prefix_len
                for i in range(start_no_number, end_no_number + 1):
                    new_code = f"{start_no_prefix}{i:0{number_len}}"
                    # print(f"  {new_code}")
                    lockers_model.create({
                        'name': new_code,
                        'batch_id': self.id,
                        'batch_group': start_no_prefix,
                    })



        return super(SdPayanehNaftiLockerBatch, self).write(vals)

    def unlink(self):
        for rec in self:
            if rec.count - rec.free_lockers > 0:
                raise ValidationError(_("Some lockers are in use"))

        return super(SdPayanehNaftiLockerBatch, self).unlink()


class SdPayanehNaftiLockersInputInfo(models.Model):
    _inherit = 'sd_payaneh_nafti.input_info'

    lockers = fields.One2many('sd_payaneh_nafti.lockers', 'input_info')

    @api.onchange('api_box_locker')
    def change_api_box_locker(self):
        # print(f'\n {self.api_box_locker}')
        pass

    def write(self, vals):
        # vlas.get('rec', 0) =>
        #       0 : No change
        #   False : removed
        # Integer : changed
        # print(f'\n write {vals}, {self.api_box_locker}')
        if vals.get('api_box_locker'):
            pass
            # print(f'\n api_box_locker: {vals.get("api_box_locker")}')
        return super(SdPayanehNaftiLockersInputInfo, self).write(vals)
