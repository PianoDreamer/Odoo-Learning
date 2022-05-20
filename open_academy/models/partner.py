# -*- coding: utf-8 -*-

from odoo import models, fields


class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    isinstructor = fields.Boolean(string="Instructor")
    session_ids = fields.Many2many(string="Attendee's Sessions", comodel_name='open_academy.session')
