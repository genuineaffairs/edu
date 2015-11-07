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

{
    'name': 'Edu365 Fees',
    'version': '1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Fee Collection',
    'description': """
        This module provide feature of fees collection &
        other finance operations.

    """,
    'author': 'KaizenDT',
    'website': 'http://www.kaizendt.com',
    'depends': ['openeducat_core', 'account_accountant'],
    'data': [
        # 'views/fee_term_views.xml',
        'views/fee_template_views.xml',
        'views/fee_category_views.xml',
        'views/fee_collect_views.xml',
        'views/fee_refund_views.xml',
        'fee_menus.xml',
    ],
    'demo': [
        'demo/product.product.csv',
        'demo/edu.fee.template.csv',
    ],
    'images': [
        'static/description/openeducat_fees_banner.jpg',
    ],
    'installable': True,
    'application': True,
}
