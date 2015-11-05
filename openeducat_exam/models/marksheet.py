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

class OpMarksheet(models.Model):
    _name = 'op.marksheet'
    _rec_name = 'student_id'

    marksheet_register_id = fields.Many2one('op.marksheet.register', 'Marksheet Register',
        select=True)
    exam_id = fields.Many2one('op.exam', 'Exam', related='marksheet_register_id.exam_id',
        store=True, select=True)
    batch_id = fields.Many2one('op.batch', 'Batch', related='marksheet_register_id.batch_id',
        store=True, select=True)
    course_id = fields.Many2one('op.course', 'Course', related='marksheet_register_id.course_id',
        store=True, select=True)
    marksheet_line_ids = fields.One2many('op.marksheet.line', 'marksheet_id', 'Results',
        ondelete='cascade')
    # declare_date = fields.Datetime('Declare Date', related='marksheet_register_id.declare_date')
    student_id = fields.Many2one('op.student', 'Student', select=True)
    total_marks = fields.Integer('Total Marks')
    obtained_total_marks = fields.Integer('Obtained Marks')
    percentage = fields.Float('Percentage')
    result = fields.Selection(RESULT, 'Result', default='pass')
    display_result = fields.Char('Result to Display')

