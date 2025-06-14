from datetime import date
import re
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    address = fields.Text(string='Address')
    pcr = fields.Boolean(string='PCR')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    cr_ratio = fields.Float(string='CR Ratio')
    # image = fields.Binary(string='Image')
    image = fields.Image(string='Image', max_width=1024, max_height=1024)
    blood_type = fields.Selection(
        [('A+', 'A+'),('A-', 'A-'), ('B+', 'B+'),('B-', 'B-'),('AB-', 'AB-'),('AB+', 'AB+'), ('O+', 'O+'), ('O-', 'O-')],
        string='Blood Type'
    )
    department_id = fields.Many2one('hms.department', string="Department")
    department_capacity = fields.Integer(related='department_id.capacity', string="Capacity", readonly=True)
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors")

    log_ids = fields.One2many('hms.log', 'patient_id', string="Logs")

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined', tracking=True)

    email = fields.Char(string='Email', required=True)

    def move_to_good(self):
        self.state = 'good'
        
    def move_to_fair(self):
        self.state = 'fair'
        
    
    def move_to_serious(self):
        self.state = 'serious'


    @api.onchange('age')
    def onchange_age_auto_check_pcr(self):
        if self.age < 30:
            self.pcr = True 
            return {
                'warning': {
                    'title': 'PCR Auto-Checked',
                    'message': 'PCR was automatically checked because patient age is below 30.',
                }
            }
        

    def write(self, vals):
        for rec in self:
            old_state = rec.state
            res = super(HmsPatient, rec).write(vals)
            new_state = vals.get('state')
            if new_state and old_state != new_state:
                self.env['hms.log'].create({
                    'patient_id': rec.id,
                    'description': f"State changed to {new_state}"
                })
        return res
    
    @api.constrains('email')
    def check_email_valid(self):
        for rec in self:
            if rec.email:
                pattern = r"[^@]+@[^@]+\.[^@]+"
                if not re.match(pattern, rec.email):
                    raise UserError("Please enter a valid email address.")
                
    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'Email must be unique for each patient.')
    ]


    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year
                if (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day):
                    rec.age -= 1
            else:
                rec.age = 0