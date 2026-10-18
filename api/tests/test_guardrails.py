from portfolio_api import guardrails as g


def test_em_dashes_stripped():
    assert "\u2014" not in g.strip_em_dashes("a \u2014 b")


def test_secret_redaction():
    assert "sk-" not in g.redact_secrets("key sk-" + "A" * 30)


def test_jd_detector_needs_length_and_signals():
    assert not g.looks_like_job_description("What are the requirements you will meet?")
    jd = ("We are looking for an engineer. Responsibilities include building models. "
          "Qualifications: 5 years of experience. " * 4)
    assert g.looks_like_job_description(jd)
