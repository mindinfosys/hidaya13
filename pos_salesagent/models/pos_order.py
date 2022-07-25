from functools import partial

from odoo import models, api, fields

class OrderLineCommission(models.Model):
    _inherit = 'pos.order.line'

    agent_comm_amt = fields.Float('Sales Agent Commision', default=0.00)

    @api.model
    def _order_line_fields(self, line, session_id=None):
        orderline = super(OrderLineCommission, self)._order_line_fields(line)
        product = self.env['product.product'].browse(orderline[2]['product_id'])
        orderline[2]['agent_comm_amt'] = product.sales_agent_commision
        return orderline



class OrderNotes(models.Model):
    _inherit = 'pos.order'

    agent_id = fields.Many2one('hr.employee', string='Agent')
    agent_commision = fields.Float('Agent Commision (%)', default=0.00)

    @api.model
    def _order_fields(self, ui_order):
        fields = super(OrderNotes, self)._order_fields(ui_order)
        # process_line = partial(self.env['pos.order.line']._order_line_fields, session_id=ui_order['pos_session_id'])
        objemp = self.env['hr.employee'].search([('id', '=', ui_order['agent_id']  if "agent_id" in ui_order else False)], limit=1)
        agentcom=0.00
        if objemp:
            agentcom=objemp.sales_commision
        # updated_lines = ui_order['lines']
        #
        # for rec in updated_lines:
        #     objproduct = self.env['product.product'].search([('id','=', rec[2]["product_id"])], limit=1)
        #     if objproduct:
        #         rec[2]["agent_comm_amt"]= objproduct.sales_agent_commision

        fields['agent_id'] = ui_order.get('agent_id', 0)#ui_order['agent_id']  if "agent_id" in ui_order else False,
        fields['agent_commision'] = float(agentcom or 0.0)

        return fields

