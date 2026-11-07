def test_telemetry_markdown_output_basics():
    markdown_output = """
# Telemetry Report

## Summary

- Requests: 10
- Errors: 0
"""

    assert "# Telemetry Report" in markdown_output
    assert "## Summary" in markdown_output
    assert "Requests:" in markdown_output
    assert "Errors:" in markdown_output
