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

from openerp import models, fields


class OpTimetableDay(models.Model):
    _name = 'op.timetable.day'
    _order = 'sequence'

    name = fields.Char()
    sequence = fields.Integer()


class OpTimetable(models.Model):
    _name = 'op.timetable'
    _description = 'Time Table'
    _rec_name = 'course_code'
    # _order = 'type, period_id'

    # period_id = fields.Many2one('op.period', 'Period', required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True, select=True)
    course_code = fields.Char('Course', related='course_id.code', store="True")
    batch_id = fields.Many2one('op.batch', 'Batch', required=True, select=True)
    faculty_id = fields.Many2one('op.faculty', 'Class Teacher', select=True)
    # subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    color = fields.Integer('Color Index')
    # type = fields.Selection(
    #     [('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
    #      ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
    #      ('Friday', 'Friday'), ('Saturday', 'Saturday')], 'Days')
    # type = fields.Many2one('op.timetable.day', 'Days')

    time_table_lines = fields.One2many(
        'op.timetable.line', 'timetable_id', 'Time Table Lines')
    time_table_lines_1 = fields.One2many(
        'op.timetable.line', 'timetable_id', 'Time Table Lines',
        domain=[('day', '=', '1')])
    time_table_lines_2 = fields.One2many(
        'op.timetable.line', 'timetable_id', 'Time Table Lines',
        domain=[('day', '=', '2')])
    time_table_lines_3 = fields.One2many(
        'op.timetable.line', 'timetable_id', 'Time Table Lines',
        domain=[('day', '=', '3')])
    time_table_lines_4 = fields.One2many(
        'op.timetable.line', 'timetable_id', 'Time Table Lines',
        domain=[('day', '=', '4')])
    time_table_lines_5 = fields.One2many(
        'op.timetable.line', 'timetable_id', 'Time Table Lines',
        domain=[('day', '=', '5')])
    time_table_lines_6 = fields.One2many(
        'op.timetable.line', 'timetable_id', 'Time Table Lines',
        domain=[('day', '=', '6')])
    time_table_lines_7 = fields.One2many(
        'op.timetable.line', 'timetable_id', 'Time Table Lines',
        domain=[('day', '=', '7')])



class OpTimetableLine(models.Model):
    _name = 'op.timetable.line'
    _description = 'Time Table Lines'
    _rec_name = 'period_id'
    _order = 'period_id'

    timetable_id = fields.Many2one('op.timetable', 'Time Table',
        required=True, select=True)
    course_id = fields.Many2one(related='timetable_id.course_id', string='Course', store=True)
    batch_id = fields.Many2one(related='timetable_id.batch_id', string='Batch', store=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True, select=True)
    subject_id = fields.Many2one('op.subject', 'Subject', required=True, select=True)
    color = fields.Integer('Color Index')
    day = fields.Selection([
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    ], 'Day', required=True, select=True)
    period_id = fields.Many2one('op.period', 'Period',  required=True, select=True)

