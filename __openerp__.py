# -*- coding: utf-8 -*-

{
    'name': 'rg_erp',
    'version': '1.0.0',
    'category': '',
    'summary': 'Research Group ERP',
    'author': 'MARK',
    'website': '',
    'application': True,
    'auto_data_include': [],
    'data': [
        'views/parent_menus.xml',
        'views/rg_account_views.xml',
        'views/res_partner_views.xml',
        'views/rg_allowance_views.xml',
        'views/rg_event_views.xml',
        'views/rg_allowance_fee_detail_views.xml',
    ],
    'qweb': [
    ],
    'depends' : ['mail'],
    'installable': True,
    'active': False,
    'web': True,
}
