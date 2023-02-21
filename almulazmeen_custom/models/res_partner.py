from odoo import fields,api,models,_
import datetime
from dateutil import relativedelta

class resPartner(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(
        string='is Patient',
        required=False)
    residence = fields.Char(
        string='Residence',
        required=False)
    occupation = fields.Char(
        string='occupation',
        required=False)
    file_number = fields.Char(
        string='File #',
        required=False)
    doctor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Doctor Name',
        domain=[('is_doctor', '=', True)],
        required=False)
    ref_doctor = fields.Char(
        string='REF DOCTOR',
        required=False)
    note = fields.Text(
        string="Note",
        required=False)
    date = fields.Datetime(
        string='Date of first visit',
        required=False)
    next_date = fields.Datetime(
        string='Next Visit',
        required=False)
    is_doctor = fields.Boolean(
        string='is Doctor',
        required=False)

    visit_ids = fields.One2many('med.appointment.visit','doctor_id', readonly=True)

    @api.depends('dob')
    def get_age(self):
        for rec in self:
            if rec.dob:
                today = datetime.date.today()
                rec.age = today.year - rec.dob.year - ((today.month, today.day) < (rec.dob.month, rec.dob.day))
            else:
                rec.age = 0.0

    @api.depends('age')
    def inverse_get_age(self):
        today = datetime.date.today()
        for rec in self:
            rec.dob = today - relativedelta.relativedelta(years=int(rec.age))

    dob = fields.Date(
        string='Date of Birth',
        required=False)
    age = fields.Float(
        string='Age',
        compute='get_age',
        inverse="inverse_get_age",
        required=False)
    gender = fields.Selection(
        string='Gender',
        selection=[('m', 'Male'),
                   ('f', 'Female'), ],
        required=False, )
    specialize_id = fields.Many2one(string='Specialize at:', comodel_name='doctor.specialize')

class DoctorSpecilaize(models.Model):
    _name = 'doctor.specialize'

    name = fields.Char(string="Specialize at:")
