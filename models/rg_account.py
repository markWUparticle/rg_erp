# coding=utf-8

from odoo import models, fields, api


class RgAccount(models.Model):
    _name = 'rg.account'
    _description = u'记账'
    _order = 'create_date, id'

    name = fields.Char(string='名称')
    res_partner_id = fields.Many2one('res.partner', string='所属',
                                      domain=[('identity_type', 'in', ['tutor'])])
    amount = fields.Float(string='余额/￥', compute='')
    detail_ids = fields.One2many('rg.account.detail', 'rg_account_id', string='明细')


class RgAccountDetail(models.Model):
    _name = 'rg.account.detail'
    _description = u'记账明细'

    create_date = fields.Datetime(string='日期')
    charge = fields.Float(string='收支/￥')
    desc = fields.Text(string='备注')
    rg_account_id = fields.Many2one('rg.account', '记账')
