from dataclasses import field
from odoo import fields,api,models,_
import datetime
# import json
from datetime import datetime, timedelta, time
from dateutil import relativedelta
# from json import dumps



class medAppointmentLab(models.Model):
    _name = 'med.appointment.lab'
    _rec_name = 'appointment_id'

    lab_product_id = fields.Many2one(
        comodel_name='product.product',
        domain=[('is_lab', '=', True)],
        string='Name',
        required=True)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Patient',
        domain=[('is_patient', '=', True)],
        related='appointment_id.patient_id',
        required=True)
    result = fields.Binary(string="Result",)
    appointment_id = fields.Many2one(
        comodel_name='med.appointment',
        string='Medical Appointment',
        required=False)

class medAppointmentDrug(models.Model):
    _name = 'med.appointment.drug'
    _rec_name = 'appointment_id'

    pos_product_id = fields.Many2one(
        comodel_name='product.product',
        domain=[('available_in_pos', '=', True)],
        string='Drug Name',
        required=True)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Patient',
        domain=[('is_patient', '=', True)],
        related='appointment_id.patient_id',
        required=True)
    use = fields.Selection(
        string='Using Every',
        selection=[('24', '24 Hours'),
                   ('12', '12 Hours'),
                   ('8', '8 Hours'),
                   ('4', '4 Hours'),
                   ('2', '2 Hours'),
                   ],
        required=False, )

    comments = fields.Text(
        string="Comments",
        required=False)
    appointment_id = fields.Many2one(
        comodel_name='med.appointment',
        string='Medical Appointment',
        required=False)

class medAppointmentOperation(models.Model):
    _name = 'med.appointment.operation'
    _rec_name = 'appointment_id'

    operation_product_id = fields.Many2one(
        comodel_name='product.product',
        domain=[('is_operation', '=', True)],
        string='Name',
        required=True)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Patient',
        domain=[('is_patient', '=', True)],
        related='appointment_id.patient_id',
        required=True)
    comments = fields.Text(
        string="Comments",
        required=False)
    date = fields.Datetime(
        string='Date',
        required=False)
    result = fields.Binary(string="Result",)
    appointment_id = fields.Many2one(
        comodel_name='med.appointment',
        string='Medical Appointment',
        required=False)

class mdAppointmentVisits(models.Model):
    _name = 'med.appointment.visit'
    _rec_name = 'date'
    visit_product_id = fields.Many2one(
        comodel_name='product.product',
        domain=[('visit_product', '=', True)],
        string='Visit',
        required=True)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Patient',
        domain=[('is_patient', '=', True)],
        related='appointment_id.patient_id',
        required=True)
    doctor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Doctor',
        domain=[('is_doctor', '=', True)],
        compute = "get_doctor",
        readonly=False,
        required=True)

    @api.depends('appointment_id')
    def get_doctor(self):
        for rec in self:
            if rec.appointment_id:
                rec.doctor_id = rec.appointment_id.doctor_id.id
    comments = fields.Text(
        string="Comments",
        required=False)
    date = fields.Datetime(
        string='Visit Date',
        required=False)
    appointment_id = fields.Many2one(
        comodel_name='med.appointment',
        string='Medical Appointment',
        required=False)



