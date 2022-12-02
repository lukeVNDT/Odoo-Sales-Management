from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _, tools
import re


class CustomerModel(models.Model):
    _name = "customer.model"
    _description = "customer management model"

    name = fields.Char(string="name")
    address = fields.Text(string="address")
    email = fields.Char(string="email")
    phone = fields.Char(string="phone")
    avatar = fields.Image(string="avatar")

    @api.constrains('phone')
    def check_valid_phone(self):
        match = re.match("^(0|\\+84)(\\s|\\.)?((3[2-9])|(5[689])|(7[06-9])|(8[1-689])|(9[0-46-9]))(\\d)(\\s|\\.)?(\\d{3})(\\s|\\.)?(\\d{3})$", str(self.phone))
        if not match:
            raise ValidationError('Số điện thoại bạn nhập phải hợp lệ, vui lòng kiểm tra lại!')

    @api.constrains('email')
    def check_valid_email(self):
        match = re.match("^[A-Za-z0-9]+[A-Za-z0-9]*@[A-Za-z0-9]+(\\.[A-Za-z0-9]+)$", str(self.email))
        if not match:
            raise ValidationError('Định dạng email không hợp lệ, vui lòng kiểm tra lại!')



