
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RgVacation(models.Model):
    _name = 'rg.vacation'
    _description = u'假期'

    create_date = fields.Datetime(string='日期')
    name = fields.Char(string='名称')
    rg_vacation_record_ids = fields.One2many('rg.vacation.record', 'rg_vacation_id', string='时间记录')


class RgVacationRecord(models.Model):
    _name = 'rg.vacation.record'
    _description = u'记录'

    rg_vacation_id = fields.Many2one('rg.vacation', string='假期')
    postgraduate_id = fields.Many2one('res.partner', string='姓名',
                                      domain=[('identity_type', 'in', ['master', 'doctorate'])])
    departure_date = fields.Date(string='离校日期')
    return_date = fields.Date(string='返校日期')