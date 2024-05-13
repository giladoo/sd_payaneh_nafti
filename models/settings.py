# todo:
# temperature scale : C/F
# wind scale: km/h or ml/h
# form code
# ref code
#
from odoo import models, fields, api, _


# #################################################################################################
class SdPayanehNaftiSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    k_0 = fields.Float(config_parameter='sd_payaneh_nafti.k_0', digits=(12, 5), tracking=True, default=341.0957)
    k_1 = fields.Float(config_parameter='sd_payaneh_nafti.k_1', digits=(12, 5), tracking=True, default=0)
    k_2 = fields.Float(config_parameter='sd_payaneh_nafti.k_2', digits=(12, 5), tracking=True, default=0)
    delta_60 = fields.Float(config_parameter='sd_payaneh_nafti.delta_60', digits=(12, 12), tracking=True, default=0.01374979547)
    tref = fields.Float(config_parameter='sd_payaneh_nafti.tref', digits=(12, 8), tracking=True, default=60.0068749)
    param_a = fields.Float(config_parameter='sd_payaneh_nafti.param_a', digits=(12, 5), tracking=True, default=-1.9947)
    param_b = fields.Float(config_parameter='sd_payaneh_nafti.param_b', digits=(12, 8), tracking=True, default=0.00013427)
    param_c = fields.Float(config_parameter='sd_payaneh_nafti.param_c', digits=(12, 2), tracking=True, default=793920)
    param_d = fields.Float(config_parameter='sd_payaneh_nafti.param_d', digits=(12, 2), tracking=True, default=2326)
    param_ai1 = fields.Float(config_parameter='sd_payaneh_nafti.param_ai1', digits=(12, 6), tracking=True, default=-0.148759)
    param_ai2 = fields.Float(config_parameter='sd_payaneh_nafti.param_ai2', digits=(12, 6), tracking=True, default=-0.267408)
    param_ai3 = fields.Float(config_parameter='sd_payaneh_nafti.param_ai3', digits=(12, 6), tracking=True, default=1.08076)
    param_ai4 = fields.Float(config_parameter='sd_payaneh_nafti.param_ai4', digits=(12, 6), tracking=True, default=1.269056)
    param_ai5 = fields.Float(config_parameter='sd_payaneh_nafti.param_ai5', digits=(12, 6), tracking=True, default=-4.089591)
    param_ai6 = fields.Float(config_parameter='sd_payaneh_nafti.param_ai6', digits=(12, 6), tracking=True, default=-1.871251)
    param_ai7 = fields.Float(config_parameter='sd_payaneh_nafti.param_ai7', digits=(12, 6), tracking=True, default=7.438081)
    param_ai8 = fields.Float(config_parameter='sd_payaneh_nafti.param_ai8', digits=(12, 6), tracking=True, default=-3.536296)


