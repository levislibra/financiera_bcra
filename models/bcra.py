# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError
import base64

class FinancieraBcra(models.Model):
	_name = 'financiera.bcra'

	name = fields.Char("Nombre")
	anio = fields.Char("Año")
	mes = fields.Selection([
		('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'),
		('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'),
		('07', 'Julio'), ('08', 'Agosto'), ('09', 'Setiembre'),
		('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
	], "Mes")
	bcra_registro_ids = fields.One2many('financiera.bcra.registro', 'bcra_id', 'Registros')

	@api.onchange('anio', 'mes')
	def onchange_anio_mes(self):
		self.name = 'BCRA/'
		if self.anio:
			self.name = self.name + self.anio
		if self.mes:
			self.name = self.name + '/' + self.mes

class FinancieraBcraRegistro(models.Model):
	_name = 'financiera.bcra.registro'

	_order = 'create_date asc'
	name = fields.Char()
	bcra_id = fields.Many2one('financiera.bcra', 'BCRA', ondelete="cascade")
	codigo_entidad = fields.Char('Código de entidad')
	fecha_informacion = fields.Char('Fecha de información')
	tipo_identificacion = fields.Char('Tipo de identificación')
	nro_identificacion = fields.Char('N° de identificación')
	actividad = fields.Char('Actividad')
	situacion = fields.Char('Situación')
	prestamos_total = fields.Char('Préstamos/Total')
	participaciones = fields.Char('Participaciones')
	garantias_otorgadas = fields.Char('Garantías otorgadas')
	otros_conceptos = fields.Char('Otros conceptos')
	garantias_preferidas_a = fields.Char('Garantías preferidas A')
	garantias_preferidas_b = fields.Char('Garantías preferidas B')
	sin_garantias_preferidas = fields.Char('Sin garantías preferidas')
	contragarantias_preferidas_a = fields.Char('Contragarantías preferidas A')
	contragarantias_preferidas_b = fields.Char('Contragarantías preferidas B')
	sin_contragarantias_preferidas = fields.Char('Sin contragarantías preferidas')
	previsiones = fields.Char('Previsiones')
	deuda_cubierta = fields.Char('Deuda cubierta')
	proceso_judicial_revision = fields.Char('Proceso Judicial/Revisión')
	refinanciaciones = fields.Char('Refinanciaciones')
	recategorizacion_obligatorio = fields.Char('Recategorización obligatoria')
	situacion_juridica = fields.Char('Situación jurídica')
	irrecuperables_disposicion_tecnica = fields.Char('Irrecuperables por disposición técnica')
	dias_atraso = fields.Char('Días de atraso')

class FinancieraBcraConsulta(models.Model):
	_name = 'financiera.bcra.consulta'

	name = fields.Char("Nombre")
	identificacion = fields.Char("Identificacion")
	peor_situacion = fields.Integer("Peor situacion")
	monto_total = fields.Float("Monto total")
	detalle_por_banco = fields.Char("Detalle por banco")
	company_id = fields.Many2one('res.company', 'Empresa', default=lambda self: self.env['res.company']._company_default_get('financiera.bcra.consulta'))

	@api.model
	def create(self, values):
		result = super(FinancieraBcraConsulta, self).create(values)
		result.update({
			'name': 'BCRA/' + str(result.id).zfill(8),
		})
		return result

	@api.onchange('identificacion')
	def onchange_identificacion(self):
		self.peor_situacion = 0
		self.monto_total = 0
		self.detalle_por_banco = False

	@api.one
	def consultar_bcra(self):
		bcra_id = self.company_id.bcra_id.bcra_id
		if bcra_id and self.identificacion:
			bcra_registro_obj = self.pool.get('financiera.bcra.registro')
			bcra_registro_ids = bcra_registro_obj.search(self.env.cr, self.env.uid, [
				('bcra_id.id', '=', bcra_id.id),
				('nro_identificacion', '=', self.identificacion),
			])
			bcra_registro_ids = bcra_registro_obj.browse(self.env.cr, self.env.uid, bcra_registro_ids)
			peor_situacion = 0
			monto_total = 0
			bank_obj = self.pool.get('res.bank')
			detalle_por_banco = ""
			for bcra_registro_id in bcra_registro_ids:
				# procesamos codigo entidad
				codigo_entidad = bcra_registro_id.codigo_entidad[2:]
				bank_ids = bank_obj.search(self.env.cr, self.env.uid, [
					('code', '=', codigo_entidad),
				])
				name_bank = codigo_entidad.ljust(60, ' ')
				if len(bank_ids) > 0:
					name_bank = bank_obj.browse(self.env.cr, self.env.uid, bank_ids[0]).name.ljust(60, ' ')
				# procesamos monto prestamos
				monto = bcra_registro_id.prestamos_total.replace(',', '.')
				monto = float(monto) * 1000
				if monto == 0:
					monto = bcra_registro_id.previsiones.replace(',', '.')
					monto = float(monto) * 1000
				monto_char = str(monto).ljust(20, ' ')
				monto_total = monto_total + monto
				# procesamos situacion
				situacion_char = bcra_registro_id.situacion.ljust(10, ' ')
				peor_situacion = max(peor_situacion, int(bcra_registro_id.situacion))
				# unimos el detalle
				detalle_por_banco = detalle_por_banco + name_bank + situacion_char + monto_char + '<br/>'
			result_dict = {
				'peor_situacion': peor_situacion,
				'monto_total': monto_total,
				'detalle_por_banco': detalle_por_banco,
			}
			self.write(result_dict)
		return result_dict
				
class FinancieraBcraTmp(models.Model):
	_name = 'financiera.bcra.tmp'

	name = fields.Char("Columna")