# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ProductBarcodeMulti(models.Model):
    _name = 'product.barcode.multi'
    _description = 'Product Barcode Multi'

    name = fields.Char(
        'code',
        required=True,
    )

    code_source = fields.Many2one('mis.code.source', string='Source')

    product_id = fields.Many2one(
        'product.product', 
        string='Product', 
        required=True,
        ondelete="cascade",
    )

class MisColCodeSource(models.Model):
    _name = 'mis.code.source'
    _description ='Barcode Source'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Barcode Source",  required=True, track_visibility='onchange')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Additional Product Code Source !"),
    ]