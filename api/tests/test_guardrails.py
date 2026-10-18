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


def test_refusal_detection_is_conservative():
    assert g.looks_like_refusal(g.EMPTY_CONTEXT_REPLY)
    assert g.looks_like_refusal("I don't have any information about that topic.")
    long_answer = "I don't have details on X, but here is what I built. " + "word " * 120
    assert not g.looks_like_refusal(long_answer)
    assert not g.looks_like_refusal("At WPP Media I built an audience platform.")


def test_choreograph_normalized_to_wpp_media():
    assert g.normalize_company_names("the Choreograph Data team") == "the WPP Media Data team"
    assert g.normalize_company_names("no change here") == "no change here"
