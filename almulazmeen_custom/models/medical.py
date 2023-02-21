from odoo import models,fields,api,_

class medInsuranceCo(models.Model):
    _name = 'med.insurance.company'
    _description = 'Medical Insurance Company'

    name = fields.Char(
        string='Company Name',
        required=True)
    image = fields.Binary(string="Logo",  )

class medInsuranceCard(models.Model):
    _name = 'med.insurance.card'
    _description = 'Medical Insurance Card'

    @api.onchange('insurance_company')
    def get_pricelist_id_domain(self):
        return {'domain':{'pricelist_id':[('is_insurance','=',True),('insurance_company_id','=',self.insurance_company.id)]}}

    name = fields.Char(
        string='Card #',
        required=True)
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('is_patient','=',True)],
        string='Patient',
        required=True)
    insurance_company = fields.Many2one(
        comodel_name='med.insurance.company',
        string='Insurance Company',
        required=True)
    expiry_date = fields.Date(
        string='Expiry Date',
        required=True)
    type = fields.Char(
        string='Type',
        required=True)
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Pricelists',
        domain=get_pricelist_id_domain,
        required=True)
    note = fields.Text(
        string="Note",
        required=False)
    image = fields.Binary(string="Logo",related='insurance_company.image')