from odoo import models, fields, api

class StockQuant(models.Model):
    _inherit = "stock.quant"

    def action_print_labels(self):
        """Open the product.label.layout wizard for label printing."""
        self.ensure_one()
        products = self.mapped("product_id")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Choose Labels Layout',
            'res_model': 'product.label.layout',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_ids': [(6, 0, products.ids)],
            },
        }
