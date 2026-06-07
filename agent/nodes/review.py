# agent/nodes/review.py

import subprocess
import json
from agent.tools.llm_tools import call_llm
from agent.prompts.prompts import CODE_REVIEW_PROMPT


def review_node(state: dict) -> dict:
    print("\n[REVIEW] Running Black + Ruff + LLM review...")

    changed_files  = state.get("changed_files", [])
    git_diff       = state.get("git_diff", "")
    file_contents  = state.get("file_contents", {})   # ← safe .get(), never KeyError

    py_files = [f for f in changed_files if f.endswith(".py")]

    # ── Black ─────────────────────────────────────────────────
    black_issues = []
    for f in py_files:
        result = subprocess.run(
            ["black", "--check", "--diff", f],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            black_issues.append(f"[BLACK] {f}:\n{result.stdout[:300]}")
    print(f"[REVIEW] Black issues: {len(black_issues)}")

    # ── Ruff ──────────────────────────────────────────────────
    ruff_issues = []
    if py_files:
        result = subprocess.run(
            ["ruff", "check", "--output-format=json"] + py_files,
            capture_output=True, text=True
        )
        try:
            findings = json.loads(result.stdout)
            ruff_issues = [
                f"[RUFF] {d['filename']}:{d['location']['row']} "
                f"{d['code']} — {d['message']}"
                for d in findings
            ]
        except Exception:
            pass
    print(f"[REVIEW] Ruff issues: {len(ruff_issues)}")

    # ── LLM review ────────────────────────────────────────────
    llm_issues = []
    if git_diff:
        response = call_llm(
            CODE_REVIEW_PROMPT.format(
                files="\n".join(changed_files),
                diff=git_diff[:6000],   # cap to avoid token overflow
            )
        )
        raw = response.get("issues", [])
        llm_issues = [
            f"[LLM] {i.get('file','?')}:{i.get('line','?')} "
            f"[{i.get('severity','?').upper()}] {i.get('message','')}"
            for i in raw
        ]
        print(f"[REVIEW] LLM issues: {len(llm_issues)}")

    return {
        **state,
        "black_issues":      black_issues,
        "ruff_issues":       ruff_issues,
        "llm_review_issues": llm_issues,
    }