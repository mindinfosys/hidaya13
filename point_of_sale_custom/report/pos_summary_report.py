from odoo import models, api
from datetime import timedelta, datetime, date
from odoo.exceptions import ValidationError, UserError

class POSSummaryReport(models.AbstractModel):
    _name = "report.point_of_sale_custom.report_pos_closingsummary"
    _description = "POS Summary Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        session_id=0
        objsession =self.env['pos.session'].browse(docids)

        for rec in docids:
            session_id = rec

        startat = objsession.start_at+timedelta(hours=4)
        endat = objsession.stop_at+timedelta(hours=4)

        strsql ="""select session_id,employee_id,cashier,sum(amount_tax) as amttax,sum(amount_total) as amttot from pos_order where session_id=""" + str(session_id) + """ group by session_id,employee_id,cashier
order by session_id"""

        self._cr.execute(strsql)
        objrec = self._cr.dictfetchall()
        sales_table = {}
        payment_table = {}

        rowindex =0
        total_sales=0.0
        total_tax =0.0
        for line in objrec:
            sales_table[rowindex]=line
            total_sales+=line['amttot']
            total_tax+=line['amttax']
            rowindex+=1

        strsql = """select pm.session_id,ppm.name as payment_method, sum(pm.amount)  as payment_amount from pos_payment pm, pos_payment_method ppm where pm.payment_method_id = ppm.id and pm.session_id=""" + str(
            session_id) + """ group by pm.session_id,ppm.name order by pm.session_id"""
        self._cr.execute(strsql)
        objpaymentrec = self._cr.dictfetchall()

        rowindex = 0
        total_payment=0.0
        for pline in objpaymentrec:
            payment_table[rowindex] = pline
            total_payment+=pline['payment_amount']
            rowindex += 1

        strsql = """select COALESCE(sum(price_subtotal_incl),0.0) as discount from pos_order_line where product_id =2 and  order_id in (select id from pos_order where session_id=""" + str(
            session_id) + """ )"""
        self._cr.execute(strsql)
        objdiscountrec = self._cr.dictfetchall()

        discount_amount = 0.0
        for discountrec in objdiscountrec:
            discount_amount += discountrec['discount']

        strsql = """select sum((price_unit*qty)-price_subtotal_incl) as discount from pos_order_line where order_id in (select id from pos_order where session_id=""" + str(
            session_id) + """ )"""
        self._cr.execute(strsql)
        objdiscount1rec = self._cr.dictfetchall()
        for discount1rec in objdiscount1rec:
            discount_amount += discount1rec['discount']


        docargs = {
            'doc_ids': docids,
            'docs': self.env['pos.session'].browse(docids),
            'doc_model': 'pos.session',
            'saletable': sales_table,
            'payment_table': payment_table,
            'discount_amount': discount_amount,
            'total_sales': total_sales,
            'total_tax': total_tax,
            'total_payment':total_payment,
            'startat':startat,
            'endat': endat,

        }
        return docargs