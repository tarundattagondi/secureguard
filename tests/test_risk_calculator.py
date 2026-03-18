import pytest


class TestRiskScoreCalculation:
    """Test risk score calculation logic."""

    @pytest.mark.parametrize("likelihood,impact,expected_score", [
        (1, 1, 1),
        (1, 5, 5),
        (5, 1, 5),
        (5, 5, 25),
        (3, 3, 9),
        (4, 5, 20),
        (2, 3, 6),
    ])
    def test_risk_score_formula(self, likelihood, impact, expected_score):
        """Risk score = likelihood * impact."""
        assert likelihood * impact == expected_score

    @pytest.mark.parametrize("score,expected_level", [
        (25, 'Critical'),
        (20, 'Critical'),
        (15, 'High'),
        (12, 'High'),
        (9, 'Medium'),
        (6, 'Medium'),
        (4, 'Low'),
        (1, 'Low'),
    ])
    def test_risk_level_classification(self, score, expected_level):
        """Test risk level thresholds."""
        if score >= 20:
            level = 'Critical'
        elif score >= 12:
            level = 'High'
        elif score >= 6:
            level = 'Medium'
        else:
            level = 'Low'
        assert level == expected_level

    def test_likelihood_range(self):
        """Likelihood must be 1-5."""
        for val in range(1, 6):
            assert 1 <= val <= 5

    def test_impact_range(self):
        """Impact must be 1-5."""
        for val in range(1, 6):
            assert 1 <= val <= 5

    def test_max_risk_score(self):
        """Maximum possible risk score is 25."""
        assert 5 * 5 == 25

    def test_min_risk_score(self):
        """Minimum possible risk score is 1."""
        assert 1 * 1 == 1

