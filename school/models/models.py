# -*- coding: utf-8 -*-
import secrets
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta, MO
from datetime import date, time, datetime
from odoo.exceptions import ValidationError


class student(models.Model):
     _name = 'school.student'
     _description = 'modelo estudiante de school'

     name = fields.Char(string ='Nombre')
     surname = fields.Char(string="Apellidos")
     birthday = fields.Date()

     gender = fields.Selection(
         string='Género',
         selection=[('1', 'Masculino'), ('2', 'Femenino')]
     )
     
     subject_id= fields.Many2many('school.classroom')
     province= fields.Char()
     password=fields.Char()
     level=fields.Selection([('1','Primero'),('2','Segundo')])
     #se admiten 3 estados
     state= fields.Selection([('1','Preinscrito'),('2','Estudiante'),('3','ex-Alumno')],default='1')


     photo = fields.Image(max_width=200, max_height=200)
     age=fields.Integer(string="Edad",compute="_value_age",store=True) # ,store=True

     #Este computo depende de la variable birthday
     @api.depends('birthday')
     #Funcion para calcular el valor de edad
     def _value_age(self):
     #Para cada registro
          for estudiante in self:
              estudiante.age = relativedelta(datetime.today(), estudiante.birthday).years
     
     # funcion para regenerar la contraseña
     def regenerar(self):
        for s in self:
            aux = secrets.token_urlsafe(10)
            s.write({'password':aux})



     #Constraints de SQL del modelo
     #Util cuando la constraint se puede definir con sintaxis SQL
     _sql_constraints = [
     #     ('Chequeo_edad_minima', 'CHECK(age>14)', 'El alumno debe tener mas de 14 años'),
          ('validar_nombre_unico', 'UNIQUE(name)', 'probar nombres unicos')
     ]

     #Util cuando la constraint no se puede definir con sintaxis SQL y debe indicar en una funcion
     # @api.constrains('age')
     # def _check_age(self):
     #    Recorremos el modelo
     #    for record in self:
     #        Comprobamos de cada registro, la edad de estudiante
     #        if record.age < 14:
     #            Si procede, lanzamos una excepcion
     #            raise models.ValidationError('El alumno tiene menos de 15 años')


     #Validacion depende de la variable birthday
     @api.constrains('birthday')
     #Funcion para calcular el valor de edad
     def _validation_age(self):
     #Para cada registro
          for estudiante in self:
               edad = relativedelta(datetime.today(), estudiante.birthday).years
               if edad < 14:
                    #Si procede, lanzamos una excepcion
                    raise models.ValidationError('El alumno tiene menos de 15 años')




class classroom(models.Model):
     _name = 'school.classroom'
     _description = 'modelo clase de school'
     
     name = fields.Char()
     teacher_id= fields.Many2many('school.teacher')
     student_id= fields.Many2many('school.student')
     level=fields.Selection([('1','Primero'),('2','Segundo')])

class teacher (models.Model):
     _name = 'school.teacher'
     _description = 'modelo profesor de school'

     name = fields.Char()
     description =fields.Char()
     classroom_id= fields.Many2many('school.classroom')
     phone = fields.Char()

# Modelo generado para la vista calendar
class seminario(models.Model):
    _name = 'school.seminario'
    _description = 'Modelo seminario'

    name = fields.Char(string="Nombre seminario") 
    start = fields.Datetime() 
    finish = fields.Datetime()
    hours= fields.Integer()
    teachers= fields.Many2one('school.teacher')