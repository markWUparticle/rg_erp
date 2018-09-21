
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RgPartner(models.Model):
    _name = 'rg.partner'
    _order = 'id'

    debit_card_no = fields.Char(string='银行卡号')
    postgraduate_type = fields.Selection([('postgraduate', '硕士'), ('doctorate', '博士'),], string='类别')
    identity_type = fields.Selection([('tutor', '导师'), ('postgraduate', '研究生'),], string='类型')
    id_card = fields.Char(string='身份证号码')
    grade = fields.Char(string='年级', default='2018')
    is_candidate = fields.Boolean(string='在读')
    native_place = fields.Char(string='籍贯')
    student_id = fields.Char(string='学号')
    tutor_id = fields.Many2one('rg.partner', string='导师', domain=[('identity_type', '=', 'tutor')])
    phone = fields.Char(string='手机')
    mobile = fields.Char(string='电话')
    email = fields.Char('电子邮件')
    name = fields.Char(index=True, string='姓名', required=1)
    title = fields.Many2one('res.partner.title', string='谓称')

# [('identity_type', '=', 'postgraduate'), ('is_candidate', '=', 'True')]

