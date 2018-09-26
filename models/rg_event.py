# coding=utf-8

from odoo import models, fields, api


class RgEvent(models.Model):
    _name = 'rg.event'
    _description = u'活动'

    name = fields.Char('名称', required='1')
    create_date = fields.Datetime(string='日期')
    address = fields.Char(string='地点')
    desc = fields.Text(string='详情')
    rg_event_fee_ids = fields.One2many('rg.event.fee', 'rg_event_id', '活动费用')
    tutor_ids = fields.Many2many('rg.partner', string='参与老师',
                                       domain=[('identity_type', '=', 'tutor'), ('is_candidate', '=', True)])
    postgraduate_ids = fields.Many2many('rg.partner', string='参加人员',
                                       domain=[('is_candidate', '=', True)])
    total = fields.Float(string='总计/￥', compute='_compute_total_amount')
    postgraduate_nums = fields.Integer(string='参加人数', compute='_compute_postgraduate_nums')
    # 活动经费从账户账户中出
    state = fields.Selection([('cancel', '取消'), ('draft', '草稿'), ('pending', '进行中'), ('done', '完成')],
                             default='draft', string='状态')

    @api.depends('rg_event_fee_ids')
    def _compute_total_amount(self):
        for obj in self:
            total = 0
            for fee in obj.rg_event_fee_ids:
                total += fee.total
            obj.total = total

    @api.depends('postgraduate_ids')
    def _compute_postgraduate_nums(self):
        for obj in self:
            obj.postgraduate_nums = len(obj.postgraduate_ids)

# 添加通知人 及状态



class RgEventFee(models.Model):
    _name = 'rg.event.fee'
    _description = u'活动费用'

    rg_event_id = fields.Many2one('rg.event', string='活动')
    name = fields.Char('名称', required='1')
    amount = fields.Float(string='单价/￥')
    qty = fields.Integer(string='数量', default=1)
    total = fields.Float(string='总计/￥')

    @api.onchange('qty', 'amount')
    def _onchange_total_amount(self):
        self.total = self.amount * self.qty