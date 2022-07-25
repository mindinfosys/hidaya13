from datetime import date, datetime
from odoo.exceptions import UserError
from odoo.tools import date_utils
import xlsxwriter
import base64
from odoo import fields, models, api, _
from io import BytesIO
from pytz import timezone
from datetime import timedelta
import pytz

class ReportSaleAgentWizard(models.TransientModel):
    _name = 'salesagent.commission.wizard'

    report_start_date = fields.Date(string='Start Date', required=True)
    report_end_date = fields.Date(string='End Date', required=True)

    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)


    def download_report(self):
        date = datetime.now()
        report_name = 'sales_agent_commission_' + date.strftime("%y%m%d%H%M%S")
        date_string = self.report_start_date.strftime("%B-%y")
        header_date = self.report_start_date.strftime("%Y-%m-%d") + ' to ' + self.report_end_date.strftime("%Y-%m-%d")
        filename = '%s %s' % (report_name, date_string)

        filterstartdate = self.report_start_date
        filterenddate = self.report_end_date + timedelta(days=1)

        objposorder = self.env['pos.order'].search(
            [('agent_id', '!=', False), ('date_order', '>=', filterstartdate),
             ('date_order', '<', filterenddate)], order='date_order')

        #
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf = {}

        wbf['content'] = workbook.add_format()
        wbf['header'] = workbook.add_format({'bold': 1, 'align': 'center'})
        wbf['content_float'] = workbook.add_format({'align': 'right', 'num_format': '#,##0.00'})
        wbf['content_border'] = workbook.add_format()
        wbf['content_border'].set_top()
        wbf['content_border'].set_bottom()
        wbf['content_border'].set_left()
        wbf['content_border'].set_right()

        wbf['content_date'] = workbook.add_format({'align': 'center', 'num_format': 'yyyy-mm-dd'})
        wbf['content_date'].set_top()
        wbf['content_date'].set_bottom()
        wbf['content_date'].set_left()
        wbf['content_date'].set_right()

        wbf['content_float_border'] = workbook.add_format({'align': 'right', 'num_format': '#,##0.00'})
        wbf['content_float_border'].set_top()
        wbf['content_float_border'].set_bottom()
        wbf['content_float_border'].set_left()
        wbf['content_float_border'].set_right()

        wbf['content_border_bg'] = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bold': 1, 'bg_color': '#E1E1E1'})
        wbf['content_border_bg'].set_top()
        wbf['content_border_bg'].set_bottom()
        wbf['content_border_bg'].set_left()
        wbf['content_border_bg'].set_right()
        wbf['content_border_bg'].set_text_wrap()


        wbf['header'] = workbook.add_format({'bold': 1, 'align': 'center'})

        worksheet = workbook.add_worksheet('Commission Detail')

        colno = 0
        column_width = 15
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Date', wbf['content_border_bg'])

        colno += 1
        column_width = 20
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'POS Name', wbf['content_border_bg'])

        colno += 1
        column_width = 20
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Order Name', wbf['content_border_bg'])

        colno += 1
        column_width = 25
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Order Ref', wbf['content_border_bg'])

        colno += 1
        column_width = 20
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Agent Name', wbf['content_border_bg'])

        colno += 1
        column_width = 60
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Product', wbf['content_border_bg'])

        colno += 1
        column_width = 10
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Qty', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Commission per Qty', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Total SO Amount (Total - Tax - Discount)', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Commission %', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Commission per SO', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        worksheet.set_column(colno, colno, column_width)
        worksheet.write(1, colno, 'Total Commission', wbf['content_border_bg'])
        worksheet.merge_range('A%s:L%s' % (1, 1), 'SALES AGENT COMMISSION REPORT ' + str(header_date), wbf['header'])
        rowno =2
        colno =0
        summary_amount = {}
        summary_amount_bypos = {}

        for recorder in objposorder:
            colno = 0
            worksheet.write(rowno, colno, recorder.date_order, wbf['content_date'])
            colno += 1
            worksheet.write(rowno, colno, recorder.session_id.config_id.name, wbf['content_border'])
            colno += 1
            worksheet.write(rowno, colno, recorder.name, wbf['content_border'])
            colno += 1
            worksheet.write(rowno, colno, recorder.pos_reference, wbf['content_border'])
            colno += 1
            worksheet.write(rowno, colno, recorder.agent_id.name, wbf['content_border'])
            colno += 1
            worksheet.write(rowno, colno, "Commission for the Sales Order", wbf['content_border'])
            colno += 1
            worksheet.write(rowno, colno, "", wbf['content_float_border'])
            colno += 1
            worksheet.write(rowno, colno, "", wbf['content_float_border'])
            colno += 1
            worksheet.write(rowno, colno, (recorder.amount_paid - recorder.amount_tax), wbf['content_float_border'])
            colno += 1
            worksheet.write(rowno, colno, recorder.agent_commision, wbf['content_float_border'])
            colno += 1
            amtcom = (recorder.agent_commision * (recorder.amount_paid - recorder.amount_tax) / 100)
            worksheet.write(rowno, colno, amtcom, wbf['content_float_border'])
            colno += 1

            worksheet.write(rowno, colno,amtcom , wbf['content_float_border'])
            colno += 1

            totalcom = amtcom
            if (recorder.agent_id.name in summary_amount):
                tmptotal = float(summary_amount[recorder.agent_id.name]) + totalcom
                summary_amount[recorder.agent_id.name] = tmptotal
            else:
                summary_amount[recorder.agent_id.name] = totalcom



            if (recorder.session_id.config_id.name+','+recorder.agent_id.name in summary_amount_bypos):
                tmptotal = float(summary_amount_bypos[recorder.session_id.config_id.name+','+recorder.agent_id.name]) + totalcom
                summary_amount_bypos[recorder.session_id.config_id.name+','+recorder.agent_id.name] = tmptotal
            else:
                summary_amount_bypos[recorder.session_id.config_id.name+','+recorder.agent_id.name] = totalcom

            rowno += 1

            objposorderline = self.env['pos.order.line'].search([('order_id', '=',recorder.id)])
            for rec in objposorderline:
                colno = 0
                worksheet.write(rowno, colno, recorder.date_order, wbf['content_date'])
                colno += 1
                worksheet.write(rowno, colno, recorder.session_id.config_id.name, wbf['content_border'])
                colno+=1
                worksheet.write(rowno, colno, recorder.name, wbf['content_border'])
                colno += 1
                worksheet.write(rowno, colno, recorder.pos_reference, wbf['content_border'])
                colno += 1
                worksheet.write(rowno, colno, recorder.agent_id.name, wbf['content_border'])
                colno += 1
                worksheet.write(rowno, colno, rec.product_id.name, wbf['content_border'])
                colno += 1
                worksheet.write(rowno, colno, rec.qty, wbf['content_float_border'])
                colno += 1
                worksheet.write(rowno, colno, rec.agent_comm_amt, wbf['content_float_border'])
                colno += 1
                worksheet.write(rowno, colno, "", wbf['content_float_border'])
                colno += 1
                worksheet.write(rowno, colno, "", wbf['content_float_border'])
                colno += 1
                worksheet.write(rowno, colno, "", wbf['content_float_border'])
                colno += 1
                totalcom = rec.qty*rec.agent_comm_amt
                worksheet.write(rowno, colno,totalcom , wbf['content_float_border'])

                if (recorder.agent_id.name in summary_amount):
                    tmptotal = float(summary_amount[recorder.agent_id.name]) + totalcom
                    summary_amount[recorder.agent_id.name] = tmptotal
                else:
                    summary_amount[recorder.agent_id.name] = totalcom

                if (recorder.session_id.config_id.name + ',' + recorder.agent_id.name in summary_amount_bypos):
                    tmptotal = float(summary_amount_bypos[
                                         recorder.session_id.config_id.name + ',' + recorder.agent_id.name]) + totalcom
                    summary_amount_bypos[recorder.session_id.config_id.name + ',' + recorder.agent_id.name] = tmptotal
                else:
                    summary_amount_bypos[recorder.session_id.config_id.name + ',' + recorder.agent_id.name] = totalcom


                rowno+=1

        worksheet2 = workbook.add_worksheet('Commission Summary')

        colno = 0
        column_width = 30
        worksheet2.set_column(colno, colno, column_width)
        worksheet2.write(1, colno, 'Agent Name', wbf['content_border_bg'])

        colno += 1
        column_width = 25
        worksheet2.set_column(colno, colno, column_width)
        worksheet2.write(1, colno, 'Total Commission', wbf['content_border_bg'])


        rowno = 2
        colno = 0
        for reccom in summary_amount:
            colno = 0
            worksheet2.write(rowno, colno, reccom, wbf['content_border'])
            colno += 1
            worksheet2.write(rowno, colno, summary_amount[reccom], wbf['content_float_border'])
            rowno+=1




    #========================== by pos

        worksheet3 = workbook.add_worksheet('Commission Summary by POS')

        colno = 0
        column_width = 30
        worksheet3.set_column(colno, colno, column_width)
        worksheet3.write(1, colno, 'POS Name', wbf['content_border_bg'])
        colno += 1
        worksheet3.set_column(colno, colno, column_width)
        worksheet3.write(1, colno, 'Agent Name', wbf['content_border_bg'])

        colno += 1
        column_width = 25
        worksheet3.set_column(colno, colno, column_width)
        worksheet3.write(1, colno, 'Total Commission', wbf['content_border_bg'])

        rowno = 2
        colno = 0
        for reccom in summary_amount_bypos:
            colno = 0
            agnamepos = reccom.split(",")
            worksheet3.write(rowno, colno, agnamepos[0], wbf['content_border'])
            colno += 1
            worksheet3.write(rowno, colno, agnamepos[1], wbf['content_border'])
            colno += 1
            worksheet3.write(rowno, colno, summary_amount_bypos[reccom], wbf['content_float_border'])
            rowno += 1

        workbook.close()
        out = base64.encodestring(fp.getvalue())
        self.write({'datas': out, 'datas_fname': filename})
        fp.close()
        filename += '%2Exlsx'

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model=' + self._name + '&id=' + str(
                self.id) + '&field=datas&download=true&filename=' + filename,
        }
