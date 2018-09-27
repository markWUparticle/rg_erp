# coding=utf-8

from odoo import models, fields, api


class RgEvent(models.Model):
    _name = 'rg.event'
    _description = u'活动'

    name = fields.Char('名称', required='1')
    create_date = fields.Datetime(string='日期')
    address = fields.Char(string='地点')
    desc = fields.Text(string='详情')
    rg_event_fee_ids = fields.One2many('rg.event.fee', 'rg_event_id', '活动费用')
    tutor_ids = fields.Many2many('rg.partner', string='参与老师',
                                       domain=[('identity_type', '=', 'tutor'), ('is_candidate', '=', True)])
    postgraduate_ids = fields.Many2many('rg.partner', string='参加人员',
                                       domain=[('is_candidate', '=', True)], compute='_compute_postgraduate_of_join')
    total = fields.Float(string='总计/￥', compute='_compute_total_amount')
    postgraduate_nums = fields.Integer(string='参加人数', compute='_compute_postgraduate_of_join')
    rg_event_partner_ids = fields.One2many('rg.event.partner', 'rg_event_id', string='通知名单')
    # 活动经费从账户账户中出
    state = fields.Selection([('cancel', '取消'), ('draft', '草稿'), ('pending', '进行中'), ('done', '完成')],
                             default='draft', string='状态')


    @api.depends('rg_event_fee_ids')
    def _compute_total_amount(self):
        for obj in self:
            total = 0
            for fee in obj.rg_event_fee_ids:
                total += fee.total
            obj.total = total

    @api.depends('rg_event_partner_ids')
    def _compute_postgraduate_of_join(self):
        for obj in self:
            obj.postgraduate_ids = ()
            for event_partner in obj.rg_event_partner_ids.filtered(lambda i: i.state == 'join'):
                obj.postgraduate_ids += event_partner.postgraduate_id
            obj.postgraduate_nums = len(obj.postgraduate_ids)

    @api.multi
    def action_generate_partner_list(self):
        self.ensure_one()
        new_context = dict(self._context) or {}
        new_context.update({
            'default_model': 'rg.event',
            'default_method': 'generate_partner_list',
            'default_info': '选择需要通知的人员',
            'record_ids': self.id,
        })
        return {
            'name': u'名单',
            'type': 'ir.actions.act_window',
            'res_model': 'rg.confirm',
            'res_id': None,
            'view_id': self.env.ref('rg_erp.rg_confirm_view_form_385').id,
            'view_mode': 'form',
            'view_type': 'form',
            'context': new_context,
            'target': 'new'
        }

    @api.model
    def generate_partner_list(self, postgraduate_ids):
        for postgraduate in postgraduate_ids:
            self.env['rg.event.partner'].create({
                'postgraduate_id': postgraduate.id,
                'rg_event_id': self.id,
            })
        self.state = 'pending'

class RgEventPartner(models.Model):
    _name = 'rg.event.partner'
    _description = u'通知名单'
    _order = 'state,postgraduate_type desc,grade desc,tutor_id,gender'

    rg_event_id = fields.Many2one('rg.event', string='活动')
    postgraduate_id = fields.Many2one('rg.partner', string='姓名',
                                      domain=[('identity_type', '=', 'postgraduate'), ('is_candidate', '=', True)], required='1')
    postgraduate_type = fields.Selection([('master', '硕士'), ('doctorate', '博士'), ], related='postgraduate_id.postgraduate_type', string='类别', store=True)
    grade = fields.Char(string='年级', related='postgraduate_id.grade', store=True)
    mobile = fields.Char(string='手机', related='postgraduate_id.mobile', store=True)
    gender = fields.Selection([('male', '男'), ('female', '女'),], string='性别', related='postgraduate_id.gender', store=True)
    tutor_id = fields.Many2one('rg.partner', string='导师', domain=[('identity_type', '=', 'tutor')], related='postgraduate_id.tutor_id', store=True)
    state = fields.Selection([('wait', '待通知'), ('pending', '待回复'), ('join', '参加'), ('uncertain', '不确定'), ('reject', '不参加'), ],
                             default='wait', string='状态')


class RgEventFee(models.Model):
    _name = 'rg.event.fee'
    _description = u'活动费用'

    rg_event_id = fields.Many2one('rg.event', string='活动')
    name = fields.Char('名称', required='1')
    amount = fields.Float(string='单价/￥')
    qty = fields.Integer(string='数量', default=1)
    total = fields.Float(string='总计/￥')

    @api.onchange('qty', 'amount')
    def _onchange_total_amount(self):
        self.total = self.amount * self.qty