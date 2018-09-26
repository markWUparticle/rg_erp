# coding=utf-8

from odoo import models, fields, api


class RgAllowance(models.Model):
    _name = 'rg.allowance'
    _description = u'补助'

    name = fields.Char('名称', required='1')
    create_date = fields.Datetime(string='日期')
    detail_ids = fields.One2many('rg.allowance.detail', 'rg_allowance_id',  string='补助费用')
    total = fields.Float(string='总计/￥', compute='_compute_total_amount')
    state = fields.Selection([('cancel', '取消'), ('draft', '草稿'), ('pending', '待确认'), ('done', '已确认')],
                             default='draft', string='状态')

    @api.depends('detail_ids')
    def _compute_total_amount(self):
        for obj in self:
            total = 0
            for fee in obj.detail_ids:
                total += fee.total
            obj.total = total

    @api.multi
    def action_generate_postgraduate(self):
        self.ensure_one()
        new_context = dict(self._context) or {}
        new_context.update({
            'default_model': 'rg.allowance',
            'default_method': 'generate_postgraduate',
            'default_info': '请选择需添加成员的条件\n相同字段最多一个条件',
            'record_ids': self.id,
            # 'default_parm_ids': self.env['rg.confirm.parm'].search([('is_default', 'in', True)]).ids
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
    def generate_postgraduate(self, parms):
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

    @api.multi
    def action_generate_fee(self):
        self.ensure_one()
        new_context = dict(self._context) or {}
        new_context.update({
            'default_model': 'rg.allowance',
            'default_method': 'generate_fee',
            'default_info': '请选择补助类型',
            'record_ids': self.id,
        })
        return {
            'name': u'添加补助费用',
            'type': 'ir.actions.act_window',
            'res_model': 'rg.confirm',
            'res_id': None,
            'view_mode': 'form',
            'view_type': 'form',
            'context': new_context,
            'target': 'new'
        }

    @api.model
    def generate_fee(self):
        pass

class RgAllowanceDetail(models.Model):
    _name = 'rg.allowance.detail'
    _description = u'补助明细'

    rg_allowance_id = fields.Many2one('rg.allowance', string='补助')
    postgraduate_id = fields.Many2one('rg.partner', string='姓名',
                                      domain=[('identity_type', '=', 'postgraduate'), ('is_candidate', '=', True)],
                                      required='1', )
    postgraduate_type = fields.Selection([('master', '硕士'), ('doctorate', '博士'), ], related='postgraduate_id.postgraduate_type', string='类别')
    grade = fields.Char(string='年级', related='postgraduate_id.grade',)
    tutor_id = fields.Many2one('rg.partner', string='导师', domain=[('identity_type', '=', 'tutor')], related='postgraduate_id.tutor_id',)
    project = fields.Char('项目')

    total = fields.Float(string='小计/￥', compute='')
    #
    # @api.depends('detail_ids')
    # def _compute_total_amount(self):
    #     for obj in self:
    #         total = 0
    #         for fee in obj.detail_ids:
    #             total += fee.total
    #         obj.total = total


class RgAllowanceFee(models.Model):
    _name = 'rg.allowance.fee'
    _description = u'补助费用'
    _order = 'amount, id'

    name = fields.Char(string='名称', required='1')
    level = fields.Integer(string='等级', default=1, help='保持唯一，等级越大金额越多')
    amount = fields.Float(string='金额/￥')
    qty = fields.Integer(string='数量', default=1)
    total = fields.Float(string='总计/￥')
    type_id = fields.Many2one('rg.allowance.type', string='类型', required='1')

    @api.onchange('qty', 'amount')
    def _onchange_total_amount(self):
        self.total = self.amount * self.qty


class RgAllowanceType(models.Model):
    _name = 'rg.allowance.type'
    _description = u'补助类型'
    _order = 'id'

    name = fields.Char(string='名称', required='1')
    rg_allowance_fee_ids = fields.One2many('rg.allowance.fee', 'type_id', string='补助费用')

