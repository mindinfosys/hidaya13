# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class PartnerUnique(models.Model):
    _inherit = 'res.partner'
          
    @api.constrains('name')
    def _check_unique_constraint(self):
        for rec in self:
            if rec.name.isspace() == True:
                raise ValidationError(_('Space in partner name not allow.'))

            record = rec.search([('name', '=ilike', rec.name),('id','!=',rec.id)])
            if record:
               raise ValidationError(_('Another partner with the same name exists!'))
    
    @api.model
    def create(self, vals):
        res = super(PartnerUnique, self).create(vals)
        res.name = res.name.rstrip().lstrip()
        return res
    
    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].rstrip().lstrip()
        return super(PartnerUnique, self).write(vals)
