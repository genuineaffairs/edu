# -*- coding: utf-8 -*-

from openerp import api, fields, models


class FeeTemplate(models.Model):
    _name = 'edu.fee.template'
    _description = 'Fee Template'


    @api.depends('fee_line_ids')
    def _compute_total(self):
        for record in self:
            record.total = sum(line.list_price for line in record.fee_line_ids)

    @api.multi
    @api.onchange('parent_id')
    def onchange_is_parent(self):
        for rec in self:
            rec.is_parent = True if rec.parent_id else False


    name = fields.Char(required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')],
        'State', default='draft')
    active = fields.Boolean(default=True)
    is_parent = fields.Boolean()
    is_refundable = fields.Boolean()
    template_id = fields.Many2one('edu.fee.template', 'Template')
    parent_id = fields.Many2one('edu.fee.template', 'Parent Template')
    child_ids = fields.One2many('edu.fee.template', 'parent_id', 'Child Templates')
    fee_line_ids = fields.Many2many('product.product', string='Fees', domain=[('is_fee', '=', True)])
    # term_ids = fields.One2many('edu.fee.term', 'template_id', string='Fees Terms')
    # term_ids = fields.Many2many('edu.fee.term', 'edu_fee_tmpl_term_rel', 'tmpl_id', 'prod_id',
    #     string='Fees Terms')
    # product_ids = fields.Many2many('product.product', 'edu_fee_tmpl_prod_rel',
    #     'tmpl_id', 'prod_id', string="Fee Lines")
    total = fields.Monetary('Total', compute=_compute_total, store=True)
    currency_id = fields.Many2one('res.currency', string='Currency')

    @api.multi
    def confirm_fee_template(self):
        for record in self:
            record.write({'state': 'confirm'})


# class OpFeeTerm(models.Model):
#     _name = 'edu.fee.term'

#     @api.multi
#     @api.depends('fee_lines')
#     def _compute_total(self):
#         for record in self:
#             record.total = sum(line.list_price for line in record.fee_lines)

#     name = fields.Char('Name', required=True)
#     template_id = fields.Many2one('edu.fee.template', 'Template')
#     course_id = fields.Many2one(related='template_id.course_id', string='Course',
#         readonly=True)
#     active = fields.Boolean(default=True)
#     fee_lines = fields.Many2many('product.product', 'edu_fee_term_product', 'term_id', 'product_id',
#         string='Fees', domain=[('is_fee', '=', True)])
#     currency_id = fields.Many2one('res.currency', string='Currency')
#     total = fields.Monetary('Total', compute=_compute_total, store=True)



class ProductProduct(models.Model):
    """ Make product as fee lines
    """
    _inherit = 'product.product'

    name_code = fields.Char()
    is_fee = fields.Boolean('Is Fee')
    refundable = fields.Boolean('Refundable')
    new_admission = fields.Boolean('New Student')

    @api.model
    def create(self, vals):
        vals.update({
            'standard_price': vals.get('list_price', 0.0),
            'type': 'service'
        })
        return super(ProductProduct, self).create(vals)
