import random
from datetime import datetime, timedelta
from app.models import ComplianceControl, ScanResult, Risk, Vendor
from app import create_app, db
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


app = create_app()

NIST_CONTROLS = [
    # IDENTIFY
    ("ID.AM-1", "NIST CSF", "Identify", "Asset Management", "Physical devices and systems within the organization are inventoried"),
    ("ID.AM-2", "NIST CSF", "Identify", "Asset Management", "Software platforms and applications within the organization are inventoried"),
    ("ID.AM-3", "NIST CSF", "Identify", "Asset Management", "Organizational communication and data flows are mapped"),
    ("ID.AM-4", "NIST CSF", "Identify", "Asset Management", "External information systems are catalogued"),
    ("ID.AM-5", "NIST CSF", "Identify", "Asset Management", "Resources are prioritized based on their classification and business value"),
    ("ID.RA-1", "NIST CSF", "Identify", "Risk Assessment", "Asset vulnerabilities are identified and documented"),
    ("ID.RA-2", "NIST CSF", "Identify", "Risk Assessment", "Cyber threat intelligence is received from information sharing forums"),
    ("ID.RA-3", "NIST CSF", "Identify", "Risk Assessment", "Threats, both internal and external, are identified and documented"),
    ("ID.RA-4", "NIST CSF", "Identify", "Risk Assessment", "Potential business impacts and likelihoods are identified"),
    ("ID.RA-5", "NIST CSF", "Identify", "Risk Assessment", "Threats, vulnerabilities, likelihoods, and impacts are used to determine risk"),
    # PROTECT
    ("PR.AC-1", "NIST CSF", "Protect", "Access Control", "Identities and credentials are issued, managed, verified, revoked, and audited"),
    ("PR.AC-2", "NIST CSF", "Protect", "Access Control", "Physical access to assets is managed and protected"),
    ("PR.AC-3", "NIST CSF", "Protect", "Access Control", "Remote access is managed"),
    ("PR.AC-4", "NIST CSF", "Protect", "Access Control", "Access permissions and authorizations are managed with least privilege"),
    ("PR.AC-5", "NIST CSF", "Protect", "Access Control", "Network integrity is protected incorporating network segregation"),
    ("PR.AT-1", "NIST CSF", "Protect", "Awareness Training", "All users are informed and trained"),
    ("PR.DS-1", "NIST CSF", "Protect", "Data Security", "Data-at-rest is protected"),
    ("PR.DS-2", "NIST CSF", "Protect", "Data Security", "Data-in-transit is protected"),
    ("PR.DS-5", "NIST CSF", "Protect", "Data Security", "Protections against data leaks are implemented"),
    ("PR.IP-1", "NIST CSF", "Protect", "Information Protection", "Baseline configuration of IT systems is created and maintained"),
    # DETECT
    ("DE.AE-1", "NIST CSF", "Detect", "Anomalies & Events", "A baseline of network operations and expected data flows is established"),
    ("DE.AE-2", "NIST CSF", "Detect", "Anomalies & Events", "Detected events are analyzed to understand attack targets and methods"),
    ("DE.AE-3", "NIST CSF", "Detect", "Anomalies & Events", "Event data are collected and correlated from multiple sources and sensors"),
    ("DE.CM-1", "NIST CSF", "Detect", "Continuous Monitoring", "The network is monitored to detect potential cybersecurity events"),
    ("DE.CM-4", "NIST CSF", "Detect", "Continuous Monitoring", "Malicious code is detected"),
    ("DE.CM-7", "NIST CSF", "Detect", "Continuous Monitoring", "Monitoring for unauthorized personnel, connections, and devices"),
    # RESPOND
    ("RS.RP-1", "NIST CSF", "Respond", "Response Planning", "Response plan is executed during or after a cybersecurity incident"),
    ("RS.CO-1", "NIST CSF", "Respond", "Communications", "Personnel know their roles and order of operations when a response is needed"),
    ("RS.AN-1", "NIST CSF", "Respond", "Analysis", "Notifications from detection systems are investigated"),
    ("RS.MI-1", "NIST CSF", "Respond", "Mitigation", "Incidents are contained"),
    # RECOVER
    ("RC.RP-1", "NIST CSF", "Recover", "Recovery Planning", "Recovery plan is executed during or after a cybersecurity incident"),
    ("RC.IM-1", "NIST CSF", "Recover", "Improvements", "Recovery plans incorporate lessons learned"),
    ("RC.CO-1", "NIST CSF", "Recover", "Communications", "Public relations are managed"),
]

