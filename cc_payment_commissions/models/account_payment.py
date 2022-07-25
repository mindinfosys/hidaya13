# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging
 
log = logging.getLogger(__name__)
 
  
class AccountPaymentInherited(models.Model):
    _inherit = "account.payment"
              
    def _prepare_payment_moves(self):
        """
        Call super _prepare_payment_moves that returns list of journal entries containing dictionaries of journal items
        For each journal entry loop over the journal items and get the item where debit is added.
        Check if payment journal is of type bank and has provider_account set.
        If yes then reduce the debit by the provider commission and create a new journal item for the provider account with debit=commission
        """
          
        all_move_vals = super(AccountPaymentInherited, self)._prepare_payment_moves()
        company_currency = self.company_id.currency_id
          
        for move_vals in all_move_vals:
            if self.payment_type == 'inbound' and self.journal_id.type == 'bank' and self.journal_id.provider_ap_account:
                log.info(">> Setting commission for provider: '%s' from journal: '%s'", self.journal_id.provider_ap_account.name, self.journal_id.name)
                
                comm_fixed = self.journal_id.provider_commission_fixed
                comm_perc = self.journal_id.provider_commission_percent
                  
                credit_account = self.journal_id.default_credit_account_id
                  
                for line in move_vals['line_ids']:
                    
                    if line[2]['account_id'] == credit_account.id:
                        
                        fixed_comm_pay_curr = comm_fixed
                        if self.journal_id.currency_id != self.currency_id:
                            # Multi-currencies AND journal_currency != payment_currency --> Convert amount to payment currency
                            fixed_comm_pay_curr = self.journal_id.currency_id._convert(comm_fixed, self.currency_id, self.company_id, self.payment_date)
                            
                        currency_id = False
                        fixed_comm_comp_curr = fixed_comm_pay_curr
                        
                        if self.currency_id != company_currency:
                            # Multi-currencies AND payment_currency != company_currency --> Convert amount to company currency
                            currency_id = self.currency_id.id
                            fixed_comm_comp_curr = self.currency_id._convert(fixed_comm_pay_curr, company_currency, self.company_id, self.payment_date)
                        
                        debit = line[2]['debit']
                        amount_currency = line[2]['amount_currency']
                        
                        comm_comp_curr = fixed_comm_comp_curr + (comm_perc/100) * debit
                        comm_pay_curr = fixed_comm_pay_curr + (comm_perc/100) * amount_currency
                        
                        line[2]['debit'] = debit - comm_comp_curr
                        line[2]['amount_currency'] = amount_currency - comm_pay_curr
                        
                        move_vals['line_ids'].append((0, 0, {
                            'name': 'Commission',
                            'amount_currency': comm_pay_curr if currency_id else 0.0,
                            'debit': comm_comp_curr,
                            'currency_id': currency_id,
                            'credit': 0.0,
                            'date_maturity': self.payment_date,
                            'partner_id': self.partner_id.commercial_partner_id.id,
                            'account_id': self.journal_id.provider_ap_account.id,
                            'payment_id': self.id,
                        }))
                        
                        break
                        
        return all_move_vals
