"""
test_prompts.py
10 test cases for the symptom summariser prompt and validator.
Run: pytest tests/test_prompts.py -v
"""

import json
import pytest
from app.validator import validate_response, SymptomSummary


def make_mock(overrides: dict) -> dict:
    base = {
        "chief_complaint": "Headache",
        "onset": "2 days ago",
        "duration": "2 days",
        "severity": 5,
        "red_flags": [],
        "triage_level": "moderate",
    }
    base.update(overrides)
    return base


# ── Validator unit tests (no API needed) ────────────────────────

def test_valid_low_triage():
    data = make_mock({"triage_level": "low", "severity": 3})
    result = validate_response(data)
    assert result.triage_level == "low"


def test_valid_high_triage_with_red_flags():
    data = make_mock({
        "triage_level": "high",
        "red_flags": ["chest pain", "left arm radiation"],
        "severity": None,
    })
    result = validate_response(data)
    assert result.triage_level == "high"
    assert len(result.red_flags) == 2


def test_null_severity_is_allowed():
    data = make_mock({"severity": None})
    result = validate_response(data)
    assert result.severity is None


def test_severity_out_of_range_raises():
    data = make_mock({"severity": 15})
    with pytest.raises(Exception):
        validate_response(data)


def test_invalid_triage_level_raises():
    data = make_mock({"triage_level": "critical"})
    with pytest.raises(Exception):
        validate_response(data)


def test_empty_red_flags_list():
    data = make_mock({"red_flags": []})
    result = validate_response(data)
    assert result.red_flags == []


def test_missing_onset_defaults_to_none():
    data = make_mock({})
    del data["onset"]
    result = validate_response(data)
    assert result.onset is None


def test_missing_duration_defaults_to_none():
    data = make_mock({})
    del data["duration"]
    result = validate_response(data)
    assert result.duration is None


def test_chief_complaint_required():
    data = make_mock({})
    del data["chief_complaint"]
    with pytest.raises(Exception):
        validate_response(data)


def test_multiple_red_flags():
    data = make_mock({
        "triage_level": "high",
        "red_flags": ["difficulty breathing", "loss of consciousness", "chest pain"],
    })
    result = validate_response(data)
    assert len(result.red_flags) == 3
