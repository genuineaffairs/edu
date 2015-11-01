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


class OpLibraryCardType(models.Model):
    _name = 'op.library.card.type'
    _description = 'Library Card Type'

    name = fields.Char('Name', required=True)
    allow_book = fields.Integer('No of Books Allowed', size=4, required=True)
    duration = fields.Float('Duration', required=True,
        help='Duration in terms of Number of Lead Days')
    penalty_amt_per_day = fields.Float('Penalty Amount per Day', required=True)


class OpLibraryCard(models.Model):
    _name = 'op.library.card'
    _rec_name = 'number'
    _description = 'Library Card'

    partner_id = fields.Many2one('res.partner', 'Card Holder', required=True)
    number = fields.Char('Number', required=True)
    library_card_type_id = fields.Many2one('op.library.card.type', 'Card Type', required=True)
    issue_date = fields.Date('Issue Date', required=True)
    type = fields.Selection([('student', 'Student'), ('faculty', 'Faculty'), ('other', 'Other')],
        'Type', default='student', required=True)
    student_id = fields.Many2one('op.student', 'Student')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')

    @api.onchange('type')
    def onchange_type(self):
        if self.type == 'student':
            self.faculty_id = False
        elif self.type == 'faculty':
            self.student_id = False
        else:
            self.student_id = False
            self.faculty_id = False

    @api.onchange('student_id', 'faculty_id')
    def onchage_partner_id(self):
        self.partner_id = self.student_id.partner_id or self.faculty_id.partner_id or False


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
