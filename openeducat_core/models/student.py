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


class OpStudent(models.Model):
    _name = 'op.student'
    _inherits = {'res.partner': 'partner_id'}
    _rec_name = 'full_name'


    @api.multi
    # @api.onchange('name', 'middle_name', 'last_name')
    def _get_full_name(self):
        for rec in self:
            rec.full_name = '%s %s %s' % (rec.name, rec.middle_name or '', rec.last_name)

    @api.multi
    @api.depends('name', 'middle_name', 'last_name')
    def _get_full_name(self):
        for rec in self:
            rec.full_name = '%s %s %s' % (rec.name, rec.middle_name or '', rec.last_name)

    @api.one
    @api.depends('roll_number_line', 'batch_id', 'course_id')
    def _get_curr_roll_number(self):
        # TO_DO:: Improve the logic by adding sequence field in course.
        if self.roll_number_line:
            for roll_no in self.roll_number_line:
                if roll_no.course_id == self.course_id and \
                        roll_no.batch_id == self.batch_id:
                    self.roll_number = roll_no.roll_number
        else:
            self.roll_number = 0


    full_name = fields.Char('Name', compute=_get_full_name, store=True)
    middle_name = fields.Char('Middle Name')
    last_name = fields.Char('Last Name', required=True)
    birth_date = fields.Date('Birth Date', required=True)
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'),
         ('o', 'Other')], 'Gender', required=True)
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info')
    id_number = fields.Char('ID Card Number')
    photo = fields.Binary('Photo')
    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    roll_number_line = fields.One2many(
        'op.roll.number', 'student_id', 'Roll Number')
    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")
    roll_number = fields.Char(
        'Current Roll Number', compute='_get_curr_roll_number', store=True)
    gr_no = fields.Char("GR Number")
    # father details
    father_id = fields.Many2one('res.partner', 'Father')
    f_mobile = fields.Char(related='father_id.mobile', string='Father Mobile')
    # mother details
    mother_id = fields.Many2one('res.partner', 'Mother')
    m_mobile = fields.Char(related='father_id.mobile', string='Father Mobile')

    @api.onchange('user_id')
    def onchange_user_id(self):
        self.user_id.student_id = self.id or False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
