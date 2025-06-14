# Odoo HMS (Hospital Management System)

This is a custom Odoo module developed to manage hospital operations.

## 🌟 Features

- Manage **Patients** (first name, last name, email, blood type, PCR, CR Ratio, etc.)
- Manage **Departments** with capacity and availability
- Manage **Doctors**, linked to departments and patients
- Automatic **age** calculation from birthdate
- Conditional field logic and validations:
  - PCR checkbox auto-checks if age < 30
  - History hidden if age < 50
  - CR Ratio required when PCR is checked
  - Cannot select a closed department
- Patient states: Undetermined, Good, Fair, Serious + state change log
- Report template for printing patient information
- Integration with CRM Customers (linked by email)
- Access rights:
  - **User Group**: can manage own patients, read doctors/departments
  - **Manager Group**: full access to everything
- Prevent customer deletion if linked to a patient

## 📁 Structure

- `models/`: Python models (`patient.py`, `department.py`, etc.)
- `views/`: XML files for form/tree views and menus
- `security/`: Access control and group definitions
- `reports/`: QWeb report template for patient report

## 🛠️ Requirements

- Odoo 15/16/18 (use the one matching your development)
- Python 3.x
- PostgreSQL

## 🚀 Installation

1. Clone this repository into your Odoo `addons/` folder:
   ```bash
   git clone https://github.com/your-username/odoo-hms.git
2. Restart Odoo server and activate Developer Mode

3. Install the HMS module from the Apps menu

## 📄 License
MIT License


---

### ✅ .gitignore (recommended)

```gitignore
*.pyc
*.pyo
*.swp
*.~ 
__pycache__/
*.log
.idea/
*.db
.env
venv/
.odoo/
.DS_Store
*.iml
*.bak
*.zip
*.tar.gz
addons/odoo/
