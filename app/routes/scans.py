from flask import Blueprint, render_template
from app.models import ScanResult

scans_bp = Blueprint('scans', __name__, url_prefix='/scans')


@scans_bp.route('/')
def list_scans():
    scans = ScanResult.query.order_by(ScanResult.scan_date.desc()).all()

    # Prepare data for trend chart
    chart_data = {
        'labels': [s.scan_date.strftime('%m/%d') for s in reversed(scans[-10:])],
        'critical': [s.critical_count for s in reversed(scans[-10:])],
        'high': [s.high_count for s in reversed(scans[-10:])],
        'medium': [s.medium_count for s in reversed(scans[-10:])],
        'low': [s.low_count for s in reversed(scans[-10:])],
    }

    return render_template('scan_results.html', scans=scans, chart_data=chart_data)