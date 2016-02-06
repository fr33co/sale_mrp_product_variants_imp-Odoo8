# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api, exceptions, _
from openerp.addons import decimal_precision as dp


class ProductAttributeValueSaleLine(models.Model):
	_name = 'sale.order.line.attribute'
	
	@api.one
	@api.depends('value', 'sale_line.product_template', 'mp_qty')
	def _get_price_extra(self):
		print '----- Sobreescribiendo _get_price_extra -----'
		res = super(ProductAttributeValueSaleLine, self)._get_price_extra()
		return res


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'
	
	@api.multi
	def update_price_unit(self):
		print '----- Sobreescribiendo update_price_unit -----'
		res = super(SaleOrderLine, self).update_price_unit()
		return res