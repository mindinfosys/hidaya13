# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    custom_source_location_id = fields.Many2one(
        'stock.location',
        'Source Location',
        required=True,
    )
    custom_source_id = fields.Many2one(
        'custom.source.location',
        'Source',
        readonly=True,
    )
    
    @api.onchange('custom_source_id')
    def _onchange_custom_source_id(self):
        self.analytic_account_id = self.custom_source_id.analytic_account_id.id
        self.custom_source_location_id = self.custom_source_id.stock_location_id.id

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    custom_client_order_ref = fields.Char(
        string='Customer Reference',
        related='order_id.client_order_ref',
        store=True,
    )
    def _prepare_invoice_custom(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
#        self.ensure_one()
        # ensure a correct context for the _get_default_journal method and company-dependent fields
        if len(self.mapped('order_id').mapped('partner_id').ids) > 1:
            raise UserError(_("To create invoice Customer must be same of selected sale order lines"))
        so_order_id = self.mapped('order_id')[0]
        so_order_id = so_order_id.with_context(default_company_id=so_order_id.company_id.id, force_company=so_order_id.company_id.id)
        journal = so_order_id.env['account.move'].with_context(default_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (so_order_id.company_id.name, so_order_id.company_id.id))

        invoice_vals = {
#            'ref': self.client_order_ref or '',
            'type': 'out_invoice',
#            'narration': self.note,
#            'currency_id': self.pricelist_id.currency_id.id,
#            'campaign_id': self.campaign_id.id,
#            'medium_id': self.medium_id.id,
#            'source_id': self.source_id.id,
            'invoice_user_id': so_order_id.user_id and so_order_id.user_id.id,
#            'team_id': self.team_id.id,
            'partner_id': so_order_id.partner_invoice_id.id,
            'partner_shipping_id': so_order_id.partner_shipping_id.id,
            'invoice_partner_bank_id': so_order_id.company_id.partner_id.bank_ids[:1].id,
            'fiscal_position_id': so_order_id.fiscal_position_id.id or so_order_id.partner_invoice_id.property_account_position_id.id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': so_order_id.name,
#            'invoice_payment_term_id': self.payment_term_id.id,
#            'invoice_payment_ref': self.reference,
#            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': so_order_id.company_id.id,
        }
        return invoice_vals

    def _prepare_invoice_line_custom(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if self.display_type:
            res['account_id'] = False
        return res


    def create_inv_custom(self):
        invoice_vals = self._prepare_invoice_custom()
        for line in self:
            if line.qty_to_invoice > 0:
                invoice_vals['invoice_line_ids'].append((0, 0, line._prepare_invoice_line_custom()))
        
        if not invoice_vals['invoice_line_ids']:
            raise UserError(_('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))
        moves = self.env['account.move'].sudo().with_context(default_type='out_invoice').create(invoice_vals)
        return moves
