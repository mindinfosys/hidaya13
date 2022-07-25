from odoo import models, fields, api, _


class ReturnPickingInv(models.TransientModel):
    _inherit = 'stock.return.picking'

    custom_journal_id = fields.Many2one(
        'account.journal',
        'Use Journal',
    )
    picking_type_code = fields.Selection(
        related="picking_id.picking_type_id.code",
        stored=True,
    )

    def _prepare_credit_note_vals(self):
        picking = self.picking_id
        return {
            'partner_id': picking.partner_id.id,
            'ref': picking.name,
            'invoice_line_ids': [],
            'type' : 'out_refund' if self.picking_type_code == 'outgoing' else 'in_refund' if self.picking_type_code == 'incoming' else '',
            'journal_id': self.custom_journal_id.id,
            'invoice_payment_term_id': picking.partner_id.property_payment_term_id.id,
            'company_id': self.env.user.company_id.id,
            'currency_id': self.env.user.company_id.currency_id.id,
        }

    def _prepare_credit_note_line_vals(self):
        line_lst = []
        for r_move in self.product_return_moves:
            line_lst.append((0, 0, {
                'product_id': r_move.product_id.id,
                'quantity': r_move.quantity,
                'price_unit': r_move.move_id.price_unit,
                'product_uom_id': r_move.uom_id.id,
            }))
        return line_lst

    def _action_credit_debit_reverse(self):
        credit_note_vals = self._prepare_credit_note_vals()
        credit_note_vals['invoice_line_ids'] = self._prepare_credit_note_line_vals()
        new_moves = self.env['account.move'].create(credit_note_vals)

        action = {
            'name': _('Reverse Moves'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
        }
        if len(new_moves) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': new_moves.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', new_moves.ids)],
            })
        return action

    def create_returns_credit_debit(self):
        self.create_returns()
        return self._action_credit_debit_reverse()
