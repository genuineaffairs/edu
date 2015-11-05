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

from openerp import models, fields, api


class OpAttendanceSheet(models.Model):
    _name = 'op.attendance.sheet'
    _rec_name = 'attendance_date'

    @api.multi
    @api.depends('attendance_line_ids.present')
    def _total_present_absent(self):
        for record in self:
            record.total_present = len(record.attendance_line_ids.filtered(
                lambda rec: rec.present))
            record.total_absent = len(record.attendance_line_ids.filtered(
                lambda rec: rec.present is False))
            record.total = record.total_present + record.total_absent


    # name = fields.Char('Name')
    register_id = fields.Many2one('op.attendance.register', 'Register', required=True)
    attendance_date = fields.Date('Date', required=True, default=lambda self: fields.Date.today())
    attendance_line_ids = fields.One2many('op.attendance.line', 'att_sheet_id', 'Attendance Line')
    course_id = fields.Many2one(string='Course', related='register_id.course_id',
        store=True)
    batch_id = fields.Many2one(string='Batch', related='register_id.batch_id',
        store=True)
    total_present = fields.Integer('Present', compute='_total_present_absent')
    total_absent = fields.Integer('Absent', compute='_total_present_absent')
    total = fields.Integer(compute='_total_present_absent')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')

    _sql_constraints = [
        ('sheet_uniq', 'unique (register_id, attendance_date)',
            "There is already one attencance sheet availble for same date!"),
    ]

