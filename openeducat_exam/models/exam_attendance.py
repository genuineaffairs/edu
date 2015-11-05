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


class OpExamAttendance(models.Model):
    _name = 'op.exam.attendance'
    # _rec_name = 'student_id'

    exam_id = fields.Many2one('op.exam', 'Exam', required=True)
    exam_line_id = fields.Many2one('op.exam.line', 'Subject Exam', required=True)
    student_id = fields.Many2one('op.student', 'Student', required=True)
    present = fields.Selection([('p', 'Present'), ('a', 'Absent')], 'Attendance', default='p')
    obtained_mark = fields.Integer('Obtained Mark')
    min_mark = fields.Integer('Passing Mark', related='exam_line_id.min_mark')
    total_mark = fields.Integer('Passing Mark', related='exam_line_id.total_mark')


    # @api.multi
    # def unlink(self):
    #     raise ValidationError(_('You can not delete Exam Lines!'))

