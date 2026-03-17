from app.models import ComplianceControl, Risk, ScanResult, Vendor
from datetime import datetime


class TestComplianceControl:
    def test_create_control(self, db):
        control = ComplianceControl(
            control_id='ID.AM-1',
            framework='NIST CSF',
            category='Identify',
            subcategory='Asset Management',
            description='Physical devices are inventoried',
            status='Not Implemented',
            owner='Security Team'
        )
        db.session.add(control)
        db.session.commit()

        saved = ComplianceControl.query.filter_by(control_id='ID.AM-1').first()
        assert saved is not None
        assert saved.framework == 'NIST CSF'
        assert saved.category == 'Identify'
        assert saved.status == 'Not Implemented'

    def test_default_status(self, db):
        control = ComplianceControl(
            control_id='PR.AC-1',
            framework='NIST CSF',
            category='Protect',
            subcategory='Access Control',
            description='Identities are managed'
        )
        db.session.add(control)
        db.session.commit()

        saved = ComplianceControl.query.filter_by(control_id='PR.AC-1').first()
        assert saved.status == 'Not Implemented'
        assert saved.owner == 'Unassigned'

    def test_control_repr(self, db):
        control = ComplianceControl(
            control_id='DE.CM-1',
            framework='NIST CSF',
            category='Detect',
            subcategory='Continuous Monitoring',
            description='Network is monitored',
            status='Implemented'
        )
        db.session.add(control)
        db.session.commit()

        assert 'DE.CM-1' in repr(control)
        assert 'Implemented' in repr(control)


class TestRisk:
    def test_create_risk(self, db):
        risk = Risk(
            title='Unpatched servers',
            description='Multiple servers running outdated OS',
            likelihood=4,
            impact=5,
            risk_score=20,
            status='Open',
            owner='IT Operations'
        )
        db.session.add(risk)
        db.session.commit()

        saved = Risk.query.filter_by(title='Unpatched servers').first()
        assert saved is not None
        assert saved.risk_score == 20
        assert saved.status == 'Open'

    def test_risk_score_calculation(self, db):
        risk = Risk(
            title='Weak passwords',
            description='Default passwords in use',
            likelihood=3,
            impact=4,
            risk_score=3 * 4,
            status='Open'
        )
        db.session.add(risk)
        db.session.commit()

        assert risk.risk_score == 12

    def test_risk_critical_score(self, db):
        risk = Risk(
            title='Data breach',
            description='Customer PII exposed',
            likelihood=5,
            impact=5,
            risk_score=25,
            status='Open'
        )
        db.session.add(risk)
        db.session.commit()

        assert risk.risk_score >= 20  # Critical threshold

    def test_risk_default_values(self, db):
        risk = Risk(
            title='Test risk',
            description='Test description',
            likelihood=1,
            impact=1,
            risk_score=1
        )
        db.session.add(risk)
        db.session.commit()

        assert risk.status == 'Open'
        assert risk.owner == 'Unassigned'
        assert risk.mitigation_plan == ''


class TestScanResult:
    def test_create_scan(self, db):
        scan = ScanResult(
            scan_type='Bandit',
            critical_count=2,
            high_count=5,
            medium_count=8,
            low_count=12,
            total_findings=27,
            report_summary='Bandit scan completed',
            pipeline_run_id='run-1001'
        )
        db.session.add(scan)
        db.session.commit()

        saved = ScanResult.query.filter_by(scan_type='Bandit').first()
        assert saved.total_findings == 27
        assert saved.critical_count == 2

    def test_scan_total_matches(self, db):
        scan = ScanResult(
            scan_type='Trivy',
            critical_count=1,
            high_count=3,
            medium_count=5,
            low_count=7,
            total_findings=1 + 3 + 5 + 7,
            pipeline_run_id='run-1002'
        )
        db.session.add(scan)
        db.session.commit()

        assert scan.total_findings == scan.critical_count + scan.high_count + scan.medium_count + scan.low_count


class TestVendor:
    def test_create_vendor(self, db):
        vendor = Vendor(
            name='CloudFlare Inc.',
            service_description='CDN and DDoS protection',
            risk_rating='Low',
            questionnaire_status='Approved',
            contact_name='John Doe',
            contact_email='john@cloudflare.com'
        )
        db.session.add(vendor)
        db.session.commit()

        saved = Vendor.query.filter_by(name='CloudFlare Inc.').first()
        assert saved is not None
        assert saved.risk_rating == 'Low'
        assert saved.questionnaire_status == 'Approved'

    def test_vendor_default_values(self, db):
        vendor = Vendor(name='Test Vendor')
        db.session.add(vendor)
        db.session.commit()

        assert vendor.risk_rating == 'Not Assessed'
        assert vendor.questionnaire_status == 'Not Sent'