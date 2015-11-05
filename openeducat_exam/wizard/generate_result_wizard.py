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

from openerp import api, models, fields


class GenerateResult(models.TransientModel):

    """ Student Hall Ticket Wizard """
    _name = 'op.generate.result'


    exam_id = fields.Many2one('op.exam', 'Exam', required=True)
    name = fields.Char('Result Name', required=True,)
        # default=lambda self: 'Marksheet for %s Exam' % self.exam_id.name)
    declare_date = fields.Datetime('Declare Date', required=True,
        default=fields.Datetime.now())
    generated_by = fields.Many2one('res.users', 'Generated By')
    result_template_id = fields.Many2one('op.result.rule.template', 'Result Template')


    @api.onchange('exam_id')
    def onchange_exam_id(self):
        self.name = 'Marksheet Register %s' % self.exam_id.name

    @api.multi
    def generate_result(self, data):
        MarksheetRegister = self.env['op.marksheet.register']
        Marksheet = self.env['op.marksheet']
        MarksheetLine = self.env['op.marksheet.line']
        ExamLine = self.env['op.exam.line']
        AttendanceLine = self.env['op.exam.attendance']

        # Generate Marksheet Register
        vals = {
            'name': self.name,
            'exam_id': self.exam_id.id,
            'declare_date': self.declare_date,
            'generated_by': self.generated_by.id
        }
        ms_register = MarksheetRegister.create(vals)

        # Find exam lines for all the students
        exam_lines = ExamLine.search([('exam_id', '=', self.exam_id.id)])

        # Find attendance lines it is also the exam lines
        attendance_lines = AttendanceLine.search([('exam_id', '=', self.exam_id.id)])

        # Generate Marksheet per student
        for student in self.exam_id.student_ids:
            student_attendance_lines = attendance_lines.filtered(lambda r: r.student_id.id == student.id)
            total_obtained = sum(student_attendance_lines.mapped('obtained_mark'))
            total_marks =  sum(student_attendance_lines.mapped('total_mark'))
            percentage = (100 * total_obtained) / float(total_marks)


            # Generate Marksheet
            vals = {
                'marksheet_register_id': ms_register.id,
                'student_id': student.id,
                'obtained_total_marks': total_obtained,
                'total_marks': total_marks,
                'percentage': percentage,
            }
            marksheet = Marksheet.create(vals)

            # Generate marksheet lines
            for line in student_attendance_lines:
                vals = {
                    'marksheet_id': marksheet.id,
                    'attendance_id': line.id,
                    'obtained_mark': line.obtained_mark,
                    'result': 'fail' if line.min_mark > line.obtained_mark else 'pass',
                }
                MarksheetLine.create(vals)

            # write marksheet result 'pass/fail' and make percentage 0.0
            if 'fail' in marksheet.marksheet_line_ids.mapped('result'):
                marksheet.write({'percentage': 0.0, 'result': 'fail'})

            display_result = ''
            per_sort = sorted(self.result_template_id.pass_status_ids, key=lambda r: r.min_percentage)
            for s in per_sort:
                if marksheet.percentage >= s.min_percentage:
                    display_result = s.display_result
            marksheet.display_result = display_result


        # Total pass and fail in result register
        total_marksheet = len(ms_register.marksheet_ids)
        total_fail_marksheet = len(ms_register.marksheet_ids.filtered(lambda r: r.percentage <= 0.0))
        total_pass_marksheet = total_marksheet - total_fail_marksheet
        ms_register.write({
            'total_passed': total_pass_marksheet,
            'total_failed': total_fail_marksheet,
            })
        return True


    # def check_pass_fail_status(self,)
