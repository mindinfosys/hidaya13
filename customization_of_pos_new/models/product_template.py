from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_group_invisible = fields.Boolean( compute='_compute_current_group')

    # flag = self.pool.get('res.users').has_group(cr, uid, 'base.group_sale_manager')
    def _compute_current_group(self):
           print(self.user_has_groups('customization_of_pos_new.group_hide_templates'))
           self.is_group_invisible =  self.user_has_groups('customization_of_pos_new.group_hide_product_templates')