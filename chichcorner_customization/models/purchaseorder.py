from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    total_product_qty = fields.Float(
        string="Total Product Quantity",
        compute="_compute_total_product_qty",
        store=True
    )

    @api.depends('order_line.product_qty')
    def _compute_total_product_qty(self):
        for order in self:
            order.total_product_qty = sum(line.product_qty for line in order.order_line)
