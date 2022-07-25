# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _write(self, vals):
        res = super(StockPicking, self)._write(vals)
        if vals.get('sale_id'):
            for rec in self:
                rec.location_id = rec.sale_id.custom_source_location_id.id
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_qty_onhand = fields.Float(
        string='Onhand Quantity',
    )

    @api.model
    def create(self, vals):
        rec = super(StockMove, self).create(vals)
        if vals.get('product_id'):
            rec.product_qty_onhand = rec.product_id.qty_available
        return rec
    
    def write(self, vals):
        res = super(StockMove, self).write(vals)
        if vals.get('product_id'):
            for rec in self:
                rec.product_qty_onhand = product_id.qty_available
        return res
