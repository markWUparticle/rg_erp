
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _name = 'res.partner'
    _order = 'id'
    _inherit = 'res.partner'

    bank_id = fields.Many2one('res.partner.bank', string='银行')
    identity_type = fields.Selection([('tutor', '老师'), ('master', '硕士'), ('doctorate', '博士'),], string='类别')
    id_card = fields.Char(string='身份证号码')
    grade = fields.Char(string='年级', default='2018')
    is_candidate = fields.Boolean(string='在读')
    native_place = fields.Char(string='籍贯')
    tutor_id = fields.Many2one('res.partner', string='导师', domain=[('type', '=', 'tutor')])



