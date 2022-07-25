import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class PrintPDCChecks(models.TransientModel):
    _name = 'print.pdc.checks.wizard'
    _description = 'PDC Report'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string="To Date", required=True)
    report_type = fields.Selection([("All", "All"), ("UnReconciled", "UnReconciled"), ("Reconciled", "Reconciled")], string="Type", required=True, default='UnReconciled')

    def pdc_report(self):
        data = {
            'start_date': self.from_date,
            'end_date': self.to_date,
            'report_type': self.report_type
        }
        return self.env.ref('mis_pdc_report.action_report_print_pdc').report_action(self, data=data)

