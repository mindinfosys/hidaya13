# -*- coding: utf-8 -*-

from odoo import models, fields, api
from collections import defaultdict


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #@Fully Override to remove warehouse for read qty_available based on source location
    @api.depends('product_id', 'customer_lead', 'product_uom_qty', 'product_uom', 'order_id.warehouse_id', 'order_id.commitment_date')
    def _compute_qty_at_date(self):
        """ Compute the quantity forecasted of product at delivery date. There are
        two cases:
         1. The quotation has a commitment_date, we take it as delivery date
         2. The quotation hasn't commitment_date, we compute the estimated delivery
            date based on lead time"""
        qty_processed_per_product = defaultdict(lambda: 0)
        grouped_lines = defaultdict(lambda: self.env['sale.order.line'])
        # We first loop over the SO lines to group them by warehouse and schedule
        # date in order to batch the read of the quantities computed field.
        for line in self:
            if not line.display_qty_widget:
                continue
            line.warehouse_id = line.order_id.warehouse_id
            if line.order_id.commitment_date:
                date = line.order_id.commitment_date
            else:
                date = line._expected_date()
            grouped_lines[(line.warehouse_id.id, date)] |= line

        treated = self.browse()
        for (warehouse, scheduled_date), lines in grouped_lines.items():
#            product_qties = lines.mapped('product_id').with_context(to_date=scheduled_date, warehouse=warehouse, location=lines.mapped("order_id").custom_source_location_id.id).read([
#                'qty_available',
#                'free_qty',
#                'virtual_available',
#            ])
            product_qties = lines.mapped('product_id').with_context(to_date=scheduled_date, location=lines.mapped("order_id").custom_source_location_id.id).read([
                'qty_available',
                'free_qty',
                'virtual_available',
            ])
            qties_per_product = {
                product['id']: (product['qty_available'], product['free_qty'], product['virtual_available'])
                for product in product_qties
            }
            for line in lines:
                line.scheduled_date = scheduled_date
                qty_available_today, free_qty_today, virtual_available_at_date = qties_per_product[line.product_id.id]
                line.qty_available_today = qty_available_today - qty_processed_per_product[line.product_id.id]
                line.free_qty_today = free_qty_today - qty_processed_per_product[line.product_id.id]
                line.virtual_available_at_date = virtual_available_at_date - qty_processed_per_product[line.product_id.id]
                if line.product_uom and line.product_id.uom_id and line.product_uom != line.product_id.uom_id:
                    line.qty_available_today = line.product_id.uom_id._compute_quantity(line.qty_available_today, line.product_uom)
                    line.free_qty_today = line.product_id.uom_id._compute_quantity(line.free_qty_today, line.product_uom)
                    line.virtual_available_at_date = line.product_id.uom_id._compute_quantity(line.virtual_available_at_date, line.product_uom)
                qty_processed_per_product[line.product_id.id] += line.product_uom_qty
            treated |= lines
        remaining = (self - treated)
        remaining.virtual_available_at_date = False
        remaining.scheduled_date = False
        remaining.free_qty_today = False
        remaining.qty_available_today = False
        remaining.warehouse_id = False