class medAppointment(models.Model):
    _name = 'med.appointment'
    _description = 'Medical Appointment'
    _inherit = ['mail.thread']


     # ==== Payment widget fields ====
    invoice_outstanding_credits_debits_widget = fields.Float(
        compute='payments_widget_to_reconcile_info')
    invoice_has_outstanding = fields.Boolean(
        compute='payments_widget_to_reconcile_info')
    ##############   ###################

    def payments_widget_to_reconcile_info(self):
        for app in self:
            app.invoice_has_outstanding = False
            total = 0.0
            patient = app.patient_id
            in_payments = self.env['account.payment'].search([
                ('payment_type','=','inbound'),
                ('partner_id','=', patient.id),
                ('state','=','posted'),
                ('is_reconciled','=',False)
            ])

            for payment in in_payments:
                total += payment.amount
            app.invoice_outstanding_credits_debits_widget = total
            if app.invoice_outstanding_credits_debits_widget:
                app.invoice_has_outstanding =True



            ######################    #################
    

    payment_type = fields.Selection(
        string='Payment Type',
        selection=[('private', 'Private'),
                   ('insurance', 'Insurance'), ],
        required=True, )

    def move_to_reception(self):
        for rec in self:
            rec.state = 'reception'

    def move_to_doctor(self):
        for rec in self:
            rec.state = 'doctor'

    def move_to_sleep(self):
        for rec in self:
            rec.state = 'sleep'

    @api.model
    def create(self, values):
        number = self.env['ir.sequence'].next_by_code('med.appointment.seq')
        if number:
            values['name'] = number
        return super(medAppointment, self).create(values)

    def get_invoice_count(self):
        for rec in self:
            ids = self.env['account.move'].search([
                ('appointment_id','=',rec.id)
            ])
            rec.invoice_count = len(ids)

    invoice_count = fields.Integer(
        string='# of Invoices',
        compute="get_invoice_count",
        required=False)

    name = fields.Char(
        string='Sequence',
        readonly=True)
    #PATIENT PERSONAL DATA
    state = fields.Selection(
        string='Status',
        selection=[('reception', 'Reception'),
                   ('doctor', 'Doctor'),
                   ('sleep','Sleeping')
                   ],
        default="reception",
        required=False, )

    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Patient',
        domain=[('is_patient','=',True)],
        required=True)
    age = fields.Float(
        string='Age',
        compute='get_age',
        related='patient_id.age',
        required=False)
    gender = fields.Selection(
        string='Gender',
        related='patient_id.gender',
        selection=[('m', 'Male'),
                   ('f', 'Female'), ],
        required=False, )
    residence = fields.Char(
        string='Residence',
        related='patient_id.residence',
        required=False)
    occupation = fields.Char(
        string='Occupation',
        related='patient_id.occupation',
        required=False)
    file_number = fields.Char(
        string='File #',
        related='patient_id.file_number',
        required=False)
    doctor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Doctor Name',
        domain=[('is_doctor', '=', True)],
        related='patient_id.doctor_id',
        readonly=False,
        required=False)
    ref_doctor = fields.Char(
        string='REF DOCTOR',
        related='patient_id.ref_doctor',
        required=False)
    note = fields.Text(
        string="Note",
        related='patient_id.note',
        required=False)
    date = fields.Datetime(
        string='Date of first visit',
        related='patient_id.date',
        readonly=False,
        required=False)
    next_date = fields.Datetime(
        string='Next Visit',
        related='patient_id.next_date',
        readonly=False,
        required=False)
    #HISTORY
    hypertension  = fields.Boolean(
        string='Hypertension',
        required=False)
    asthma  = fields.Boolean(
        string='Asthma',
        required=False)
    diabetus_mellitus = fields.Boolean(
        string='Diabetus Mellitus ',
        required=False)
    cardiac_disorders = fields.Boolean(
        string='Cardiac Disorders',
        required=False)
    respiratory_disorders = fields.Boolean(
        string='Respiratory Disorders ',
        required=False)
    neurological_disorders = fields.Boolean(
        string='Neurological Disorders ',
        required=False)
    others = fields.Text(
        string="Others",
        required=False)
    histroy_of_surgery = fields.Text(
        string="Histroy of surgery",
        required=False)
    #Lab
    lab_ids = fields.One2many(
        comodel_name='med.appointment.lab',
        inverse_name='appointment_id',
        string='Imaging',
        required=False)
    #Prescribed Drugs
    drug_ids = fields.One2many(
        comodel_name='med.appointment.drug',
        inverse_name='appointment_id',
        string='Prescribed Drugs ',
        required=False)
    # Operation
    operation_ids = fields.One2many(
        comodel_name='med.appointment.operation',
        inverse_name='appointment_id',
        string='Operation Request ',
        required=False)

    # Visits
    visit_ids = fields.One2many(
        comodel_name='med.appointment.visit',
        inverse_name='appointment_id',
        string='Visit Request ',
        required=False)



###################################################################
#             One2many Fields for Appoinment Fields               #
#                                                                 #
###################################################################

    room_appointment_ids = fields.One2many(
        comodel_name= 'med.appointment.room.appointment',
        inverse_name= 'appointment_id')

    bed_appointment_ids = fields.One2many('med.appointment.room.bed.appointment','appointment_id')
    


##################################################################
#                   Room and bed Configuration                   #
#                                                                #
##################################################################

class MedAppointmentRoom(models.Model):
    _name = 'med.appointment.room'
    _inherit = ['mail.thread','mail.activity.mixin']

    name  = fields.Char(string='Name')
    type = fields.Selection(string='Room Type', selection=[('room', 'Room'),('vip','VIP'),('normal','Normal'),('wing','Winger'),('icu','ICU')],required=True, default="room")
    # appointment_id = fields.Many2one( comodel_name='med.appointment',string="Medical Appointment")
    room_product_id = fields.Many2one(
        comodel_name='product.product',
        domain=[('is_room', '=', True)],
        string='item',)
    state  = fields.Selection(string='Room Status', selection=[('empty', 'Empty'),('reserve','Reserved')], required = True, default="empty", readonly=True)
    bed_ids = fields.One2many('med.appointment.room.bed', 'room_id', string='Beds')

