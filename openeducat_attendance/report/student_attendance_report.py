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

import time

from openerp import models
from openerp.report import report_sxw


class StudentAttendanceGenerate(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(StudentAttendanceGenerate, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_student_name': self.get_student_name,
            'get_data': self.get_data
        })

    def get_student_name(self, data):
        student = self.pool.get('op.student').browse(
            self.cr, self.uid, data['student_id'])
        if student:
            return ' '.join([student.name,
                             student.middle_name,
                             student.last_name])

    def get_data(self, data):

        sheet_pool = self.pool.get('op.attendance.sheet')

        sheet_search = sheet_pool.search(
            self.cr, self.uid,
            [('attendance_date', '>=', data['from_date']),
             ('attendance_date', '<=', data['to_date'])],
            order='attendance_date asc')

        lst = []
        absent_count = 0
        for sheet in sheet_search:
            sheet_browse = sheet_pool.browse(self.cr, self.uid, sheet)
            for line in sheet_browse.attendance_line_ids:
                if data['student_id'] == line.student_id.id:
                    dic = {
                        'date': sheet_browse.attendance_date,
                        'present': 'P' if line.present else 'A',
                        'remark': line.remark
                    }
                    if not line.present:
                        absent_count += 1
                    lst.append(dic)
        total = len(lst)
        return [{
            'total': total,
            'total_present': total - absent_count,
            'total_absent': absent_count,
            'line': lst,
         }]


class StudentAttendanceReport(models.AbstractModel):
    _name = 'report.openeducat_attendance.student_attendance_report'
    _inherit = 'report.abstract_report'
    _template = 'openeducat_attendance.student_attendance_report'
    _wrapped_report_class = StudentAttendanceGenerate

