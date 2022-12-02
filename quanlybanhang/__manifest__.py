# -*- coding: utf-8 -*-
{
    'name': "Quản lý bán hàng",
    'summary': """Module quản lý bán hàng""",
    'description': """Quản lý bán hàng bao gồm quản lý sản phẩm, nhóm sản phẩm, đơn hàng, khách hàng, báo giá.""",
    'author': "Văn Nguyễn Duy Tân",
    'website': "https://bffblog.herokuapp.com/",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base',
        'product',
        'sale',
    ],
    'data': [
        'views/product_view.xml',
        'security/ir.model.access.csv',
    ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}