# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        if self._context.get('custom_pos_session_close_at'):
            for vals in vals_list:
                vals.update({
                    'date': self._context.get('custom_pos_session_close_at')
                })
        return super(AccountMove, self).create(vals_list)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model_create_multi
    def create(self, vals_list):
        if self._context.get('custom_pos_analytic_account_id'):
            for vals in vals_list:
                vals.update({
                    'analytic_account_id': self._context.get('custom_pos_analytic_account_id')
                })
        return super(AccountMoveLine, self).create(vals_list)
