# -*- coding: utf-8 -*-
{
    'name': "BCRA connect",

    'summary': """
        Acceso a consultas del Banco Central de Deudores.""",

    'description': """
        Acceso a consultas del Banco Central de Deudores.
    """,

    'author': "Librasoft",
    'website': "http://www.libra-soft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'finance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'financiera_prestamos'],

    # always loaded
    'data': [
			'security/user_groups.xml',
			'security/ir.model.access.csv',
			'security/security.xml',
      'views/bcra_config.xml',
			'views/bcra_consulta.xml',
			'views/bcra.xml',
			'views/extends_res_company.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}