# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError, UserError
class account_payment(models.Model):
    _inherit = "account.payment"

    check_layout = fields.Char('Layout')
    check_date = fields.Date('Check Date')



    def do_print_checks(self):

#         if self:
#             journal_name =self[0].journal_id.name
#             self.write({'state': 'sent'})
#             check_layout = 'action_print_check_layout1'
#
#             if journal_name=='ADIB - 17952837 (CA)':
#                 check_layout='action_print_check_layout1'
#             elif journal_name=='ADCB - 265070920012 (CA)':
#                 check_layout='action_print_check_layout2'
# #               else:
# #                  check_layout = 'action_print_check_middle'

        return self.env.ref('mis_check_printing.action_print_check_%s' % self.check_layout).report_action(self)
        return super(account_payment, self).do_print_checks()
