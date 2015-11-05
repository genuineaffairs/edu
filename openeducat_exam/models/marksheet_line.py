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


RESULT = [('pass', 'PASS'), ('fail', 'FAIL')]

class OpMarksheetLine(models.Model):
    _name = 'op.marksheet.line'
    # _rec_name = 'student_id'

    marksheet_id = fields.Many2one('op.marksheet', 'Marksheet',
        select=True)
    marksheet_register_id = fields.Many2one('op.marksheet.register', 'Register',
        related='marksheet_id.marksheet_register_id')
    exam_id = fields.Many2one('op.exam', 'Exam', related='marksheet_id.exam_id')
    attendance_id = fields.Many2one('op.exam.attendance', 'Attendee')
    exam_line_id = fields.Many2one('op.exam.line', 'Exam Line', store=True,
        related='attendance_id.exam_line_id', select=True)
    subject_id = fields.Many2one('op.subject', 'Subject', select=True,
        related='attendance_id.exam_line_id.subject_id', store=True)
    total_mark = fields.Integer('Total Mark', related='attendance_id.total_mark')
    passing_mark = fields.Integer('Passing Mark', related='attendance_id.min_mark')
    obtained_mark = fields.Integer('Obtained Mark')
    result = fields.Selection(RESULT, 'Result')
