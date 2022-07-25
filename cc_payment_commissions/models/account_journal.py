# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountJournalInherited(models.Model):
    _inherit = "account.journal"
    
    provider_ap_account = fields.Many2one('account.account', default=None, string="Provider Account", help="Provider account where commissions are added")
    provider_commission_fixed = fields.Float("Provider Commission Fixed Fees", help="Commission fixed amount to be deducted from the payment")
    provider_commission_percent = fields.Float("Provider Commission Percentage", help="Commission percentage to be  deducted from the payment")
    
    @api.constrains('provider_commission_fixed', 'provider_commission_percent')
    def validate_provider_commission(self):
    
        for obj in self:
            if obj.provider_commission_fixed < 0:
                raise ValidationError("Commission fixed amount should be greater than 0")
            if obj.provider_commission_percent < 0 or obj.provider_commission_percent > 100:
                raise ValidationError("Commission percentage should be between 0 and 100")
            
        return True
