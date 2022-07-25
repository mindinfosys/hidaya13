from datetime import datetime

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, AccessError




class prevurchaselinewiz(models.TransientModel):
    _name = "purchaseline.prev"
    _description = ' Purchase Product History'
    _order = 'date desc'
    
    wiz_id = fields.Many2one('purchaseline.wizard')
    po_order = fields.Many2one('purchase.order',string="Purchase Order")
    unit_price = fields.Float(string="Unit Price")
    vendor = fields.Many2one('res.partner',string="Vendor")
    quantity = fields.Float(string="Quantity")
    po_date =fields.Datetime(string="Purchase Date")
    
    
class PurchaseOrderlinewiz(models.TransientModel):
    _name = "purchaseline.wizard"
    _description = ' Purchase Product History Wizard'
    @api.model
    def _get_purchase_lines(self):
        lines = self.env['purchase.order.line']
        PurchaseOrderLines = lines.browse(self._context.get('active_ids'))[0]
        product_id=PurchaseOrderLines.product_id.id
        PurchaseHistoryLines=lines.search([('product_id','=',product_id)])
        vals = []
        for line in PurchaseHistoryLines:
            purchase_id=line.order_id
            if purchase_id.state in ['purchase','done']:
                po_order_id=line.order_id.id
                vendor=purchase_id.partner_id.id
                quantity=line.product_qty
                date=line.date_order
                price_unit=line.price_unit
                vals.append((0, 0, {'po_order':po_order_id,
                                    'unit_price':price_unit,
                                    'vendor':vendor,
                                    'quantity':quantity,
                                    'po_date':date,
                                    }))
        return vals
    
    purchase_lines=fields.One2many('purchaseline.prev','wiz_id',string="Purchases" ,default=_get_purchase_lines)
    
    
  