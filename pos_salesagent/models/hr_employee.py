from odoo import models, fields

class EmployeeMasterExtend(models.Model):

    _inherit = 'hr.employee'

    is_a_agent = fields.Boolean(string='Is a Sales Agent',
                                 help='Enable this field to mark the normal employee as a Sales Agent')

    sales_commision = fields.Float('Sales Commision (%)', default=0.00)

class HrEmployeePublicExtend(models.Model):
    _inherit = "hr.employee.public"

    is_a_agent = fields.Boolean(readonly=True)
    sales_commision = fields.Float(readonly=True)
