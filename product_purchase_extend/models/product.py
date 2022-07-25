# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Product(models.Model):
    _inherit = 'product.product'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        res = super(Product, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
        if self._context.get('search_qty_hand_min_reord_qty'):
            res = self.browse(res).filtered(lambda product:product.qty_available <= product.reordering_min_qty).ids
        return res
