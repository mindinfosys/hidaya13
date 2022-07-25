# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreateSoLine(models.TransientModel):
    _name = 'create.so.line'
    
    def create_inv_line(self):
        so_line_ids = self.env['sale.order.line'].browse(self._context.get('active_ids'))
        invoice_ids = so_line_ids.create_inv_custom()
        action = self.env.ref("account.action_move_out_invoice_type").read()[0]
        action['domain'] = [('id', 'in', invoice_ids.ids)]
        return action
