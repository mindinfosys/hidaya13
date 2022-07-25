from odoo import models, api, fields

class ProductTemplate_AgentCommision(models.Model):
    _inherit = 'product.template'

    sales_agent_commision = fields.Float('Sales Agent Commision', default=0.00)