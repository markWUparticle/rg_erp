
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RgPartner(models.Model):
    _name = 'rg.partner'
    _description = u'成员'
    _order = 'is_candidate desc,title desc,postgraduate_type desc,grade desc,tutor_id,id'

    sequence = fields.Integer('顺序')
    gender = fields.Selection([('male', '男'), ('female', '女'),], string='性别')
    debit_card_no = fields.Char(string='银行卡号')
    postgraduate_type = fields.Selection([('postgraduate', '硕士'), ('doctorate', '博士'),], string='类别')
    identity_type = fields.Selection([('tutor', '导师'), ('postgraduate', '研究生'),], string='类型')
    id_card = fields.Char(string='身份证号码')
    grade = fields.Char(string='年级',)
    is_candidate = fields.Boolean(string='在读')
    native_place = fields.Char(string='籍贯')
    student_id = fields.Char(string='学号')
    tutor_id = fields.Many2one('rg.partner', string='导师', domain=[('identity_type', '=', 'tutor')])
    phone = fields.Char(string='电话')
    mobile = fields.Char(string='手机')
    email = fields.Char('电子邮件')
    name = fields.Char(index=True, string='姓名', required=1)
    title = fields.Many2one('res.partner.title', string='谓称')

    @api.multi
    def change_candidate_state(self):
        for obj in self:
            obj.is_candidate = not obj.is_candidate
