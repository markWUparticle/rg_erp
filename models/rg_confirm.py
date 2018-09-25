# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RgConfirm(models.TransientModel):
    _name = 'rg.confirm'
    _description = u'确认'

    info = fields.Text("信息")
    model = fields.Char('模型')
    method = fields.Char('方法')
    parm_ids = fields.Many2many('rg.confirm.parm', string='参数')
    allowance_fee_ids = fields.Many2many('rg.allowance.fee.detail', string='补助费用')

    @api.multi
    def execute(self):
        self.ensure_one()
        active_ids = self._context.get('record_ids')
        rs = self.env[self.model].browse(active_ids)
        ret = getattr(rs, self.method)()
        return ret

    @api.multi
    def execute_with_parm(self):
        self.ensure_one()
        active_ids = self._context.get('record_ids')
        rs = self.env[self.model].browse(active_ids)
        ret = getattr(rs, self.method)(self.parm_ids)
        return ret


class RgConfirmParm(models.TransientModel):
    _name = 'rg.confirm.parm'
    _description = u'参数'

    name = fields.Char('名字')
    element = fields.Char('条件表达式')
    is_default = fields.Boolean('默认')