from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _, tools


class ProductModel(models.Model):
    _name = "product.model"
    _description = "product management model"

    name = fields.Char(string="product name")
    description = fields.Text(string="description")
    category_id = fields.Many2one('category.model', ondelete="cascade")
    order_id = fields.Many2one('order.model')
    price = fields.Float(string="price", digits=(12, 0))
    purchase_price = fields.Float(string="purchase price", digits=(12, 0))
    product_image = fields.Image(string="product image")

    @api.constrains('price')
    def check_negative_number(self):
        if self.price < 0:
            raise ValidationError('Giá nhập vào phải là số dương')

    @api.constrains('purchase_price')
    def check_negative_number_purchase_price(self):
        if self.purchase_price < 0:
            raise ValidationError('Giá nhập vào phải là số dương')

    @api.constrains('category_id')
    def check_default_category(self):
        if not self.category_id:
            raise ValidationError('Sản phẩm mặc định cần thuộc một nhóm sản phẩm')


class CategoryModel(models.Model):
    _inherit = "category.model"
    list_product = fields.One2many('product.model', 'category_id', string='Product List')

