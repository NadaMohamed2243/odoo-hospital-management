from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctor'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Image()
    _rec_name = 'first_name'