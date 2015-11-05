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


class OpAttendanceLine(models.Model):
    _name = 'op.attendance.line'
    _rec_name = 'attendance_date'
    _order = 'attendance_date'

    register_id = fields.Many2one('op.attendance.register', 'Attendance Register', required=True)
    att_sheet_id = fields.Many2one('op.attendance.sheet', 'Attendance Sheet', required=True)
    student_id = fields.Many2one('op.student', 'Student', required=True)
    present = fields.Boolean('Present ?')
    attendance_date = fields.Date('Date', related='att_sheet_id.attendance_date', store=True,
        readonly=True)
    course_id = fields.Many2one(string='Course', related='att_sheet_id.course_id',
        store=True, readonly=True)
    batch_id = fields.Many2one(string='Batch', related='att_sheet_id.batch_id',
        store=True, readonly=True)
    remark = fields.Char('Remark')


    _sql_constraints = [
        ('attendance_uniq', 'unique (att_sheet_id, student_id)',
            "You can't enter duplicate entry of student!"),
    ]