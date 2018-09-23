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

    @api.multi
    def action_write_postgraduate(self):
        self.ensure_one()
        new_context = dict(self._context) or {}
        new_context.update({
            'default_model': 'rg.allowance',
            'default_method': 'write_postgraduate',
            'default_info': '请选择需添加成员的条件\n相同字段最多一个条件',
            'record_ids': self.id,
            'default_parm_ids': self.env['rg.confirm.parm'].search([('is_default', 'in', True)]).ids
        })
        return {
            'name': u'添加成员',
            'type': 'ir.actions.act_window',
            'res_model': 'rg.confirm',
            'res_id': None,
            'view_mode': 'form',
            'view_type': 'form',
            'context': new_context,
            'target': 'new'
        }

    @api.model
    def write_postgraduate(self, parms):
        domain = []
        for parm in parms:
            element = parm.element.split(',')
            if 'tutor_id' in element:
                element[2] = self.env['rg.partner'].search([('name', '=', element[2])], limit=1).id
            domain.append(tuple(element))
        partner_ids = self.env['rg.partner'].search(domain)
        for partner in partner_ids:
            vals = {
                'postgraduate_id': partner.id,
                'rg_allowance_id': self.id,
            }
            self.env['rg.allowance.fee'].create(vals)


class RgAllowanceFee(models.Model):
    _name = 'rg.allowance.fee'
    _description = u'补助费用'

    rg_allowance_id = fields.Many2one('rg.allowance', string='补助')
    postgraduate_id = fields.Many2one('rg.partner', string='姓名',
                                      domain=[('identity_type', '=', 'postgraduate'), ('is_candidate', '=', True)],
                                      required='1', )
    postgraduate_type = fields.Selection([('master', '硕士'), ('doctorate', '博士'), ], related='postgraduate_id.postgraduate_type', string='类别')
    grade = fields.Char(string='年级', related='postgraduate_id.grade',)
    tutor_id = fields.Many2one('rg.partner', string='导师', domain=[('identity_type', '=', 'tutor')], related='postgraduate_id.tutor_id',)

    detail_ids = fields.Many2many('rg.allowance.fee.detail',  string='明细')
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

    name = fields.Char(string='名称', required='1')
    amount = fields.Float(string='金额/￥')
    qty = fields.Integer(string='数量', default=1)
    total = fields.Float(string='总计/￥')

    @api.onchange('qty', 'amount')
    def _onchange_total_amount(self):
        self.total = self.amount * self.qty