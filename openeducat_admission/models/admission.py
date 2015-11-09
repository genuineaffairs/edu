# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
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
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, UserError


class OpAdmissionState(models.Model):
    _name = 'op.admission.state'
    _order = 'sequence'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(default=20)
    fold = fields.Boolean()
    admission_ids = fields.One2many('op.admission', 'stage_id')


class OpAdmission(models.Model):
    _name = 'op.admission'
    _inherit = 'mail.thread'
    _rec_name = 'application_number'
    _description = "Admission"


    @api.multi
    def _get_full_name(self):
        for rec in self:
            rec.full_name = '%s %s %s' % (rec.name, rec.middle_name or '', rec.last_name)

    @api.multi
    def _default_stage_id(self):
        stage_id = self.env['op.admission.state'].search([], order='sequence asc', limit=1).ids[0] or False
        return stage_id or False


    full_name = fields.Char('Name', compute=_get_full_name)
    name = fields.Char('First Name', required=True,
        )
    middle_name = fields.Char('Middle Name',
        )
    last_name = fields.Char('Last Name', required=True,
        )
    title = fields.Many2one('res.partner.title', 'Title', )
    application_number = fields.Char('Admission Number', copy=False,
        )
    admission_date = fields.Date('Admission Date', copy=False,
        )
    application_date = fields.Datetime('Application Date', required=True, copy=False,
        default=fields.Datetime.now())
    birth_date = fields.Date('Birth Date', required=True, )
    course_id = fields.Many2one('op.course', 'Course', required=True,
        )
    batch_id = fields.Many2one('op.batch', 'Batch', required=False,
        )

    # Address fields
    street = fields.Char()
    street2 = fields.Char()
    phone = fields.Char()
    mobile = fields.Char()
    email = fields.Char()
    city = fields.Char()
    zip = fields.Char()
    state_id = fields.Many2one('res.country.state', 'States',
        )
    country_id = fields.Many2one('res.country', 'Country',
        )

    photo = fields.Binary('Photo', )
    gender = fields.Selection([
        ('m', 'Male'), ('f', 'Female'), ('o', 'Other')], 'Gender',
        required=True, )
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('payment_process', 'Payment Process'), ('fees_paid', 'Fees Paid'),
         ('reject', 'Rejected'), ('pending', 'Pending'),
         ('cancel', 'Cancelled'), ('done', 'Done')],
        'State', readonly=True, select=True,
        default='draft', track_visibility='onchange')
    stage_id = fields.Many2one('op.admission.state', readonly=True,
        default=_default_stage_id,
        track_visibility='onchange')
    fees = fields.Float('Fees', )
    due_date = fields.Date('Due Date', )
    prev_institute_id = fields.Many2one(
        'res.partner', 'Previous Institute',
        )
    prev_course_id = fields.Many2one(
        'op.course', 'Previous Course', )
    prev_result = fields.Char(
        'Previous Result', size=256, )
    family_business = fields.Char('Family Business')
    family_income = fields.Float('Family Income')
    student_id = fields.Many2one('op.student', 'Student', )
    nbr = fields.Integer('No of Admission', readonly=True)
    register_id = fields.Many2one('op.admission.register', 'Admission Register',
        required=True, )
    partner_id = fields.Many2one('res.partner', 'Partner')


    @api.model
    def _read_group_stage_ids(self, ids, domain, read_group_order=None, access_rights_uid=None):
        access_rights_uid = access_rights_uid or self.env.uid
        Stage = self.env['op.admission.state']
        order = Stage._order
        stage_ids = Stage._search([], order=order, access_rights_uid=access_rights_uid)
        stages = Stage.sudo(access_rights_uid).browse(stage_ids)
        result = stages.name_get()

        fold = {}
        for stage in stages:
            fold[stage.id] = stage.fold or False
        return result, fold

    _group_by_full = {
        'stage_id': _read_group_stage_ids
    }


    @api.onchange('register_id')
    def onchange_register(self):
        self.course_id = self.register_id.course_id
        self.fees = self.register_id.product_id.lst_price
        self.admission_date = self.register_id.start_date

    @api.constrains('register_id', 'application_date')
    def _check_admission_register(self):
        start_date = fields.Date.from_string(self.register_id.start_date)
        end_date = fields.Date.from_string(self.register_id.end_date)
        application_date = fields.Date.from_string(self.application_date)
        if application_date < start_date or application_date > end_date:
            raise ValidationError(
                "Application Date should be between Start Date & \
                End Date of Admission Register.")

    @api.multi
    def confirm_in_progress(self):
        self.state = 'confirm'
        if self.partner_id:
            self.state = 'payment_process'


    @api.model
    def create(self, vals):
        admission = super(OpAdmission, self).create(vals)
        suffix = str(admission.id).zfill(4)
        admission.application_number = 'AD' + suffix
        return admission

    # @api.multi
    def get_student_vals(self):
        return {
            'title': self.title.id,
            'name': self.name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'course_id': self.course_id.id,
            'batch_id': self.batch_id.id,
            'photo': self.photo,
            'street': self.street,
            'street2': self.street2,
            'phone': self.phone,
            'mobile': self.mobile,
            'zip': self.zip,
            'city': self.city,
            'country_id': self.country_id.id,
            'state_id': self.state_id.id,
        }

    # @api.multi
    @api.onchange('stage_id')
    def onchange_enroll_student(self):
        self.ensure_one()
        if self.stage_id.code != 'confirmed' and not self.student_id:
            return
        total_admission = self.env['op.admission'].search_count([
            ('register_id', '=', self.register_id.id),
            ])
            # ('state', '=', 'done')])
        if self.register_id.max_count and total_admission >= self.register_id.max_count:
            msg = 'Admission of %s course is now full !' % (self.register_id.course_id)
            raise ValidationError(msg)

        vals = self.get_student_vals()
        vals.update({'partner_id': self.partner_id.id})
        student = self.env['op.student'].create(vals)
        self.write({
            'nbr': 1,
            'state': 'done',
            # 'admission_date': fields.Date.today(),
            'student_id': student.id,
        })

    @api.multi
    def confirm_rejected(self):
        self.state = 'reject'

    @api.multi
    def confirm_pending(self):
        self.state = 'pending'

    @api.multi
    def confirm_to_draft(self):
        self.state = 'draft'

    @api.multi
    def confirm_cancel(self):
        self.state = 'cancel'

    @api.multi
    def payment_process(self):
        self.state = 'fees_paid'

    @api.multi
    def open_student(self):
        form_view = self.env.ref('openeducat_core.view_op_student_form')
        tree_view = self.env.ref('openeducat_core.view_op_student_tree')
        value = {
            'domain': str([('id', '=', self.student_id.id)]),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'op.student',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': self.student_id.id,
            'target': 'current',
            'nodestroy': True
        }
        self.state = 'done'
        return value

    @api.multi
    def create_invoice(self):
        """ Create invoice for fee payment process of student """

        inv_obj = self.env['account.invoice']
        partner_id = self.env['res.partner'].create({'name': self.name})

        account_id = False
        product = self.register_id.product_id
        if product.id:
            account_id = product.property_account_income_id.id
        if not account_id:
            account_id = product.categ_id.property_account_income_categ_id.id
        if not account_id:
            raise UserError(
                _('There is no income account defined for this product: "%s". \
                   You may have to install a chart of account from Accounting \
                   app, settings menu.') % (product.name,))

        if self.fees <= 0.00:
            raise UserError(_('The value of the deposit amount must be \
                             positive.'))
        else:
            amount = self.fees
            name = product.name

        invoice = inv_obj.create({
            'name': self.name,
            'origin': self.application_number,
            'type': 'out_invoice',
            'reference': False,
            'account_id': partner_id.property_account_receivable_id.id,
            'partner_id': partner_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'origin': self.application_number,
                'account_id': account_id,
                'price_unit': amount,
                'quantity': 1.0,
                'discount': 0.0,
                'uom_id': self.register_id.product_id.uom_id.id,
                'product_id': product.id,
            })],
        })
        invoice.compute_taxes()

        form_view = self.env.ref('account.invoice_form')
        tree_view = self.env.ref('account.invoice_tree')
        value = {
            'domain': str([('id', '=', invoice.id)]),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': invoice.id,
            'target': 'current',
            'nodestroy': True
        }
        self.partner_id = partner_id
        self.state = 'payment_process'
        return value


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
