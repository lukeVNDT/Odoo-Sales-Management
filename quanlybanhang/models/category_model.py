from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _, tools


class CategoryModel(models.Model):
    _name = "category.model"
    _description = "category management model"

    name = fields.Char(string="name")
    description = fields.Text(string="description")





