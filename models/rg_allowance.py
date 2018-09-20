# coding=utf-8

from odoo import models, fields, api


class RgAllowance(models.Model):
    _name = 'rg.allowance'
    _description = u'补助'

    name = fields.Char('名称')
    create_date = fields.Datetime(string='日期')
    rg_allowance_fee_ids = fields.One2many('rg.allowance.fee', 'rg_allowance_id', '补助费用')
    project = fields.Char('项目')
    total = fields.Float(string='总计/￥')


class RgAllowanceFee(models.Model):
    _name = 'rg.allowance.fee'
    _description = u'补助费用'

    rg_allowance_id = fields.Many2one('rg.allowance', string='补助')
    postgraduate_id = fields.Many2one('res.partner', string='姓名', domain=[('identity_type', 'in', ['master', 'doctorate'])])
    detail_ids = fields.One2many('rg.allowance.fee.detail', 'rg_allowance_fee_id', string='明细')
    total = fields.Float(string='小计/￥')


class RgAllowanceFeeDetail(models.Model):
    _name = 'rg.allowance.fee.detail'
    _description = u'费用明细'

    name = fields.Char('名称')
    amount = fields.Float(string='金额/￥')
    rg_allowance_fee_id = fields.Many2one('rg.allowance.fee', '补助费用')
