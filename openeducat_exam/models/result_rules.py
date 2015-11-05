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

RESULT_STATUS = [('pass', 'PASS'), ('fail', 'FAIL')]

class OpResultRuleTemplate(models.Model):
    _name = 'op.result.rule.template'

    name = fields.Char(required=True)
    pass_status_ids = fields.One2many('op.status.pass', 'template_id', 'Pass Rules')
    fail_status_ids = fields.One2many('op.status.fail', 'template_id', 'Fail Rules')
    active = fields.Boolean(default=True)


class OpPassStatus(models.Model):
    _name = 'op.status.pass'
    _description = 'Pass Status'

    name = fields.Char('Name', required=True)
    min_percentage = fields.Float('Minimum Percentage', required=True)
    display_result = fields.Char('Result to Display', required=True)
    status = fields.Selection(RESULT_STATUS, 'Status', default='pass')
    template_id = fields.Many2one('op.result.rule.template', required=True)


class OpFailStatus(models.Model):
    _name = "op.status.fail"

    name = fields.Char('Name', required=True)
    number = fields.Integer('Number of Failed Subject', required=True)
    display_result = fields.Char('Result to Display', required=True)
    status = fields.Selection(RESULT_STATUS, 'Status', default='fail')
    template_id = fields.Many2one('op.result.rule.template', required=True)

