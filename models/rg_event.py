# coding=utf-8

from odoo import models, fields, api


class RgEvent(models.Model):
    _name = 'rg.event'
    _description = u'活动'

    name = fields.Char('名称', required='1')
    create_date = fields.Datetime(string='日期')
    rg_event_fee_ids = fields.One2many('rg.event.fee', 'rg_event_id', '活动费用')
    tutor_ids = fields.Many2many('rg.partner', string='参与老师',
                                       domain=[('identity_type', '=', 'tutor'),])
    postgraduate_ids = fields.Many2many('rg.partner', string='参加人员',
                                       domain=[('identity_type', '=', 'postgraduate'), ('is_candidate', '=', True)])
    total = fields.Float(string='总计/￥')


class RgEventFee(models.Model):
    _name = 'rg.event.fee'
    _description = u'活动费用'

    rg_event_id = fields.Many2one('rg.event', string='活动')
    name = fields.Char('名称', required='1')
    amount = fields.Float(string='金额/￥')
