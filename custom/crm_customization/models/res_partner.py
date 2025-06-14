from odoo import models, fields, api
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='related_patient_id')

    @api.constrains('email', 'related_patient_id')
    def _check_email_not_in_patients(self):
        for rec in self:
            if rec.email:
                existing_patient = self.env['hms.patient'].search([('email', '=', rec.email)])
                if existing_patient:
                    raise UserError("This email already exists in the patient model.")
    
    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise UserError("You cannot delete a customer linked to a patient.")
