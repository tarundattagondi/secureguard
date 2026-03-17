from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import ComplianceControl

controls_bp = Blueprint('controls', __name__, url_prefix='/controls')


@controls_bp.route('/')
def list_controls():
    # Filter by framework or status
    framework = request.args.get('framework', '')
    status = request.args.get('status', '')

    query = ComplianceControl.query

    if framework:
        query = query.filter_by(framework=framework)
    if status:
        query = query.filter_by(status=status)

    controls = query.order_by(ComplianceControl.control_id).all()
    return render_template('controls.html', controls=controls,
                           current_framework=framework, current_status=status)


@controls_bp.route('/<int:control_id>/update', methods=['POST'])
def update_control(control_id):
    control = ComplianceControl.query.get_or_404(control_id)
    control.status = request.form.get('status', control.status)
    control.owner = request.form.get('owner', control.owner)
    control.evidence_link = request.form.get('evidence_link', control.evidence_link)
    db.session.commit()
    return redirect(url_for('controls.list_controls'))