class MedAppointmentRoomBed(models.Model):
    _name = 'med.appointment.room.bed'
    _inherit = ['mail.thread','mail.activity.mixin']

    room_id = fields.Many2one(string='Room', comodel_name='med.appointment.room',)
    # appointment_id = fields.Many2one( comodel_name='med.appointment',string="Medical Appointment")
    name  = fields.Char(string="Bed Label")
    state = fields.Selection(string='Bed Status', selection=[('empty', 'Empty'),('reserve','Reserved')], required = True, default="empty", readonly=True)
    bed_product_id = fields.Many2one(
        comodel_name='product.product',
        domain=[('is_bed', '=', True)],
        string='item',)

##########################################################################
#                                                                        #
#                  Room Appointment                                      #
##########################################################################

class MedAppointmentRoomAppointment(models.Model):
    _name = 'med.appointment.room.appointment'
    _rec_name = "room_id"

    state  = fields.Selection(string='Room Status', selection=[('empty', 'Empty'),('reserve','Reserved')], required = True, default="empty", readonly=True)

    room_id = fields.Many2one(string='Room', comodel_name='med.appointment.room', domain="[('type','in',('room','vip','normal')),('state', '=', 'empty')]")
    appointment_id = fields.Many2one( comodel_name='med.appointment',string="Medical Appointment")
    patient_id = fields.Many2one(
        'res.partner',related="appointment_id.patient_id",
        string='Patient', store=True,
        )
    doctor_id = fields.Many2one(
        'res.partner',related="appointment_id.doctor_id",
        string='Doctor', store=True,
        )
    date_from  = fields.Datetime(string='From',default=fields.Datetime.now(), required=True)
    date_to  = fields.Datetime(string='To',default=fields.Datetime.now(),required=True)
    difference =fields.Integer(
        string='Staying period', readonly=True, compute = "get_difference"
    )

##################################################################################
##Function to calculate difference time in days between Entry date and Exit date##
##################################################################################


    @api.depends('date_from','date_to')
    def get_difference(self):
        for rec in self:
            rec.difference = (rec.date_to - rec.date_from).days
    

##################################################################################
##                             Function to unreserve rooms                      ##
#                            state(reserve) ==> unreserve                        #
##################################################################################
    def unreserve_button(self):
        for rec in self:
            rec.state = 'empty'
            rec.room_id.state = "empty"
#########################################################################
##                 Function to reserve rooms                           ##
#                            state(unreserve) ==> reserve               #
#########################################################################

    def reserve_button(self):
        for rec in self:
            rec.state = 'reserve'
            rec.room_id.state = "reserve"
            
##########################################################################
#                                                                        #
#                  Bed Appointment                                       #
##########################################################################   
class MedAppointmentRoomAppointment(models.Model):
    _name = 'med.appointment.room.bed.appointment'
    _rec_name = 'bed_id'

    state = fields.Selection(string='Bed Status', selection=[('empty', 'Empty'),('reserve','Reserved')], required = True, default="empty", readonly=True)

    bed_id = fields.Many2one(string='bed', comodel_name='med.appointment.room.bed', domain=[('state', '=', 'empty')])
    appointment_id = fields.Many2one(comodel_name='med.appointment', string="Medical Appointment")
    patient_id = fields.Many2one(
        'res.partner',related="appointment_id.patient_id",
        string='Patient', store=True,
        )
    doctor_id = fields.Many2one(
        'res.partner',related="appointment_id.doctor_id",
        string='Doctor', store=True,
        )
    date_from  = fields.Datetime(string='From',default=fields.Datetime.now(),required=True)
    date_to  = fields.Datetime(string='To',default=fields.Datetime.now(),required=True)
    difference =fields.Integer(
        string='Staying period', readonly=True
    )

##################################################################################
##Function to calculate difference time in days between Entry date and Exit date##
##################################################################################

    @api.onchange('date_from','date_to')
    def onchange_date_from_date_to(self):
        for rec in self:
            rec.difference = (rec.date_to - rec.date_from).days

##################################################################################
##                             Function to unreserve Beds                       ##
#                            state(reserve) ==> unreserve                        #
##################################################################################

    def unreserve_button(self):
        for rec in self:
            rec.state = 'empty'
            rec.bed_id.state = "empty"

##################################################################################
##                             Function to reserve Beds                         ##
#                            state(unreserve) ==> reserve                        #
##################################################################################

    def reserve_button(self):
        for rec in self:
            rec.state = 'reserve'
            rec.bed_id.state = "reserve"

