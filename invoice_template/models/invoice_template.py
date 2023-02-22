# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class InvoiceTemplate(models.Model):
    _name = 'invoice.template'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'sequence.mixin']
    _check_company_auto = True
    _description = 'invoice template'
    
    name = fields.Char(string='name')
    service_ids = fields.One2many('invoice.template.services','invoice_template_id')

class InvoiceTemplateServices(models.Model):
    _name = 'invoice.template.services'
    _description = 'invoice template Services'
    
    service_id = fields.Many2one('product.product', string='Product Name')
    qty = fields.Float(string='Quanity')
    invoice_template_id = fields.Many2one(string='Invoice template', comodel_name='invoice.template',)

class AppointmentInvoiceTemplate(models.Model):
    _inherit = 'med.appointment'
    
    invoice_template_id = fields.Many2one(string='Invoice template', comodel_name='invoice.template',)
      
class AppointmentInvoiceTemplate(models.Model):
    _inherit = 'account.move'
    
    invoice_template_id = fields.Many2one(string='Invoice template', comodel_name='invoice.template',)
    service_ids = fields.One2many(string='Services',related = 'invoice_template_id.service_ids' )
    
    has_template = fields.Boolean('Has template', compute="is_template")
    
    @api.depends('invoice_template_id')
    def is_template(self):
        if self.invoice_template_id:
            self.has_template = True
        else:
            self.has_template = False
            
    
    @api.onchange('appointment_id')
    def onchange_appointment_id(self):
        self.invoice_template_id = self.appointment_id.invoice_template_id.id
    

                    