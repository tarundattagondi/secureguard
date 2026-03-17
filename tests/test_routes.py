class TestDashboard:
    def test_dashboard_loads(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Security Compliance Dashboard' in response.data

    def test_dashboard_shows_compliance_score(self, client):
        response = client.get('/')
        assert b'COMPLIANCE SCORE' in response.data

    def test_dashboard_shows_open_risks(self, client):
        response = client.get('/')
        assert b'OPEN RISKS' in response.data

    def test_dashboard_shows_scan_info(self, client):
        response = client.get('/')
        assert b'LAST SCAN' in response.data

    def test_dashboard_shows_vendors(self, client):
        response = client.get('/')
        assert b'VENDORS' in response.data


class TestControls:
    def test_controls_page_loads(self, client):
        response = client.get('/controls/')
        assert response.status_code == 200
        assert b'Compliance Controls' in response.data

    def test_controls_filter_by_status(self, client):
        response = client.get('/controls/?status=Implemented')
        assert response.status_code == 200

    def test_controls_filter_by_framework(self, client):
        response = client.get('/controls/?framework=NIST CSF')
        assert response.status_code == 200

    def test_update_control_status(self, client, db):
        from app.models import ComplianceControl
        control = ComplianceControl(
            control_id='TEST-1',
            framework='NIST CSF',
            category='Identify',
            subcategory='Test',
            description='Test control',
            status='Not Implemented'
        )
        db.session.add(control)
        db.session.commit()

        response = client.post(f'/controls/{control.id}/update', data={
            'status': 'Implemented',
            'owner': 'Security Team',
            'evidence_link': 'http://example.com'
        }, follow_redirects=True)
        assert response.status_code == 200

        updated = ComplianceControl.query.get(control.id)
        assert updated.status == 'Implemented'


class TestRisks:
    def test_risks_page_loads(self, client):
        response = client.get('/risks/')
        assert response.status_code == 200
        assert b'Risk Register' in response.data

    def test_add_risk(self, client, db):
        response = client.post('/risks/add', data={
            'title': 'Test Risk',
            'description': 'This is a test risk',
            'likelihood': '4',
            'impact': '3',
            'status': 'Open',
            'mitigation_plan': 'Fix it',
            'owner': 'Security Team',
            'related_control': 'PR.AC-1'
        }, follow_redirects=True)
        assert response.status_code == 200

        from app.models import Risk
        risk = Risk.query.filter_by(title='Test Risk').first()
        assert risk is not None
        assert risk.risk_score == 12
        assert risk.owner == 'Security Team'

    def test_risks_filter_by_status(self, client):
        response = client.get('/risks/?status=Open')
        assert response.status_code == 200

    def test_add_risk_calculates_score(self, client, db):
        client.post('/risks/add', data={
            'title': 'Score Test',
            'description': 'Testing score calculation',
            'likelihood': '5',
            'impact': '5',
            'status': 'Open',
            'owner': 'Test'
        }, follow_redirects=True)

        from app.models import Risk
        risk = Risk.query.filter_by(title='Score Test').first()
        assert risk.risk_score == 25


class TestScans:
    def test_scans_page_loads(self, client):
        response = client.get('/scans/')
        assert response.status_code == 200
        assert b'Security Scan Results' in response.data

    def test_scans_empty_state(self, client):
        response = client.get('/scans/')
        assert response.status_code == 200