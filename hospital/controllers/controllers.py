# -*- coding: utf-8 -*-
from odoo import http

class MyController(http.Controller):
    @http.route('/hospital/paciente/', auth='user', type='json')
    def paciente(self):
        return {
            'html': """
                <div id="hospital_banner">
                 <link href="/hospital/static/banner.css"
                    rel="stylesheet">
                   
                <h1>Paciente</h1>
                <p>Creación de pacientes</p>
                <a class="paciente_button" type="action" data-reload-on-close="true" role="button" data-method="action_paciente_wizard" data-model="hospital.paciente_wizard">
                Crear paciente
            </a>
            </div> """
        }