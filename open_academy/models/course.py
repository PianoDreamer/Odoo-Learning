# -*- coding: utf-8 -*-

from odoo import models, fields


class Course(models.Model):
    _name = "open_academy.course"
    _description = "Academy Course"
    _rec_name = 'title'
    _sql_constraints = [
        ('check_title_not_equal_description',
         'CHECK(title != description)',
         "Course 'title' and 'description' must be different!"),
        ('check_title_unique',
         'UNIQUE(title)',
         "Course 'title' must be unique!")
    ]

    # Common data
    title = fields.Char(string='Title', required=True, translate=True)
    description = fields.Text(string='Description')

    # Course data
    responsible_id = fields.Many2one(string='Responsible', comodel_name='res.users')
    session_ids = fields.One2many(string='Session', comodel_name='open_academy.session', inverse_name='course_id')

    def copy(self, default={}):
        default['name'] = 'Copy of '+ self.name
        return super(Course, self).copy(default)
