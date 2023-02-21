from odoo import fields,api,models,_


class productTemp(models.Model):
    _inherit = 'product.template'

    is_lab = fields.Boolean(
        string='is Lab',
        required=False)
    is_operation = fields.Boolean(
        string='Operations',
        required=False)
    is_med_service = fields.Boolean(
        string='Clinical & Medical Services',
        required=False)
    is_room = fields.Boolean(
        string='Room?',
        required=False)
    is_bed = fields.Boolean(
        string='Bed?',
        required=False)
    visit_product = fields.Boolean(
        string='Visit?',
        required=False)
    # is_ultra_sound = fields.Boolean(
    #     string='Ultrasound and Grams',
    #     required=False)
    # is_image = fields.Boolean(
    #     string='Imaging',
    #     required=False)
    # is_laser = fields.Boolean(
    #     string='Laser',
    #     required=False)
    # is_glass = fields.Boolean(
    #     string='Glass',
    #     required=False)
    # is_frame = fields.Boolean(
    #     string='Frame',
    #     required=False)


