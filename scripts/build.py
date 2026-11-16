"""Render both language editions of the report for GitHub Pages."""

import json
import re
from collections import Counter
from html import escape
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / "src"
template = (source / "index.template.html").read_text(encoding="utf-8")


def read_json(name):
    return json.loads((source / name).read_text(encoding="utf-8"))


def links(ids):
    return " ".join(f'<a href="#{escape(item)}">{escape(item)}</a>' for item in ids)


def cards(rows):
    return "\n".join(
        f'<article id="{identifier}" class="card"><h3><span>{identifier}</span> {escape(title)}</h3>'
        f'<p>{escape(body)}</p></article>'
        for identifier, title, body in rows
    )


def rule_cards(contracts, ui):
    return "\n".join(
        f'<article id="{identifier}" class="card"><h3><span>{identifier}</span> {escape(title)}</h3>'
        + "".join(f"<p>{escape(paragraph)}</p>" for paragraph in body)
        + f'<div class="references">{ui["MOCKUP_REFERENCE"]} {links(observations.split(", "))} '
        f'&nbsp; {ui["QUESTION_REFERENCES"]} {links(questions.split(", "))}</div></article>'
        for identifier, title, body, observations, questions in contracts
    )


def render_case(case, ui):
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
          <p class="references">{ui["RULE_REFERENCES"]} {links(rule_ids)}</p>
          <dl>
            <div><dt>{ui["PRECONDITIONS"]}</dt><dd>{escape(setup)}</dd></div>
            <div><dt>{ui["STEPS"]}</dt><dd><ol>{steps_html}</ol></dd></div>
            <div><dt>{ui["EXPECTED"]}</dt><dd>{escape(result)}</dd></div>
          </dl>
        </div>
      </details>
"""


def case_groups(groups, cases, ui):
    return "\n".join(
        f'<section class="case-group" aria-labelledby="group-{key}"><h3 id="group-{key}">{escape(label)}</h3>'
        + "".join(render_case(case, ui) for case in cases if case[1] == key)
        + "</section>"
        for key, label in groups
    )


def coverage(contracts, cases):
    return "\n".join(
        f'<tr><th scope="row"><a href="#{identifier}">{identifier}</a> · {escape(title)}</th>'
        f'<td>{links(case[0] for case in cases if identifier in case[4])}</td></tr>'
        for identifier, title, *_ in contracts
    )


def language_switch(language, urls):
    items = []
    for code, label in (("ru", "Русский"), ("en", "English")):
        if code == language:
            items.append(f'<span lang="{code}" aria-current="page" aria-label="{label}">{code.upper()}</span>')
        else:
            items.append(f'<a lang="{code}" hreflang="{code}" href="{urls[code]}" aria-label="{label}">{code.upper()}</a>')
    return "".join(items)


def localize_report(original, english):
    # IDs, group membership, priorities, and rule references are shared.
    for section, rows in original.items():
        if [row[0] for row in rows] != [row[0] for row in english[section]]:
            raise ValueError(f"IDs in report translations differ for {section}")

    contracts = [
        [identifier, title, paragraphs, *original_rule[3:]]
        for original_rule, (identifier, title, paragraphs) in zip(original["contracts"], english["contracts"])
    ]
    cases = []
    for original_case, (identifier, title, setup, steps, result) in zip(original["cases"], english["cases"]):
        _, group, priority, _, rule_ids, _, original_steps, _ = original_case
        if len(steps) != len(original_steps):
            raise ValueError(f"Step count differs for {identifier}")
        cases.append([identifier, group, priority, title, rule_ids, setup, steps, result])
    return {**english, "contracts": contracts, "cases": cases}


def render_report(language, data, messages, output, pdf_name, asset_root, urls):
    cases = data["cases"]
    groups = data["groups"]
    contracts = data["contracts"]
    priorities = Counter(case[2] for case in cases)
    ui = {key: escape(value) for key, value in messages.items()}
    ui["CASES_INTRO"] = ui["CASES_INTRO"].format(total=len(cases), p0=priorities["P0"])
    sections = {
        **ui,
        "LANG": language,
        "ASSET_ROOT": asset_root,
        "RU_URL": urls["ru"],
        "EN_URL": urls["en"],
        "LANG_SWITCH": language_switch(language, urls),
        "PDF_URL": pdf_name,
        "OBSERVATIONS": cards(data["observations"]),
        "CONTRACTS": rule_cards(contracts, ui),
        "QUESTIONS": cards(data["questions"]),
        "GROUP_OPTIONS": "".join(f'<option value="{key}">{escape(label)}</option>' for key, label in groups),
        "CASE_GROUPS": case_groups(groups, cases, ui),
        "COVERAGE": coverage(contracts, cases),
    }
    html = re.sub(r"@@([A-Z][A-Z0-9_]*)@@", lambda token: sections[token[1]], template)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")


report_ru = read_json("report.json")
report_en = localize_report(report_ru, read_json("report.en.json"))
messages = read_json("interface.json")
cases = report_ru["cases"]
rule_ids = {row[0] for row in report_ru["contracts"]}
if len({case[0] for case in cases}) != len(cases):
    raise ValueError("Duplicate test case ID")
if rule_ids != {rule for case in cases for rule in case[4]}:
    raise ValueError("Rules and test case references differ")
if {row[0] for row in report_ru["groups"]} != {case[1] for case in cases}:
    raise ValueError("Case groups are missing or unknown")

render_report(
    "ru", report_ru, messages["ru"], root / "docs/index.html",
    "in-game-chat-qa.pdf", "", {"ru": "./", "en": "en/"},
)
render_report(
    "en", report_en, messages["en"], root / "docs/en/index.html",
    "in-game-chat-qa-en.pdf", "../", {"ru": "../", "en": "./"},
)
