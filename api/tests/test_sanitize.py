from portfolio_api.rag.sanitize import is_excluded, sanitize_retrieved_text


def test_excluded_topic_spellings():
    for text in (
        "built a text-to-SQL agent",
        "Text to SQL LLM agent",
        "a schema-grounded NL2SQL LLM agent",
        "NL-to-SQL assistant",
        "natural language to SQL",
    ):
        assert is_excluded(text), text


def test_unrelated_sql_is_not_excluded():
    assert not is_excluded("wrote AMC SQL to size segments")
    assert not is_excluded("compiles rule trees into Snowflake SQL")


def test_sanitize_drops_excluded_lines():
    text = "Kept line\nBuilt an NL2SQL LLM agent\nAnother kept line"
    out = sanitize_retrieved_text(text, max_chars=1000)
    assert "NL2SQL" not in out
    assert "Kept line" in out and "Another kept line" in out
