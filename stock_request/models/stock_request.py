from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

REQUEST_STATES = [
    ("draft", "Draft"),
    ("open", "In progress"),
    ("done", "Done"),
    ("cancel", "Cancelled"),
]

class StockRequest(models.Model):
    _name = "stock.request"
    _description = "Stock Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    def __get_request_states(self):
        return REQUEST_STATES

    def _get_request_states(self):
        return self.__get_request_states()

    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)

    @staticmethod
    def _get_expected_date():
        return fields.Datetime.now()



    name = fields.Char(states={"draft": [("readonly", False)]})
    company_id = fields.Many2one("res.company", "Company", required=True, default=lambda self: self.env.company)
    state = fields.Selection(
        selection=_get_request_states,
        string="Status",
        copy=False,
        default="draft",
        index=True,
        readonly=True,
        track_visibility="onchange",
    )
    requested_by = fields.Many2one(
        "res.users",
        "Requested by",
        required=True,
        track_visibility="onchange",
        default=lambda s: s._get_default_requested_by(),
    )
    expected_date = fields.Datetime(
        "Expected Date",
        default=lambda s: s._get_expected_date(),
        index=True,
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Date when you expect to receive the goods.",
    )

    from_location_id = fields.Many2one(
        "stock.location",
        "From Location",
        domain=[("usage", "in", ["internal"])],
        ondelete="cascade",
        required=True,
    )

    to_location_id = fields.Many2one(
        "stock.location",
        "To Location",
        domain=[("usage", "in", ["internal"])],
        ondelete="cascade",
        required=True,
    )

    remarks = fields.Text('Remark')
    request_type = fields.Many2one('stock.request.type', 'Request Type', required="1")


    picking_count = fields.Integer(
        string="Delivery Orders", compute="_compute_picking_ids", readonly=True
    )

    request_ids = fields.One2many("stock.request.line", 'stock_request_id',string='Request Lines')


    _sql_constraints = [
        ("name_uniq", "unique(name, company_id)", "Stock Request name must be unique")
    ]

    @api.constrains("from_location_id", "to_location_id")
    def check_order_location(self):
        if self.from_location_id == self.to_location_id:
            raise ValidationError(_("From Location and To Location must be different"))


    def _action_confirm(self):
        for rec in self.request_ids:
            rec.qty_in_progress= rec.product_uom_qty
        self.state = "open"

    def action_confirm(self):
        self._action_confirm()
        return True

    def action_draft(self):
        self.write({"state": "draft"})
        return True
    def action_draft_manager(self):
        self.write({"state": "draft"})
        return True

    def action_cancel(self):
        for rec in self.request_ids:
            rec.qty_in_progress= 0
            rec.qty_done=0
        self.state = "cancel"
        return True

    def action_done(self):
        for rec in self.request_ids:
            rec.qty_in_progress= rec.product_uom_qty
            rec.qty_done= rec.product_uom_qty
        self.state = "done"

        return True


    @api.model
    def create(self, vals):
        upd_vals = vals.copy()
        if upd_vals.get("name", "/") == "/":
            upd_vals["name"] = self.env["ir.sequence"].next_by_code("stock.request")
        return super(StockRequest, self).create(upd_vals)

    def unlink(self):
        if self.filtered(lambda r: r.state != "draft"):
            raise UserError(_("Only requests on draft state can be unlinked"))
        return super(StockRequest, self).unlink()

class StockRequestLine(models.Model):
    _name = "stock.request.line"
    _description = "Stock Request Line"
    _order = "id desc"

    stock_request_id = fields.Many2one('stock.request', string='Request line id')

    product_id = fields.Many2one(
        "product.product",
        "Product",
        domain=[("type", "in", ["product", "consu"])],
        ondelete="cascade",
        required=True,
    )
    product_uom_id = fields.Many2one(
        "uom.uom",
        "Product Unit of Measure",

    )

    product_uom_qty = fields.Float(
        "Quantity",
        digits="Product Unit of Measure",

        help="Quantity, specified in the unit of measure indicated in the request.",
    )

    company_id = fields.Many2one("res.company", "Company", required=True, default=lambda self: self.env.company)

    qty_in_progress = fields.Float(
        "Qty In Progress",
        digits="Product Unit of Measure",
        readonly=True,
        compute="_compute_qty",
        store=True,
        help="Quantity in progress.",
    )
    qty_done = fields.Float(
        "Qty Done",
        digits="Product Unit of Measure",
        readonly=True,
        compute="_compute_qty",
        store=True,
        help="Quantity completed",
    )
    @api.onchange('product_id')
    def _prodcut_onchage(self):
        self.product_uom_id=self.product_id.uom_id.id


class StockRequestType(models.Model):
    _name ='stock.request.type'
    _description ='Stock Request Type'

    name = fields.Char('Request Type')