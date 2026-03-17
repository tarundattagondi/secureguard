from flask import Blueprint, render_template
from app.models import ComplianceControl, Risk, ScanResult, Vendor

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    # Calculate compliance score
    total_controls = ComplianceControl.query.count()
    implemented = ComplianceControl.query.filter_by(status='Implemented').count()
    compliance_score = round((implemented / total_controls) * 100) if total_controls > 0 else 0

    # Count open risks
    open_risks = Risk.query.filter(Risk.status.in_(['Open', 'In Progress'])).count()

    # Get latest scan
    latest_scan = ScanResult.query.order_by(ScanResult.scan_date.desc()).first()
    scan_findings = latest_scan.total_findings if latest_scan else 0

    # Count vendors under review
    vendors_review = Vendor.query.filter(
        Vendor.questionnaire_status.in_(['Sent', 'In Review'])
    ).count()

    # Get recent risks for activity feed
    recent_risks = Risk.query.order_by(Risk.created_at.desc()).limit(5).all()

    # Get control status breakdown for chart
    control_statuses = {
        'Implemented': ComplianceControl.query.filter_by(status='Implemented').count(),
        'Partially Implemented': ComplianceControl.query.filter_by(status='Partially Implemented').count(),
        'Not Implemented': ComplianceControl.query.filter_by(status='Not Implemented').count(),
        'Not Applicable': ComplianceControl.query.filter_by(status='Not Applicable').count(),
    }

    return render_template('dashboard.html',
                           compliance_score=compliance_score,
                           open_risks=open_risks,
                           scan_findings=scan_findings,
                           vendors_review=vendors_review,
                           recent_risks=recent_risks,
                           control_statuses=control_statuses)