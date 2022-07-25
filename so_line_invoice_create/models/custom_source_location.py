# -*- coding: utf-8 -*-

from odoo import models, fields


class SourceLocation(models.Model):
    _name = 'custom.source.location'
    _description = 'Warehouse location'

    name = fields.Char(
        string='Name',
        required=True,
    )
    stock_location_id = fields.Many2one(
        'stock.location',
        'Source Location',
        required=True,
    )

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
    )
