# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    barcode_ids = fields.One2many(related='product_variant_ids.barcode_ids', readonly=False)
    arabic_name = fields.Char('Arabic Name')
    brand = fields.Many2one('mis.product.brand', string='Brand')

class MisColProductBrand(models.Model):
    _name = 'mis.product.brand'
    _description = 'Product Band'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Brand",  required=True, track_visibility='onchange')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Product Brand !"),
    ]