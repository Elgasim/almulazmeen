from odoo import fields,api,models,_

class productPricelist(models.Model):
    _inherit = 'product.pricelist'

    is_insurance = fields.Boolean(
        string='Insurance',
        required=False)
    insurance_company_id = fields.Many2one(
        comodel_name='med.insurance.company',
        string='Insurance Company',
        required=False)