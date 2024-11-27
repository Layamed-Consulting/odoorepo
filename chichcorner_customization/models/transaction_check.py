from odoo import models, fields,api,_
import datetime
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class TransactionCheck(models.Model):
    _name = "transaction.check"
    _description = "Check Transaction"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string="Date", required=True)
    magasin_name = fields.Many2one(
        'pos.config',
        string="Magasin",
        required=True,
        domain=[('id', '!=', False)]
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft')

    transaction_ids = fields.One2many("transaction.session", "check_id", string="Relevés")

    @api.onchange('date', 'magasin_name')
    def _filter_transactions_by_date(self):
        """Populate transaction_ids with transactions matching the selected date."""
        if self.date and self.magasin_name:
            _logger.info(f"Filtering transactions for date: {self.date}")

            start_datetime = datetime.datetime.combine(self.date, datetime.time.min)
            end_datetime = datetime.datetime.combine(self.date, datetime.time.max)

            _logger.info(f"Search range: {start_datetime} to {end_datetime}")

            transactions = self.env['transaction.session'].search([
                ('close_time', '>=', start_datetime),
                ('close_time', '<=', end_datetime),
                ('store_name', '=', self.magasin_name.name),
                ('check_id', '=', False)
            ])

            _logger.info(f"Found {len(transactions)} transactions")
            for trans in transactions:
                _logger.info(f"Transaction ID: {trans.id}, Session: {trans.session_id.name}")

            self.transaction_ids = [(5, 0, 0)]
            _logger.info("Cleared existing transaction records")

            if transactions:
                self.transaction_ids = [(4, transaction.id) for transaction in transactions]
                _logger.info(f"Added {len(transactions)} transactions to transaction_ids")
            else:
                _logger.warning("No transactions found for the selected date")

    def write(self, vals):
        _logger.info(f"Writing values to transaction.check: {vals}")
        return super(TransactionCheck, self).write(vals)