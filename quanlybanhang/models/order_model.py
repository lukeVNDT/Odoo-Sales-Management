from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _, tools
from datetime import datetime
import uuid


def default_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.upper()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    return random[0:string_length]  # Return the random string.


class OrderModel(models.Model):
    _name = "order.model"
    _description = "order management model"
    name = fields.Char(string="Name of Order")
    date_order = fields.Datetime(string="Date Order", default=datetime.today())
    amount = fields.Float(string="Amount all", compute="amount_all_quotation", store=True, digits=(12, 0))
    customer_id = fields.Many2one('customer.model', required=True)
    user_id = fields.Many2one('res.users', string='Salesperson', required=True)
    order_details = fields.One2many('order.detail', 'order_id', string='Order Details', copy=True, auto_join=True,
                                    required=True)
    shipping_address = fields.Char(string="Shipping address", store=True)
    sign_by = fields.Char(string="Sign by")
    sign_on = fields.Datetime(string="Sign on")
    sign_image = fields.Image(string="Sign image")
    shipping_phone = fields.Char(string="Shipping phone", default=False, store=True)
    state = fields.Selection([
        ('mới', 'Mới'),
        ('xác nhận', 'Đã xác nhận'),
        ('hoàn thành', 'Hoàn thành'),
        ('hủy bỏ', 'Hủy bỏ'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='mới')

    @api.model
    def create(self, vals):
        vals['name'] = default_random_string(6)
        result = super(OrderModel, self).create(vals)
        return result

    @api.depends('order_details.price_total')
    def amount_all_quotation(self):
        for order in self:
            final_amount = 0.0
            for line in order.order_details:
                final_amount += line.price_subtotal

            order.update({
                'amount': final_amount
            })

    @api.onchange('customer_id')
    def onchange_information_customer(self):
        if not self.customer_id:
            self.shipping_phone = False
            self.shipping_address = False
        else:
            self.shipping_phone = self.customer_id.phone
            self.shipping_address = self.customer_id.address
        self.update({
            'shipping_address': self.shipping_address,
            'shipping_phone': self.shipping_phone
        })

    def action_confirm(self):
        self.state = 'xác nhận'

    def action_cancel(self):
        self.state = 'hủy bỏ'

    def action_new(self):
        self.state = 'mới'

    def unlink(self):
        if self.state not in ('mới', 'hủy bỏ', 'hoàn thành'):
            raise UserError('Bạn không thể xóa một báo giá đã được xác nhận, hãy hủy bỏ trước khi xóa')
        return super(OrderModel, self).unlink()

    # @api.constrains('date_order')
    # def check_valid_date(self):
    #     if self.date_order.strftime('%Y-%m-%d') > datetime.today().strftime('%Y-%m-%d') or self.date_order.strftime(
    #             '%Y-%m-%d') < datetime.today().strftime('%Y-%m-%d'):
    #         raise ValidationError('Bạn không thể chọn một ngày nào khác không phải là ngày hôm nay!')


class OrderDetail(models.Model):
    _name = 'order.detail'
    _description = 'detail of order'

    name = fields.Text(string='Description', required=True)
    order_id = fields.Many2one('order.model', string='Order Reference', ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    price_unit = fields.Float('Unit Price', required=True, digits=(12, 0), default=0.0)
    price_subtotal = fields.Float(compute='compute_subtotal', string='Subtotal', store=True, digits=(12, 0))
    price_total = fields.Float(compute='compute_total', string='Total', store=True, digits=(12, 0))
    product_id = fields.Many2one('product.model', string='Product', ondelete='restrict', required=True)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', default=1.0)
    salesman_id = fields.Many2one(related='order_id.user_id', store=True, string='Salesperson', readonly=True)
    order_customer_id = fields.Many2one(related='order_id.customer_id', store=True, string='Customer', readonly=False)

    @api.depends('product_uom_qty', 'price_unit')
    def compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.product_uom_qty * line.price_unit

        line.update({
            'price_subtotal': line.price_subtotal
        })

    @api.depends('product_uom_qty', 'price_unit')
    def compute_total(self):
        for line in self:
            line.price_total = line.product_uom_qty * line.price_unit

        line.update({
            'price_total': line.price_total
        })
