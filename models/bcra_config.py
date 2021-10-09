# -*- coding: utf-8 -*-

from openerp import models, fields, api

class FinancieraBcraConfig(models.Model):
	_name = 'financiera.bcra.config'

	name = fields.Char("Nombre")
	bcra_id = fields.Many2one('financiera.bcra', 'BCRA base')
	