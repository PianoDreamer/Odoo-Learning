# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = "open_academy.session"
    _description = "Academy Session"

    # Common data
    name = fields.Char(string='Name', translate=True)
    course_id = fields.Many2one(string='Course', comodel_name='open_academy.course', required=True)

    instructor_id = fields.Many2one(string='Instructor', comodel_name='res.partner',
                                    domain=lambda self: self._compute_instructor_domain())

    @api.model
    def _compute_instructor_domain(self):
        domain = ['|', ('isinstructor', '=', True),
                  '&', ('category_id.parent_id.name', '=', _('Teacher')), ('category_id.name', '=like', _('Level %'))]
        return domain

    # Period
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today)
    duration = fields.Integer(string='Duration')
    finish_date = fields.Date(compute='_compute_finish_date', store=True)
    days_left = fields.Integer(compute='_compute_days_left')

    # Attendees
    number_of_seats = fields.Integer(string='Number of Seats')
    attendee_ids = fields.Many2many(string='Attendees', comodel_name='res.partner')
    attendees_count = fields.Integer(compute='_compute_attendees_count', store=True)
    taken_seats_ratio = fields.Integer(string='Taken Seats Ratio', compute='_compute_taken_seats_ratio')

    # System
    active = fields.Boolean(default=True)

    @api.depends('start_date', 'duration')
    def _compute_finish_date(self):
        for record in self:
            record.finish_date = record.start_date + timedelta(days=record.duration)

    @api.depends('start_date', 'duration')
    def _compute_days_left(self):
        today = fields.Date.today()
        for record in self:
            record.days_left = 0
            if record.start_date:
                record.days_left = (record.finish_date - today).days

    @api.depends('attendee_ids')
    def _compute_attendees_count(self):
        for record in self:
            record.attendees_count = len(self.attendee_ids)

    @api.depends('number_of_seats', 'attendee_ids')
    def _compute_taken_seats_ratio(self):
        for record in self:
            if record.number_of_seats:
                record.taken_seats_ratio = record.attendees_count / record.number_of_seats * 100
            else:
                record.taken_seats_ratio = 0

    @api.onchange('number_of_seats', 'attendee_ids')
    def _onchange_seats(self):
        if self.number_of_seats < 0:
            return {
                'warning': {
                    'title': _("Wrong value"),
                    'message': _("The field 'Number of Seats' should contain positive value"),
                }
            }
        if len(self.attendee_ids) > self.number_of_seats:
            return {
                'warning': {
                    'title': _("Not enough places"),
                    'message': _("There's not enough places for all attendees"),
                }
            }

    @api.constrains('instructor_id')
    def _check_instructor(self):
        if self.instructor_id in self.attendee_ids:
            raise ValidationError(
                _("Instructor %s can't be in list of his/her session attendees") % self.instructor_id.name)
