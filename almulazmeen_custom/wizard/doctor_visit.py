from decimal import DefaultContext
from odoo import fields,api,models,_

class DoctorVisitReport(models.TransientModel):
    _name = 'doctor.visit.report'
    _description = 'Doctor Visit Report'

    date_from = fields.Datetime(
        string='From',)
    date_to = fields.Datetime(
        string='To',)
    doctor_id = fields.Many2one(string='Doctor', comodel_name='res.partner',domain=[('is_doctor', '=', True)],default=lambda self: self._context.get('active_id')
    )
    def print_report(self):
        active_ids = self.env.context.get('active_ids', [])
        data = {
            'ids':active_ids,
            'model': 'doctor.visit.report',
            'form': self.read()[0]
        }

        return self.env.ref('almulazmeen_custom.report_doctor_visit_report').report_action(self, data=data)

class medInsuranceReportAbs(models.AbstractModel):
    _name = 'report.almulazmeen_custom.report_doctor_visit_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data['form']['doctor_id']:
            selected_doctor = data['form']['doctor_id'][0]
            date_from = data['form']['date_from']
            date_to = data['form']['date_to']
            doctor_visit = self.env['med.appointment.visit'].search([('doctor_id','=',selected_doctor),('date','>=',date_from),('date','<=',date_to)])
        else:
            doctor_visit = self.env['med.appointment.visit'].search([])
        print("=>>" *200)
        print(doctor_visit)
        return{
            'doc_model':'res.partner',
            'docs':doctor_visit,
        }

# class InvoiceReportAbs(models.AbstractModel):
#     _name = 'report.almulazmeen_custom.report_doctor_invoice_template'

#     @api.model
#     def _get_report_values(self, docids, data=None):
#         if data['form']['doctor_id']:
#             selected_doctor = data['form']['doctor_id'][0]
#             date_from = data['form']['date_from']
#             date_to = data['form']['date_to']
#             doctor_visit = self.env['med.appointment.visit'].search([('doctor_id','=',selected_doctor),('date','>=',date_from),('date','<=',date_to)])
#             account_move_line_ids = self.env['account.move.line'].search([('doctor_id','=',selected_doctor),('visit_id','in',doctor_visit),('date','>=',date_from),('date','<=',date_to)])
#         else:
#             doctor_visit = self.env['med.appointment.visit'].search([])
#             account_move_line_ids = self.env['account.move.line'].search([])
#         print("=>>" *200)
#         print(doctor_visit)
#         return{
#             'doc_model':'res.partner',
#             'docs':account_move_line_ids,
#         }