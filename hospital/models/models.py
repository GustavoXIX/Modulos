# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta, MO
from odoo.exceptions import ValidationError 



class paciente(models.Model):
     _name = 'hospital.paciente'
     _no_descriptionmbre = 'Pacientes del hospital'
     
     code = fields.Char(string="Código")
     name = fields.Char(string ='Nombre')
     surname = fields.Char(string="Apellidos")
     adress = fields.Char(string="Dirección")
     city = fields.Char(string="Población")
     province = fields.Char(string="Provincia")
     postal_code = fields.Char(string="Código Postal")
     phone = fields.Char(string="Telefono")
     
     
     ingresos_id = fields.Many2one('hospital.ingreso')
     doctores_ids = fields.Many2many('hospital.doctores') 

     F_Nacimiento = fields.Date()


class ingreso(models.Model):
     _name = 'hospital.ingreso'
     _description = 'Ingresos pasados y actuales del paciente'
     
     code = fields.Char(string="Código")
     room = fields.Char(string ='Hambitación')
     bed = fields.Char(string ='Cama')
     f_ingreso = fields.Date(string='Fecha de ingreso', default=datetime.utcnow())
     salida = fields.Date()
     symtomps = fields.Text(string ='Síntomas')
     diagnostico = fields.Text(string ='Diagnóstico')    
     dias_ingresado = fields.Integer(string="Dias ingresado",compute="_dias_ingresado")
     #field para seleccionar cama A o B
     cama = fields.Selection([('A', 'A'),('B', 'B')], string='Cama')


     doctor_id = fields.Many2one('hospital.doctores')
     patience_id  = fields.One2many('hospital.paciente', 'ingresos_id')


     # @api.constrains('ingreso')
     # def _check_ingreso(self):
     #      for record in self: 
     #           hoy = date.today()
     #           unasemana = timedelta(days=7)
     #           if record.f_ingreso < hoy - unasemana:
     #                raise ValidationError("la fecha de ingreso no puede ser mayor a una semana")

     # comstraint para que f_ingreso no pueda ser anterior a una semana
     @api.constrains('f_ingreso')
     def _check_ingreso(self):
          for record in self: 
               if record.f_ingreso < date.today() - timedelta(days=7):
                    raise ValidationError("la fecha de ingreso no puede ser mayor al una semana atrás")
     
     @api.constrains('salida')
     def _check_salida(self):
          for record in self: 
               if record.salida > date.today() + timedelta(days=1):
                    raise ValidationError("la fecha de salida no puede ser mayor al día de hoy")

     @api.depends('salida')
     def _dias_ingresado(self):
          for i in self:
               i.dias_ingresado = relativedelta(i.salida, i.f_ingreso).days
                  

class doctores(models.Model):
     _name = 'hospital.doctores'
     _description = 'Doctores del hospital'

     name = fields.Char(string ='Nombre')
     surname = fields.Char(string="Apellidos")
     code = fields.Char(string ='Código')
     phone = fields.Char(string="Telefono")
     especiality = fields.Char(string ='Especialidad')
     college = fields.Char(string ='Número de colegiado')
     
     ingresos_ids = fields.One2many('hospital.ingreso', 'doctor_id')
     patience_ids = fields.Many2many('hospital.paciente') 
     
     photo = fields.Image(max_width=200, max_height=200)

     _sql_constraints = [
          ('validar_colegiatura_unica', 'UNIQUE(college)', 'El número de colegiatura ya existe')
     ]
      


class Diagnostico(models.Model):
    _name = 'hospital.diagnostico'
    _descripcion = 'Diagnostico a enfermedades de pacientes'

    diagnostico = fields.Char(string ='Diagnostico')
    fecha = fields.Date()

    patience  = fields.Many2one('hospital.paciente')





 # clases wizard
class paciente_wizard(models.TransientModel):
	_name = 'hospital.paciente_wizard'
	
    #todos los atributos que queremos trabajar
    # estado en el que esta el asistente
	state = fields.Selection([('1','Paciente'),('2','Ingreso'),('3','doctores'),('4','Enrollment')],default='1')
	name = fields.Char()
	
    #atributos de Ingreso
	symtomps = fields.Char(string='síntomas')
	f_ingreso = fields.Date(string='Ingreso', default=datetime.utcnow())
	f_salida = fields.Date(string='Salida')
	
    #atributos de doctores
	d_name = fields.Char(string='Nombre de doctor')
	d_surname = fields.Char(string='Apellido de doctor')
	doctores = fields.Many2many('hospital.doctor_aux')

    #metodo accedido desde el boton del controller
    #accedo al modelo
	@api.model
	def action_paciente_wizard(self):
		action = self.env.ref('hospital.action_paciente_wizard').read()[0]
		return action

	def next(self):
		if self.state == '1':
			self.state = '2'
		elif self.state == '2':
			self.state = '3'
		elif self.state == '3':
			self.state = '4'
		return {
           	'type': 'ir.actions.act_window',
           	'res_model': self._name,
           	'res_id': self.id,
           	'view_mode': 'form',
           	'target': 'new',
        }
	def previous(self):
		if self.state == '2':
			self.state = '1'
		elif self.state == '3':
			self.state = '2'
		elif self.state == '4':
			self.state = '3'
		return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    #añadir clase al modelo temporal
	def add_ingreso(self):
		for c in self:
			#0 permite crear crear un ingreso
			c.write({'Ingreso':[(0,0,{'symtomps':c.symtomps,'f_salida':c.f_salida})]})
		
		# devolvemos la vista que queremos actualizar
		return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    #añadir doctores al modelo temporal
	def add_doctores(self):
		for c in self:
			c.write({'doctores':[(0,0,{'name':c.d_name,
                                    'surname':c.surname})]})
		return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    #confirmar los datos, mostrando todo
	def commit(self):
		return {
			'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    #transladamos al modelo los datos temporales
    #importante el orden, PACIENTE, INGRESO asociada a al PACIENTE  , DOCTOR a la clase
	def create_paciente(self):
		for c in self:
			paciente = c.env['hospital.paciente'].create({'name': c.name})
			doctores = []
			for cl in c.Ingreso:
				ingreso = c.env['hospital.ingreso'].create({'symtomps':cl.symtomps,
						        'f_ingreso':cl.f_ingreso,
			                    'f_salida':cl.f_salida})
				for st in cl.doctores:
					doctor=c.env['hospital.doctores'].create({'name': st.d_name,
                                                     	'surname': st.d_surname
                                                     	})
					doctores.append(doctor.id)
			paciente.write({'doctores':[(6,0,doctores)]})
		#devolvemos la vista, para que se refresque
		return {
        	'type': 'ir.actions.act_window',
        	'res_model': 'hospital.paciente',
        	'res_id': paciente.id,
        	'view_mode': 'form',
        	'target': 'current',
    	}

class doctor_aux(models.TransientModel):
	_name = 'hospital.doctor_aux'
	name = fields.Char()
	surname = fields.Char()
	doctores = fields.One2many('hospital.doctor_aux','doctores')



