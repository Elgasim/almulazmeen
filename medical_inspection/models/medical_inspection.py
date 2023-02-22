from dataclasses import field
from odoo import fields,api,models,_
import datetime

from datetime import datetime, timedelta, time
from dateutil import relativedelta


class MedicalInspection(models.Model):
    _name = 'medical.inspection'
    _inherit = ['mail.thread']
    _description = 'Medical Inspection'

    
    name  = fields.Char()
    date = fields.Datetime(string="Date of plan",default=fields.Date.today())
    month = fields.Char(string="Month")
    company_id = fields.Many2one(
        'res.company',
        string='Hospital of',
        default=lambda self: self.env.user.company_id, 
        readonly=True 
        )
    project_ids = fields.One2many('medical.inspection.project', 'inspectin_id', string="Medical Inspection")



class MedicalInspectionProject(models.Model):
    _name = 'medical.inspection.project'
    _inherit = ['mail.thread']
    _description = 'Medical Inspection Project'


    name = fields.Char(string='Project Name')
    inspectin_id = fields.Many2one(
        'medical.inspection',
        string='Inspection',
        )
    activity_id = fields.Many2one(
        'medical.inspection.project.activity',
        string='Activity',domain=[('project_id', '=', id)]
        )
    wanted = fields.Float(related="activity_id.wanted")
    acheived = fields.Float(string="Acheived")
    ratio  = fields.Float(string="Ratio %", compute="get_ratio")

    @api.depends('wanted', 'acheived')
    def get_ratio(self):
        for rec in self:
            rec.ratio = (rec.acheived / rec.wanted)*100
    


class MedicalInspectionProjectActivities(models.Model):
    _name = 'medical.inspection.project.activity'
    _inherit = ['mail.thread']
    _description = 'Medical Inspection Project Activity'


    name = fields.Char(string='Activity')
    project_id = fields.Many2one(string='Project', comodel_name='medical.inspection.project')
    wanted = fields.Float("wanted")




