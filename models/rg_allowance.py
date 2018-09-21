# coding=utf-8

from odoo import models, fields, api


class RgAllowance(models.Model):
    _name = 'rg.allowance'
    _description = u'补助'

    name = fields.Char('名称', required='1')
    create_date = fields.Datetime(string='日期')
    rg_allowance_fee_ids = fields.One2many('rg.allowance.fee', 'rg_allowance_id', '补助费用')
    project = fields.Char('项目')
    total = fields.Float(string='总计/￥', compute='_compute_total_amount')

    @api.depends('rg_allowance_fee_ids')
    def _compute_total_amount(self):
        for obj in self:
            total = 0
            for fee in obj.rg_allowance_fee_ids:
                total += fee.total
            obj.total = total


class RgAllowanceFee(models.Model):
    _name = 'rg.allowance.fee'
    _description = u'补助费用'

    rg_allowance_id = fields.Many2one('rg.allowance', string='补助')
    postgraduate_id = fields.Many2one('rg.partner', string='姓名', domain=[('identity_type', '=', 'postgraduate'),('is_candidate', '=', True)], required='1', )
    detail_ids = fields.One2many('rg.allowance.fee.detail', 'rg_allowance_fee_id',  string='明细')
    total = fields.Float(string='小计/￥', compute='_compute_total_amount')

    @api.depends('detail_ids')
    def _compute_total_amount(self):
        for obj in self:
            total = 0
            for fee in obj.detail_ids:
                total += fee.total
            obj.total = total


class RgAllowanceFeeDetail(models.Model):
    _name = 'rg.allowance.fee.detail'
    _description = u'费用明细'
    _order = 'amount, id'

    rg_allowance_fee_id = fields.Many2one('rg.allowance.fee', string='补助')
    name = fields.Char(string='名称', required='1')
    amount = fields.Float(string='金额/￥')
    qty = fields.Integer(string='数量', default=1)
    total = fields.Float(string='总计/￥')

    @api.onchange('qty', 'amount')
    def _onchange_total_amount(self):
        self.total = self.amount * self.qty