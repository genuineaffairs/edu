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


class OpPeriod(models.Model):
    _name = 'op.period'
    _description = 'Period'
    _order = 'sequence'

    name = fields.Char('Name', required=True)
    hour = fields.Selection([
        ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'),
        ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'),
        ('11', '11'), ('12', '12')], 'Hours', required=True)
    minute = fields.Selection([
        ('00', '00'), ('05', '05'), ('10', '10'), ('15', '15'),
        ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'),
        ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55'),
        ], 'Minute',required=True)
    duration = fields.Float('Duration', required=True)
    am_pm = fields.Selection([
        ('am', 'AM'), ('pm', 'PM')], 'AM/PM', required=True)
    sequence = fields.Integer('Sequence')

