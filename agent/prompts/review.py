# agent/prompts/prompts.py

CODE_REVIEW_PROMPT = """
You are a senior software engineer.

Review this pull request diff and return ONLY valid JSON.

Files changed:
{files}

Diff:
{diff}

Return this exact JSON structure:
{{
  "issues": [
    {{
      "file": "filename.py",
      "line": 0,
      "severity": "high|medium|low",
      "category": "unused_import|missing_docstring|smell|validation|performance",
      "message": "description of the issue",
      "suggestion": "how to fix it"
    }}
  ],
  "summary": "one paragraph overall assessment"
}}
"""

SECURITY_REVIEW_PROMPT = """
You are a Python security expert.

Review this diff for security issues and return ONLY valid JSON.

Diff:
{diff}

Return this exact JSON structure:
{{
  "security_issues": [
    {{
      "file": "filename.py",
      "line": 0,
      "severity": "critical|high|medium|low",
      "cwe": "CWE-000",
      "message": "description of the vulnerability",
      "fix": "how to fix it"
    }}
  ]
}}
"""

AUTOFIX_PROMPT = """
You are a Python refactoring expert.

Issue to fix:
{issue}

Relevant diff:
{diff}

Return ONLY valid JSON. Do NOT change business logic.

{{
  "safe_to_apply": true,
  "description": "what was changed and why",
  "fixed_code_snippet": "the corrected Python code"
}}
"""

TESTGEN_PROMPT = """
You are a Python test engineer. Write pytest unit tests.

New or modified code:
{new_code}

Changed files:
{changed_files}

Rules:
- Use pytest
- Cover happy path, edge cases, error cases
- Use pytest.raises for exceptions
- Mock external calls with unittest.mock

Return ONLY valid JSON:
{{
  "test_code": "complete Python test file as a string",
  "covered_functions": ["function1", "function2"]
}}
"""

TESTFAIL_PROMPT = """
You are a Python debugging expert.

Pytest output:
{pytest_output}

Recent diff:
{diff}

Analyse the failures and return ONLY valid JSON:
{{
  "failing_tests": [
    {{
      "test_name": "test_name",
      "root_cause": "explanation",
      "fix_location": "source|test",
      "fix_description": "what to change"
    }}
  ],
  "suggested_fixes": ["fix 1", "fix 2"]
}}
"""

DOCS_PROMPT = """
You are a Python technical writer.

New or modified code:
{new_code}

Write Google-style docstrings for every public function and a changelog entry.

Return ONLY valid JSON:
{{
  "docstrings": {{
    "function_name": "docstring text"
  }},
  "changelog_entry": "- what changed"
}}
"""

MERGE_DECISION_PROMPT = """
You are a senior engineering lead.

Review report:
{review_report}

Severity counts:
{severity_counts}

Tests passed: {pytest_passed}
Confidence score: {confidence_score}

Return ONLY valid JSON:
{{
  "recommendation": "approve|reject",
  "reason": "one sentence explanation",
  "must_fix_before_merge": ["issue 1", "issue 2"]
}}
"""