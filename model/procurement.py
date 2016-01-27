# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api, exceptions, _
from openerp.addons import decimal_precision as dp


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'


    @api.multi
    def make_mo(self):
        print '----- Sobreescribiendo make_mo -----'
        res = super(ProcurementOrder, self).make_mo()
        production_id = res.values()[0]
        sale_order_id = self.env['mrp.production'].search_read([('id', '=', production_id)], ['sale_order'])
        sale_order_line_id = self.env['sale.order.line'].search_read([('order_id', '=', sale_order_id[0]['sale_order'][0])], ['id', 'product_cantidad_total'])
        sale_order_line_attr = self.env['sale.order.line.attribute'].search_read([('sale_line', '=', sale_order_line_id[0]['id'])], ['attribute', 'value', 'size_x', 'size_y', 'size_z'])
        cantidad_total_product = 0.0
        for a in sale_order_line_attr:
            attribute = False
            value = False
            size_x = 0.0
            size_y = 0.0
            size_z = 0.0
            attribute = a['attribute'][0]
            if a['value']:
                value = a['value'][0]
            else:
                value = False
            if a['size_x']:
                size_x = a['size_x']
            else:
                size_x = 0.0
            if a['size_y']:
                size_y = a['size_y']
            else:
                size_y = 0.0
            if a['size_z']:
                size_z = a['size_z']
            else:
                size_z = 0.0
            mrp_production_attr_id = self.env['mrp.production.attribute'].search_read([('attribute', '=', attribute), ('mrp_production', '=', production_id)], ['id'])
            mrp_production_attr_obj = self.env['mrp.production.attribute'].browse(mrp_production_attr_id[0]['id'])
            mp_qty = 1 * (size_x or 1.0) * (size_y or 1.0) * (size_z)
            mrp_production_attr_obj.write({'size_x': size_x, 'size_y': size_y, 'size_z': size_z, 'mp_qty': mp_qty})
            cantidad_total_product += mp_qty / 10000
        mrp_production_obj = self.env['mrp.production'].browse(production_id)
        mrp_production_obj.write({'product_qty': round(cantidad_total_product, 2)})
        return res