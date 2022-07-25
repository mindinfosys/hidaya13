import time
from datetime import date, datetime
import pytz
import json
import io
from odoo import api, fields, models, _
from odoo.tools import date_utils
import xlsxwriter
import base64
from datetime import timedelta


class StockReport(models.TransientModel):
    _name = "wizard.stock.history"
    _description = "Current Stock History"

    warehouse = fields.Many2many('stock.warehouse', 'wh_wiz_rel', 'wh', 'wiz', string='Warehouse', required=True)
    # category = fields.Many2many('product.category', 'categ_wiz_rel', 'categ', 'wiz', string='Warehouse')

    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)

    def export_xls(self):

        objlocation = self.env['stock.location'].search([('usage', '=', 'internal'), ('active', '=', True), ('company_id', 'in', self.warehouse.ids)], order='id')
        locationids = tuple([loc_id.id for loc_id in objlocation])

        date = datetime.now()
        report_name = 'stock_' + date.strftime("%y%m%d%H%M%S")
        date_string = date.strftime("%B-%y")
        filename = '%s %s' % (report_name, date_string)




        fp = io.BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf = {}

        comp = self.env.user.company_id.name
        sheet = workbook.add_worksheet('Stock Info')
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format4 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True})
        font_size_8 = workbook.add_format({'font_size': 8, 'align': 'center'})
        font_size_8_l = workbook.add_format({'font_size': 8, 'align': 'left'})
        font_size_8_r = workbook.add_format({'font_size': 8, 'align': 'right'})
        red_mark = workbook.add_format({'font_size': 8, 'bg_color': 'red'})
        justify = workbook.add_format({'font_size': 12})
        format3.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        #sheet.merge_range(1, 7, 2, 10, 'Product Stock Info', format0)
        #sheet.merge_range(3, 7, 3, 10, comp, format11)

        wbf['content_border'] = workbook.add_format()
        wbf['content_border'].set_top()
        wbf['content_border'].set_bottom()
        wbf['content_border'].set_left()
        wbf['content_border'].set_right()
        wbf['content_border'].set_text_wrap()

        wbf['content_border_red'] = workbook.add_format({'bg_color': 'red'})
        wbf['content_border_red'].set_top()
        wbf['content_border_red'].set_bottom()
        wbf['content_border_red'].set_left()
        wbf['content_border_red'].set_right()
        wbf['content_border_red'].set_text_wrap()

        wbf['content_border_bg'] = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bold': 1, 'bg_color': '#E1E1E1'})
        wbf['content_border_bg'].set_top()
        wbf['content_border_bg'].set_bottom()
        wbf['content_border_bg'].set_left()
        wbf['content_border_bg'].set_right()
        wbf['content_border_bg'].set_text_wrap()

        wbf['content_float_border'] = workbook.add_format({'align': 'right', 'num_format': '#,##0.00'})
        wbf['content_float_border'].set_top()
        wbf['content_float_border'].set_bottom()
        wbf['content_float_border'].set_left()
        wbf['content_float_border'].set_right()



        objstock = self.env['stock.quant'].search([('location_id', 'in', locationids)])
        productids = tuple([product_id.id for product_id in objstock])
        objproduct = self.env['product.product'].search([('id', 'in', productids)])
        rowno = 2
        colno = 0

        colno = 0
        column_width = 10
        sheet.set_column(colno, colno, column_width)
        sheet.write(1, colno, 'Sl#', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(1, colno, 'Barcode', wbf['content_border_bg'])

        colno += 1
        column_width = 65
        sheet.set_column(colno, colno, column_width)
        sheet.write(1, colno, 'Product', wbf['content_border_bg'])

        colno += 1
        column_width = 10
        sheet.set_column(colno, colno, column_width)
        sheet.write(1, colno, 'Cost', wbf['content_border_bg'])

        colno += 1
        column_width = 10
        sheet.set_column(colno, colno, column_width)
        sheet.write(1, colno, 'Sales Price', wbf['content_border_bg'])

        for recloc in objlocation:
            colno += 1
            column_width = 11
            sheet.set_column(colno, colno, column_width)
            sheet.write(1, colno, recloc.name, wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(1, colno, 'Total QTY Available', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(1, colno, 'Total Cost Value', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(1, colno, 'Total Sales Value', wbf['content_border_bg'])

        for rec in objproduct:
            colno = 0
            sheet.write(rowno, colno, rowno-1, wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, str(rec.barcode), wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, rec.name, wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, rec.standard_price, wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, rec.list_price, wbf['content_float_border'])

            totcost =0.00
            totsal=0.00
            totqty=0
            for rec_stk_loc in objlocation:
                colno += 1
                objstockqnt = self.env['stock.quant'].search([('product_id', '=', rec.id), ('location_id', '=', rec_stk_loc.id)], limit=1)
                if objstockqnt:
                    totqty+=objstockqnt.quantity
                    totcost+=objstockqnt.quantity*rec.standard_price
                    totsal+=objstockqnt.quantity*rec.list_price
                    if objstockqnt.quantity<0:
                        sheet.write(rowno, colno, objstockqnt.quantity, wbf['content_border_red'])
                    else:
                        sheet.write(rowno, colno, objstockqnt.quantity, wbf['content_border'])
                else:
                    sheet.write(rowno, colno, "", wbf['content_border'])

            colno += 1
            if totqty<0:
                sheet.write(rowno, colno, totqty, wbf['content_border_red'])
            else:
                sheet.write(rowno, colno, totqty, wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, totcost, wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, totsal, wbf['content_float_border'])


            rowno+=1

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
