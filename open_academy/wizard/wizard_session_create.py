# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreateSessionWizard(models.TransientModel):
    _name = 'open_academy.create_session.wizard'
    _description = 'Create Session Wizard'

    def _set_default_session(self):
        return self.env['open_academy.session'].browse(self._context.get('active_id'))

    session_id = fields.Many2one(string='Session', comodel_name="open_academy.session", required=True, default=_set_default_session)
    attendee_ids = fields.Many2many(string="Attendees", comodel_name="res.partner")

    def action_subscribe_session(self):
        self.session_id.attendee_ids |= self.attendee_ids
        return {}
