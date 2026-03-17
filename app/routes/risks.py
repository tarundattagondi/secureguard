from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Risk

risks_bp = Blueprint('risks', __name__, url_prefix='/risks')


@risks_bp.route('/')
def list_risks():
    status_filter = request.args.get('status', '')
    query = Risk.query

    if status_filter:
        query = query.filter_by(status=status_filter)

    risks = query.order_by(Risk.risk_score.desc()).all()
    return render_template('risk_register.html', risks=risks, current_status=status_filter)


@risks_bp.route('/add', methods=['POST'])
def add_risk():
    likelihood = int(request.form.get('likelihood', 1))
    impact = int(request.form.get('impact', 1))

    risk = Risk(
        title=request.form.get('title', ''),
        description=request.form.get('description', ''),
        likelihood=likelihood,
        impact=impact,
        risk_score=likelihood * impact,
        status=request.form.get('status', 'Open'),
        mitigation_plan=request.form.get('mitigation_plan', ''),
        owner=request.form.get('owner', 'Unassigned'),
        related_control=request.form.get('related_control', '')
    )
    db.session.add(risk)
    db.session.commit()
    return redirect(url_for('risks.list_risks'))


@risks_bp.route('/<int:risk_id>/update', methods=['POST'])
def update_risk(risk_id):
    risk = Risk.query.get_or_404(risk_id)
    risk.status = request.form.get('status', risk.status)
    risk.mitigation_plan = request.form.get('mitigation_plan', risk.mitigation_plan)
    db.session.commit()
    return redirect(url_for('risks.list_risks'))