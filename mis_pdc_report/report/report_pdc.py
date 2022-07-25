
from odoo import models, fields, api


class ReportPDC(models.AbstractModel):
    _name = 'report.mis_pdc_report.report_pdc'
    _description ='PDC PDF report'

    def get_pdc(self, docs):
        if docs.report_type=='All':
            rec = self.env['account.payment'].search([('check_date', '>=', docs.from_date),
                                                            ('check_date', '<=', docs.to_date)])
        elif docs.report_type=='Reconciled':
            rec = self.env['account.payment'].search([('state', '=', 'reconciled'),
                                                            ('check_date', '>=', docs.from_date),
                                                            ('check_date', '<=', docs.to_date)])
        elif docs.report_type=='UnReconciled':
            rec = self.env['account.payment'].search([('state', 'in', ('sent','posted','draft')),
                                                            ('check_date', '>=', docs.from_date),
                                                            ('check_date', '<=', docs.to_date)])

        records = []
        total = 0
        for r in rec:
            vals = {'partner_id': r.partner_id,
                    'journal_id': r.journal_id,
                    'check_date': r.check_date,
                    'payment_date': r.payment_date,
                    'name': r.name,
                    'amount': r.amount,
                    }
            records.append(vals)
        return records

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = self.env['print.pdc.checks.wizard'].browse(self.env.context.get('active_id'))
        period = "From " + str(docs.from_date) + " To " + str(docs.to_date)
        pdc_data = self.get_pdc(docs)

        return {
            'doc_ids': self.ids,
            'docs': docs,
            'pdc_data': pdc_data,
            'period': period,
        }
