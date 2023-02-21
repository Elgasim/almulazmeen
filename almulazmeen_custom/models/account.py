from odoo import fields,api,models,_


class accountMove(models.Model):
    _inherit = 'account.move'

    payment_method = fields.Selection(
        string='Payment Type',
        selection=[('private', 'Private'),
                   ('insurance', 'Insurance'),],)

    @api.onchange('appointment_id')
    def onchange_appointment_id(self):
        self.payment_method = self.appointment_id.payment_type
        self.partner_id = self.appointment_id.patient_id.id

    @api.onchange('partner_id')
    def get_insurance_card_domain(self):
        domain = []
        if self.partner_id:
            domain = [('patient_id','=',self.partner_id.id)]
        return {'domain':{'insurance_card':domain}}

    @api.onchange('insurance_card')
    def onchange_insurance_card(self):
        if self.insurance_card:
            self.pricelist_id = self.insurance_card.pricelist_id.id
    
    insurance_card = fields.Many2one(
        comodel_name='med.insurance.card',
        string='Insurance Card',
        required=False)
    appointment_id = fields.Many2one(
        comodel_name='med.appointment',
        string='Appointment',
        required=False)

class accountMoveLine(models.Model):
    _inherit = 'account.move.line'

    doctor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Doctor',
        compute="get_doctor",
        domain=[('is_doctor', '=', True)],
        store=True,
        required=False)
    @api.depends('move_id','is_visit')
    def get_doctor(self):
        for rec in self:
            if rec.is_visit:
                rec.doctor_id = rec.move_id.appointment_id.doctor_id.id
            else:
                rec.doctor_id = False

    is_lab = fields.Boolean(
        string='is Lab',
        related='product_id.is_lab',
        required=False)
    is_operation = fields.Boolean(
        string='Ophthalmic Operations',
        related='product_id.is_operation',
        required=False)
    is_med_service = fields.Boolean(
        string='Clinical & Medical Services',
        related='product_id.is_med_service',
        required=False)
    is_visit = fields.Boolean(
        string='Is Visit',
        related='product_id.visit_product',
        required=False)
    