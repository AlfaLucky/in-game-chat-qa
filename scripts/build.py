"""Render the report into static HTML for GitHub Pages."""

import json
from collections import Counter
from html import escape
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "src/report.json").read_text(encoding="utf-8"))
template = (root / "src/index.template.html").read_text(encoding="utf-8")
cases = data["cases"]
groups = dict(data["groups"])
priorities = Counter(case[2] for case in cases)


def links(ids):
    return " ".join(f'<a href="#{escape(item)}">{escape(item)}</a>' for item in ids)


def cards(rows):
    return "\n".join(
        f'<article id="{identifier}" class="card"><h3><span>{identifier}</span> {escape(title)}</h3>'
        f'<p>{escape(body)}</p></article>'
        for identifier, title, body in rows
    )


def rule_cards():
    return "\n".join(
        f'<article id="{identifier}" class="card"><h3><span>{identifier}</span> {escape(title)}</h3>'
        + "".join(f"<p>{escape(paragraph)}</p>" for paragraph in body)
        + f'<div class="references">Макет {links(observations.split(", "))} '
        f'&nbsp; Вопросы {links(questions.split(", "))}</div></article>'
        for identifier, title, body, observations, questions in data["contracts"]
    )


def render_case(case):
    identifier, group, priority, title, rule_ids, setup, steps, result = case
    steps_html = "".join(f"<li>{escape(step)}</li>" for step in steps)
    return f"""
      <details class="case" id="{identifier}" data-group="{group}" data-priority="{priority}" open>
        <summary>
          <span class="case-id">{identifier}</span>
          <span class="case-title">{escape(title)}</span>
          <span class="pill {priority.lower()}">{priority}</span>
        </summary>
        <div class="case-body">
          <p class="references">Правила {links(rule_ids)}</p>
          <dl>
            <div><dt>Предусловия</dt><dd>{escape(setup)}</dd></div>
            <div><dt>Шаги</dt><dd><ol>{steps_html}</ol></dd></div>
            <div><dt>Ожидаемый результат</dt><dd>{escape(result)}</dd></div>
          </dl>
        </div>
      </details>
"""


def case_groups():
    return "\n".join(
        f'<section class="case-group" aria-labelledby="group-{key}"><h3 id="group-{key}">{escape(label)}</h3>'
        + "".join(render_case(case) for case in cases if case[1] == key)
        + "</section>"
        for key, label in groups.items()
    )


def coverage():
    return "\n".join(
        f'<tr><th scope="row"><a href="#{identifier}">{identifier}</a> · {escape(title)}</th>'
        f'<td>{links(case[0] for case in cases if identifier in case[4])}</td></tr>'
        for identifier, title, *_ in data["contracts"]
    )


rule_ids = {row[0] for row in data["contracts"]}
if len({case[0] for case in cases}) != len(cases):
    raise ValueError("Duplicate test case ID")
if rule_ids != {rule for case in cases for rule in case[4]}:
    raise ValueError("Rules and test case references differ")
if set(groups) != {case[1] for case in cases}:
    raise ValueError("Case groups are missing or unknown")

sections = {
    "CASE_COUNT": str(len(cases)),
    "P0_COUNT": str(priorities["P0"]),
    "CONTRACT_COUNT": str(len(rule_ids)),
    "OBSERVATIONS": cards(data["observations"]),
    "CONTRACTS": rule_cards(),
    "QUESTIONS": cards(data["questions"]),
    "GROUP_OPTIONS": "".join(f'<option value="{key}">{escape(label)}</option>' for key, label in groups.items()),
    "CASE_GROUPS": case_groups(),
    "COVERAGE": coverage(),
}
for name, html in sections.items():
    template = template.replace(f"@@{name}@@", html)
(root / "docs/index.html").write_text(template, encoding="utf-8")
