# -*- coding: utf-8 -*-
from openerp import http

# class FinancieraBcra(http.Controller):
#     @http.route('/financiera_bcra/financiera_bcra/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/financiera_bcra/financiera_bcra/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('financiera_bcra.listing', {
#             'root': '/financiera_bcra/financiera_bcra',
#             'objects': http.request.env['financiera_bcra.financiera_bcra'].search([]),
#         })

#     @http.route('/financiera_bcra/financiera_bcra/objects/<model("financiera_bcra.financiera_bcra"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('financiera_bcra.object', {
#             'object': obj
#         })