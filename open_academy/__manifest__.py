# -*- coding: utf-8 -*-

{
    # Default properties (10)
    'name': "Open Academy",
    'summary': "Open Academy Accounting",
    'description': """Open Academy Accounting Software""",
    'author': "Me",
    'website': "http://www.dummy.com",
    'category': 'Services',
    'version': '1.0',
    'depends': [
        'base',
        'board',
    ],
    'data': [
        'security/open_academy_security.xml',
        'security/ir.model.access.csv',
        'views/root_menu_views.xml',
        'wizard/wizard_session_create_views.xml',
        'views/course_views.xml',
        'views/session_views.xml',
        'views/dashboard_views.xml',
        'views/partner_views.xml',
        'views/common_views.xml',
        'data/course_predefined.xml',
        'data/partner_category_predefined.xml',
        'report/session_templates.xml',
        'report/session_report.xml',
    ],
    'demo': [],

    # Additional properties (3)
    'sequence': 1,
    'application': True,
    'license': 'LGPL-3'
}
