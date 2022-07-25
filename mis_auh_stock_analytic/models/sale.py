# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.analytic_account_id:
            for pick in self.picking_ids:
                pick.analytic_id = self.analytic_account_id.id
                for line in pick.move_ids_without_package:
                    line.write({
                    	"analytic_account_id": self.analytic_account_id.id
                    	})
        for s_line in self.order_line:
            if s_line.analytic_tag_ids:
                tags = s_line.mapped('analytic_tag_ids')
                for move in s_line.move_ids:
                    move.write({
                            'custom_analytic_tag_ids': [(6, 0, tags.ids)]
                            })
        return res
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
