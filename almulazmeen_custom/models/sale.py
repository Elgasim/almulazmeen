from odoo import fields,api,models,_

class saleOrder(models.Model):
    _inherit = 'sale.order'

    def refresh(self):
        if self.partner_id:
            id = self.sudo().env['med.appointment'].search([
                ('patient_id','=',self.partner_id.id),
            ],limit=1)
            if id:
                self.od_d_sph = id.od_d_sph
                self.od_d_cyl = id.od_d_cyl
                self.od_d_axis = id.od_d_axis
                self.od_d_va = id.od_d_va

                self.od_n_sph = id.od_n_sph
                self.od_n_cyl = id.od_n_cyl
                self.od_n_axis = id.od_n_axis
                self.od_n_va = id.od_n_va

                self.os_d_sph = id.os_d_sph
                self.os_d_cyl = id.os_d_cyl
                self.os_d_axis = id.os_d_axis
                self.os_d_va = id.os_d_va

                self.os_n_sph = id.os_n_sph
                self.os_n_cyl = id.os_n_cyl
                self.os_n_axis = id.os_n_axis
                self.os_n_va = id.os_n_va

    # Correction
    # OD
    od_d_sph = fields.Char(
        string='SPH',
        required=False)
    od_d_cyl = fields.Char(
        string='CYL',
        required=False)
    od_d_axis = fields.Char(
        string='AXIS',
        required=False)
    od_d_va = fields.Char(
        string='V/A',
        required=False)
    od_n_sph = fields.Char(
        string='SPH',
        required=False)
    od_n_cyl = fields.Char(
        string='CYL',
        required=False)
    od_n_axis = fields.Char(
        string='AXIS',
        required=False)
    od_n_va = fields.Char(
        string='V/A',
        required=False)
    # OS
    os_d_sph = fields.Char(
        string='SPH',
        required=False)
    os_d_cyl = fields.Char(
        string='CYL',
        required=False)
    os_d_axis = fields.Char(
        string='AXIS',
        required=False)
    os_d_va = fields.Char(
        string='V/A',
        required=False)
    os_n_sph = fields.Char(
        string='SPH',
        required=False)
    os_n_cyl = fields.Char(
        string='CYL',
        required=False)
    os_n_axis = fields.Char(
        string='AXIS',
        required=False)
    os_n_va = fields.Char(
        string='V/A',
        required=False)