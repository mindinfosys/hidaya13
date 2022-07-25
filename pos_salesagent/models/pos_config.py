from odoo import models, fields

class Configuration(models.Model):
    _inherit = 'pos.config'

    agent_configuration = fields.Boolean(string='Enable Sales Agent Selection', default=False,
                                          help='Allow to select Sales Agent in POS interface')

