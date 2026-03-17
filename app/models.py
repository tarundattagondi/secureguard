from datetime import datetime
from app import db


class ComplianceControl(db.Model):
    __tablename__ = 'compliance_controls'

    id = db.Column(db.Integer, primary_key=True)
    control_id = db.Column(db.String(20), unique=True, nullable=False)  # e.g., "ID.AM-1"
    framework = db.Column(db.String(20), nullable=False)  # "NIST CSF" or "ISO 27001"
    category = db.Column(db.String(100), nullable=False)  # e.g., "Identify"
    subcategory = db.Column(db.String(100), nullable=False)  # e.g., "Asset Management"
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='Not Implemented')
    # Status options: Implemented, Partially Implemented, Not Implemented, Not Applicable
    owner = db.Column(db.String(100), default='Unassigned')
    evidence_link = db.Column(db.String(500), default='')
    last_reviewed = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Control {self.control_id}: {self.status}>'


class Risk(db.Model):
    __tablename__ = 'risks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    likelihood = db.Column(db.Integer, nullable=False)  # 1-5
    impact = db.Column(db.Integer, nullable=False)  # 1-5
    risk_score = db.Column(db.Integer, nullable=False)  # likelihood * impact
    status = db.Column(db.String(30), default='Open')
    # Status options: Open, In Progress, Mitigated, Accepted
    mitigation_plan = db.Column(db.Text, default='')
    owner = db.Column(db.String(100), default='Unassigned')
    related_control = db.Column(db.String(20), default='')  # Maps to control_id
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Risk {self.title}: Score {self.risk_score}>'


class ScanResult(db.Model):
    __tablename__ = 'scan_results'

    id = db.Column(db.Integer, primary_key=True)
    scan_type = db.Column(db.String(50), nullable=False)  # "Bandit", "Safety", "Trivy"
    scan_date = db.Column(db.DateTime, default=datetime.utcnow)
    critical_count = db.Column(db.Integer, default=0)
    high_count = db.Column(db.Integer, default=0)
    medium_count = db.Column(db.Integer, default=0)
    low_count = db.Column(db.Integer, default=0)
    total_findings = db.Column(db.Integer, default=0)
    report_summary = db.Column(db.Text, default='')
    pipeline_run_id = db.Column(db.String(100), default='')

    def __repr__(self):
        return f'<Scan {self.scan_type} on {self.scan_date}: {self.total_findings} findings>'


class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    service_description = db.Column(db.Text, default='')
    risk_rating = db.Column(db.String(20), default='Not Assessed')
    # Options: Critical, High, Medium, Low, Not Assessed
    questionnaire_status = db.Column(db.String(30), default='Not Sent')
    # Options: Not Sent, Sent, In Review, Approved, Rejected
    soc2_report_date = db.Column(db.DateTime, nullable=True)
    soc2_expiry_date = db.Column(db.DateTime, nullable=True)
    contact_name = db.Column(db.String(100), default='')
    contact_email = db.Column(db.String(200), default='')
    notes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Vendor {self.name}: {self.risk_rating}>'