# coding=utf-8

from odoo import models, fields, api


class RgMeeting(models.Model):
    _name = 'rg.meeting'
    _description = u'会议'

    name = fields.Char('名称', required='1')
    create_date = fields.Datetime(string='日期')
    tutor_ids = fields.Many2many('rg.partner', string='出席老师',
                                    domain=[('identity_type', '=', 'tutor'),])
    expect_attend_num = fields.Integer(string='预计学生人数')
    actual_attend_num = fields.Integer(string='实到学生人数')
    detail_ids = fields.One2many('rg.meeting.detail', 'rg_meeting_id', string='明细')
    desc = fields.Text(string='详情')


class RgMeetingDetail(models.Model):
    _name = 'rg.meeting.detail'
    _description = u'会议人员明细'

    rg_meeting_id = fields.Many2one('rg.meeting', string='会议')
    absentee_id = fields.Many2one('rg.partner', string='学生',
                                    domain=[('identity_type', '=', 'postgraduate'), ('is_candidate', '=', True)])
    state = fields.Selection([('signed ', '已签到'), ('ask_for_leave', '请假'), ('absence', '缺勤')], string='状态')
