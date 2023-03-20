# -*- coding: utf-8 -*-
{
    'name': "school",

    'summary': """
        Herramienta de gestión de alumnos
        """,

    'description': """
        Modulo que implementa la matricula de los alumnos en una escuela
    """,

    'author': "Pascual Perez",
    'website': "iesch.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        #Estos dos primeros ficheros:
        #1) El primero indica grupo de seguridad basado en rol
        #2) El segundo indica la politica de acceso del modelo
        #Mas información en https://www.odoo.com/documentation/14.0/es/developer/howtos/rdtraining/05_securityintro.html
        #Y en www.odoo.yenthevg.com/creating-security-groups-odoo/      
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
