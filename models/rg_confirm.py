# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RgConfirm(models.TransientModel):
    _name = 'rg.confirm'
    _description = u'确认'

    info = fields.Text("信息")
    model = fields.Char('模型')
    method = fields.Char('方法')

    # onchange
    postgraduate_ids = fields.Many2many('rg.partner', string='学生',
                                      domain=[('is_candidate', '=', True)])
    rg_allowance_type_id = fields.Many2one('rg.allowance.type', string='费用类型')
    rg_attendance_id = fields.Many2one('rg.attendance', string='考勤记录')
    rg_vacation_id = fields.Many2one('rg.vacation', string='假期记录')

    @api.onchange('rg_allowance_type_id', 'rg_attendance_id')
    def _onchange_postgraduate_ids(self):
        self.postgraduate_ids = ()
        if self.rg_allowance_type_id.name in ['生活补助', '路费补助'] :
            self.postgraduate_ids = self.env['rg.partner'].search([('identity_type', '=', 'postgraduate'),
                                                                   ('is_candidate', '=', 'True'),]).filtered(lambda i: i.tutor_id.name != '殷素红')
        if self.rg_allowance_type_id.name == '全勤奖':
            self.postgraduate_ids = self.rg_attendance_id.postgraduate_ids


    @api.multi
    def execute(self):
        self.ensure_one()
        active_ids = self._context.get('record_ids')
        rs = self.env[self.model].browse(active_ids)
        ret = getattr(rs, self.method)()
        return ret

    @api.multi
    def execute_with_partner(self):
        self.ensure_one()
        active_ids = self._context.get('record_ids')
        rs = self.env[self.model].browse(active_ids)
        ret = getattr(rs, self.method)(self.postgraduate_ids)
        return ret

