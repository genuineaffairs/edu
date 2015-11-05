# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class OpExamType(models.Model):
    _name = 'op.exam.type'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code')


class OpExam(models.Model):
    _name = 'op.exam'
    _inherit = 'mail.thread'
    _description = 'Exam'

    name = fields.Char('Exam', required=True, track_visibility='onchange')
    code = fields.Char('Code')
    start_date = fields.Date('Start Date', required=True, track_visibility='onchange')
    end_date = fields.Date('End Date', required=True, track_visibility='onchange')
    course_id = fields.Many2one('op.course', 'Course', required=True, track_visibility='onchange')
    batch_id = fields.Many2one('op.batch', 'Batch', required=True, track_visibility='onchange')
    student_ids = fields.One2many(related='batch_id.student_ids', string='Students')
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('GPA', 'GPA'), ('CWA', 'CWA'), ('CCE', 'CCE')],
        'Evaluation Type', required=True)
    state = fields.Selection(
        [('new', 'New'), ('confirm', 'Confirm'), ('start', 'Start'), ('done', 'Done'),
         ('cancel', 'Cancelled')], 'State', select=True,
        readonly=True, default='new', track_visibility='onchange')
    exam_type = fields.Many2one('op.exam.type', 'Exam Type')
    exam_line_ids = fields.One2many('op.exam.line', 'exam_id', 'Exam Lines', ondelete='cascade')
    venue = fields.Many2one('res.partner', 'Venue')
    print_result = fields.Boolean()
    note = fields.Text('Note')


    @api.constrains('start_date', 'end_date')
    def _check_date_time(self):
        if self.start_date > self.end_date:
            raise ValidationError(_('Start Date should be greater than End Date!'))

    @api.onchange('course_id')
    def onchange_course_id(self):
        self.batch_id = False


    @api.multi
    def act_confirm(self):
        for record in self:
            record.state = 'confirm'

    @api.multi
    def act_start(self):
        for record in self:
            record.state = 'start'

    @api.multi
    def act_done(self):
        for record in self:
            record.state = 'done'

    @api.multi
    def act_cancel(self):
        for record in self:
            record.state = 'cancel'

    @api.multi
    def act_new(self):
        for record in self:
            record.state = 'new'


class OpExamLine(models.Model):
    _name = 'op.exam.line'
    _inherit = 'mail.thread'
    _description = 'Subject Exam'
    _order = 'sequence, start_time'

    exam_id = fields.Many2one('op.exam', 'Exam', required=True, select=True)
    course_id = fields.Many2one(string='Course', related='exam_id.course_id', store=True, select=True)
    batch_id = fields.Many2one(string='Batch', related='exam_id.batch_id', store=True, select=True)
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    student_ids = fields.One2many('op.exam.attendance', 'exam_line_id', 'Students')
    start_time = fields.Datetime('Start Time', required=True)
    end_time = fields.Datetime('End Time', required=True)
    state = fields.Selection(
        [('new', 'New'), ('start', 'Start'), ('done', 'Done'),
         ('cancel', 'Cancelled')], 'State', select=True,
        readonly=True, default='new', track_visibility='onchange')
    instructor_id = fields.Many2one('op.faculty', string='Instructor')
    total_mark = fields.Integer('Total Marks', required=True)
    min_mark = fields.Integer('Passing Marks', required=True)
    sequence = fields.Integer(default=20)
    note = fields.Text('Note')


    @api.multi
    def name_get(self):
        result = []
        name = ''
        for exam_line in self:
            if exam_line.exam_id.code:
                name = exam_line.exam_id.code + ' - '
            name += exam_line.subject_id.code
            result.append((exam_line.id, name))
        return result

    @api.constrains('total_mark', 'min_mark')
    def _check_marks(self):
        if self.total_mark < 0 or self.min_mark < 0:
            raise ValidationError(_('Mark shoul be positive !'))

    @api.constrains('start_time', 'end_time')
    def _check_date_time(self):
        if self.start_time > self.end_time:
            raise ValidationError(_('Start Time should be greater than End Time!'))


    @api.model
    def create(self, vals):
        OpExamAttendance = self.env['op.exam.attendance']
        examline = super(OpExamLine, self).create(vals)
        students = self.env['op.student'].search([('course_id', '=', examline.course_id.id),
            ('batch_id', '=', examline.batch_id.id)])
        for stud in students:
            OpExamAttendance.create({
                'exam_id': examline.exam_id.id,
                'exam_line_id': examline.id,
                'student_id': stud.id
            })
        return examline

    @api.multi
    def act_start(self):
        for record in self:
            record.state = 'start'

    @api.multi
    def act_done(self):
        for record in self:
            record.state = 'done'

    @api.multi
    def act_cancel(self):
        for record in self:
            record.state = 'cancel'

    @api.multi
    def act_new(self):
        for record in self:
            record.state = 'new'
