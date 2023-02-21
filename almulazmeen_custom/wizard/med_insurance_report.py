from odoo import fields,api,models,_

class medInsuranceReport(models.TransientModel):
    _name = 'med.insurance.report'
    _description = 'Medical Insurance Report'

    date_from = fields.Date(
        string='From',
        required=True)
    date_to = fields.Date(
        string='To',
        required=True)
    insurance_company_ids = fields.Many2many(
        comodel_name='med.insurance.company',
        string='Companies',
        required=True)

    def print_report(self):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'hr.contribution.register',
            'form': self.read()[0]
        }
        return self.env.ref('almulazmeen_custom.action_med_insurance_report').report_action([], data=datas)

class medInsuranceReportAbs(models.AbstractModel):
    _name = 'report.almulazmeen_custom.report_medical_insurance_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        insurance_company_ids = self.env['med.insurance.company'].browse(data['form']['insurance_company_ids'])

        return {
            'docs': docs,
            'date_from':date_from,
            'date_to':date_to,
            'get_insurance_data':self.get_insurance_data(insurance_company_ids),
        }

    def get_insurance_data(self,insurance_company_ids):
        report_data = {}
        for i_company in insurance_company_ids:
            final_list = []
            report_data.update({i_company.name:[]})
            counter = 0
            t = 0.0
            # Receivable
            domain = [
                ('move_id.move_type', '=', 'out_invoice'),
                ('move_id.payment_type','=','insurance'),
                ('move_id.insurance_card.insurance_company','=',i_company.id),
                ('move_id.state', '=', 'posted'),
                ('account_id.user_type_id.name','!=',"Receivable")
            ]
            for line in self.env['account.move.line'].search(domain):
                if line.price_unit != line.product_id.list_price:
                    counter += 1
                    li = []
                    li.append(counter)
                    li.append(line.move_id.name)
                    li.append(line.move_id.invoice_date)
                    li.append(line.move_id.partner_id.name)
                    li.append(line.product_id.name)
                    li.append(line.product_id.list_price)
                    li.append(line.price_unit)
                    li.append(line.quantity)
                    diff = (line.product_id.list_price - line.price_unit)*line.quantity
                    t = t+diff
                    li.append(diff)
                    final_list.append(li)
            report_data.update({i_company.name: final_list})
        return report_data