# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from odoo import models, fields

class POSConfig(models.Model):
    _inherit = "pos.config"

    custom_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
    )

class POSSession(models.Model):
    _inherit = "pos.session"

    stop_at = fields.Datetime(
        readonly=False,
    )
    custom_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
    )

    total_cost = fields.Float('Total Cost', compute='_calculate_cost')



    def _calculate_cost(self):

        for rec in self:
            totalcost = 0.0
            objorder = self.env['pos.order'].search([('session_id', '=', rec.id)])
            for orec in objorder:
                objorderln = self.env['pos.order.line'].search([('order_id', '=', orec.id)])
                for rlrec in objorderln:
                    objprod = self.env['product.product'].search([('id', '=', rlrec.product_id.id)])
                    if objprod:
                        totalcost+= rlrec.qty * objprod.standard_price
            rec.total_cost= totalcost




    def action_pos_session_open(self):
        # second browse because we need to refetch the data from the DB for cash_register_id
        # we only open sessions that haven't already been opened
        for session in self.filtered(lambda session: session.state in ('new_session', 'opening_control')):
            values = {}
            if not session.start_at:
                values['start_at'] = fields.Datetime.now()
            if not session.custom_analytic_account_id:
                values['custom_analytic_account_id'] = self.config_id.custom_analytic_account_id.id
            values['state'] = 'opened'
            session.write(values)
            session.statement_ids.button_open()
        return True

    def write(self, vals):
        if vals.get('stop_at') and self._context.get('custom_action_session_close'):
            for rec in self:
                if rec.stop_at:
                    vals.pop('stop_at')
        return super(POSSession, self).write(vals)

    def action_pos_session_closing_control(self):
        res = super(POSSession, self.with_context(custom_action_session_close=True)).action_pos_session_closing_control()
        return res

    def _create_account_move(self):
        timezone_tz = 'utc'
        user_id = self.env.user
        if user_id.tz:
            timezone_tz = user_id.tz
        local = pytz.timezone(timezone_tz)
        local_dt = local.utcoffset(self.stop_at)
        custom_pos_session_close_at = (self.stop_at + local_dt).date() #CONVERT UTC TIME TO USER TIMEZONE
#        res = super(POSSession, self.with_context(custom_pos_session_close_at=self.stop_at.date()))._create_account_move()
        res = super(POSSession, self.with_context(custom_pos_session_close_at=custom_pos_session_close_at,custom_pos_analytic_account_id=self.custom_analytic_account_id.id))._create_account_move()
        return res
