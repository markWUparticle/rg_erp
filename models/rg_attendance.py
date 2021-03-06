# coding=utf-8

from odoo import models, fields, api


class RgAttendance(models.Model):
    _name = 'rg.attendance'
    _description = u'出勤'

    name = fields.Char('名称', required='1')
    start_date = fields.Date(string='开始日期')
    end_date = fields.Date(string='结束日期')
    total_times = fields.Integer(string='总出勤数')
    postgraduate_ids  = fields.Many2many('rg.partner', string='全勤',
                                         domain=[('identity_type', '=', 'postgraduate'), ('is_candidate', '=', True)],
                                         compute='')
    detail_ids = fields.One2many('rg.attendance.detail', 'rg_attendance_id', string='明细')
    #全勤补助
    rg_allowance_id = fields.Many2one('rg.allowance', string='补助单')


class RgAttendanceDetail(models.Model):
    _name = 'rg.attendance.detail'
    _description = u'出勤明细'

    rg_attendance_id = fields.Many2one('rg.attendance', string='出勤')
    postgraduate_id = fields.Many2one('rg.partner', string='姓名',
                                      domain=[('identity_type', '=', 'postgraduate'), ('is_candidate', '=', True)], required='1')
    times_of_normal = fields.Integer(string='正常')
    times_of_late = fields.Integer(string='迟到')
    times_of_leave = fields.Integer(string='请假')