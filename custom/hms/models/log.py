from odoo import models, fields

class HMSLog(models.Model):
    _name = 'hms.log'

    patient_id = fields.Many2one('hms.patient', required=True)
    created_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    description = fields.Text()
    date = fields.Datetime(default=fields.Datetime.now)