STATUSES = ['Implemented', 'Partially Implemented', 'Not Implemented', 'Not Applicable']
OWNERS = ['Security Team', 'IT Operations', 'DevOps', 'Compliance Team', 'CISO Office', 'Unassigned']

with app.app_context():
    # Create all tables
    db.create_all()

    # Skip if already seeded
    if ComplianceControl.query.count() > 0:
        print("Database already seeded, skipping...")
        exit(0)

    # Seed NIST Controls with random statuses for demo
    for ctrl in NIST_CONTROLS:
        control = ComplianceControl(
            control_id=ctrl[0],
            framework=ctrl[1],
            category=ctrl[2],
            subcategory=ctrl[3],
            description=ctrl[4],
            status=random.choice(STATUSES),
            owner=random.choice(OWNERS),
            last_reviewed=datetime.utcnow() - timedelta(days=random.randint(1, 90))
        )
        db.session.add(control)

    # Seed sample risks
    sample_risks = [
        ("Unpatched production servers", "Multiple servers running outdated OS versions with known CVEs", 4, 5, "Open", "PR.IP-1"),
        ("Weak vendor access controls", "Third-party vendor has excessive permissions to internal systems", 3, 4, "In Progress", "PR.AC-4"),
        ("Missing encryption on data-at-rest", "Customer PII stored in unencrypted database columns", 3, 5, "Open", "PR.DS-1"),
        ("No incident response drill conducted", "Team has not practiced IR plan in over 12 months", 2, 4, "Open", "RS.RP-1"),
        ("Shadow IT applications detected", "Unapproved SaaS tools found in network traffic analysis", 3, 3, "In Progress", "ID.AM-2"),
        ("Expired SSL certificates", "Two internal services running with expired TLS certificates", 4, 3, "Mitigated", "PR.DS-2"),
        ("Insufficient logging coverage", "30% of production systems lack centralized log forwarding", 3, 4, "Open", "DE.AE-3"),
    ]

    for r in sample_risks:
        risk = Risk(
            title=r[0],
            description=r[1],
            likelihood=r[2],
            impact=r[3],
            risk_score=r[2] * r[3],
            status=r[4],
            mitigation_plan=f"Remediation plan pending review for: {r[0]}",
            owner=random.choice(OWNERS),
            related_control=r[5]
        )
        db.session.add(risk)

    # Seed scan results (last 8 pipeline runs)
    for i in range(8):
        scan_date = datetime.utcnow() - timedelta(days=i * 3)
        for scan_type in ['Bandit', 'Safety', 'Trivy']:
            critical = random.randint(0, 2)
            high = random.randint(0, 5)
            medium = random.randint(1, 8)
            low = random.randint(2, 12)
            scan = ScanResult(
                scan_type=scan_type,
                scan_date=scan_date,
                critical_count=critical,
                high_count=high,
                medium_count=medium,
                low_count=low,
                total_findings=critical + high + medium + low,
                report_summary=f"{scan_type} scan completed with {critical + high + medium + low} findings",
                pipeline_run_id=f"run-{1000 + i}"
            )
            db.session.add(scan)

    # Seed vendors
    sample_vendors = [
        ("CloudFlare Inc.", "CDN and DDoS protection", "Low", "Approved", 60),
        ("Acme Analytics", "Business intelligence platform", "Medium", "In Review", 180),
        ("DataSync Corp", "Data backup and recovery", "High", "Sent", 30),
        ("SecureAuth Ltd", "SSO authentication provider", "Low", "Approved", 45),
        ("QuickPay Systems", "Payment processing", "Critical", "In Review", 90),
    ]

    for v in sample_vendors:
        vendor = Vendor(
            name=v[0],
            service_description=v[1],
            risk_rating=v[2],
            questionnaire_status=v[3],
            soc2_report_date=datetime.utcnow() - timedelta(days=v[4]),
            soc2_expiry_date=datetime.utcnow() + timedelta(days=365 - v[4]),
            contact_name=f"Contact at {v[0]}",
            contact_email=f"security@{v[0].lower().replace(' ', '').replace('.', '')}.com"
        )
        db.session.add(vendor)

    db.session.commit()

    # Print summary
    print(f"Seeded {ComplianceControl.query.count()} compliance controls")
    print(f"Seeded {Risk.query.count()} risks")
    print(f"Seeded {ScanResult.query.count()} scan results")
    print(f"Seeded {Vendor.query.count()} vendors")
    print("Database seeding complete!")
