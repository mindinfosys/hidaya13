# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreatePO(models.TransientModel):
    _name = 'custom.product.create.po'
    _description = 'Product create PO'

    @api.model
    def _get_picking_type(self):
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', self.env.company.id)])
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return picking_type[:1]

    vendor_id = fields.Many2one(
        'res.partner',
        string='Vendor',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self:self.env.company.id,
    )
    picking_type_id = fields.Many2one(
        'stock.picking.type',
        string='Deliver To',
        domain="['|', ('warehouse_id', '=', False), ('warehouse_id.company_id', '=', company_id)]",
        default=_get_picking_type,
    )

    def _prepare_po_line_vals(self, product_ids, order_id):
        po_line_vals = {}
        line_lst = []
        po_line = self.env['purchase.order.line']
        for product in product_ids:
            vals = {
                'product_id': product.id,
                'product_qty': product.reordering_min_qty - product.qty_available,
                'order_id': order_id.id,
            }
            po_line_new = po_line.new(vals)
            po_line_new.onchange_product_id()
            po_line_new._onchange_quantity()
            po_line_values = po_line_new._convert_to_write({
                name: po_line_new[name] for name in po_line_new._cache
            })
            po_line_values.update({
                'product_qty': product.reordering_min_qty - product.qty_available,
            })
            line_lst.append((0, 0, po_line_values))
        po_line_vals.update({
            'order_line': line_lst,
        })
        return po_line_vals
        
    def _prepare_po_vals(self):
        po_obj = self.env['purchase.order']
        po_vals = {
            'partner_id': self.vendor_id.id,
            'company_id': self.company_id.id,
            'picking_type_id': self.picking_type_id.id,
        }
        po_new = po_obj.new(po_vals)
        po_new.onchange_partner_id()
        po_values = po_new._convert_to_write({
            name: po_new[name] for name in po_new._cache
        })
        return po_values
    
    def create_product_po(self):
        product_ids = self.env['product.product'].browse(self._context.get('active_ids'))
        purchase_order_vals = self._prepare_po_vals()
        purchase_order = self.env['purchase.order'].create(purchase_order_vals)
        po_line_vals = self._prepare_po_line_vals(product_ids, purchase_order)
        purchase_order.write(po_line_vals)
        action = self.env.ref("purchase.purchase_rfq").read()[0]
        action['domain'] = [('id', 'in', purchase_order.ids)]
        return action
