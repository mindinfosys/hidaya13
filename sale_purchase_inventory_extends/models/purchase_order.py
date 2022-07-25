# -*- coding: utf-8 -*-

from odoo import models


class Purchase(models.Model):
    _inherit = 'purchase.order'

    def write(self, vals):
        res = super(Purchase, self).write(vals)
        for rec in self:
            if vals.get('state') and vals.get('state') == 'to approve':
                template = self.env.ref("sale_purchase_inventory_extends.custom_email_template_approve_purchase")
                template.send_mail(rec.id)
        return res
