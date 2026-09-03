"""House style pass over the built HTML: American English, no em dashes.

Idempotent. Run it on the site folder after any content edit:

    python tools/style_pass.py .

Proper nouns that legitimately carry British spellings (journal titles,
organization names, official programme names) are listed in KEEP and are left
alone.
"""

import os
import re
import sys

# Exact rewrites. Order matters: the longer, more specific ones come first.
REWRITES = [
    # --- em dashes -------------------------------------------------------
    # page titles: use a pipe separator
    (re.compile(r"(&mdash;|—)(\s*Alaa Khamis)"), r"|\2"),

    # research page intro
    ("business models &mdash; projects, grants and graduate supervision.",
     "business models: projects, grants, and graduate supervision."),

    # legacy sentence about the smart mobility triad
    ("smart mobility triad — technology, governance, and city planning — work together",
     "smart mobility triad (technology, governance, and city planning) work together"),

    # --- American English ------------------------------------------------
    ("Awards &amp; Honours", "Awards &amp; Honors"),
    ("Awards & Honours", "Awards & Honors"),
    ("Service &amp; Honours", "Service &amp; Honors"),
    ("no flash of the wrong colours.", "no flash of the wrong colors."),
    ("Research programme, funded projects and thesis supervision",
     "Research program, funded projects, and thesis supervision"),
    ("Awards, honours, fellowships and appointments",
     "Awards, honors, fellowships, and appointments"),
    ("MSc Thesis Defence:", "MSc Thesis Defense:"),

    # legacy typo picked up along the way
    ("Bayesian Appraoch", "Bayesian Approach"),
]

# British-looking words that must NOT be changed: they sit inside proper nouns.
KEEP = [
    # competition, journal, organization and official programme names
    "Minesweepers: Towards", "minesweepers-towards", "Engine: Towards",
    "Automation towards Global Standards",
    "Intelligent Defence Support Systems", "Defence R&D Canada",
    "Journal of Modelling",
    "Centre for Pattern Analysis", "centre-pattern-analysis",
    "International Centre for Humanitarian Demining", "Centre of Excellence",
    "Innovation Programme", "Executive Programme", "Research Partnership Programme",
    "DAAD",
]

# Crude detector used only for reporting, not for rewriting. Verb/noun forms are
# spelled out so ordinary American words (specialist, organism) are not flagged.
SUSPECT = re.compile(
    r"\bhonours?\b|\bcolours?\b|\bprogramme[s]?\b|\bcentre[s]?\b|\bdefence\b|"
    r"\bmodelling\b|\btowards\b|\bwhilst\b|\bamongst\b|\bcatalogue\b|\blicence\b|"
    r"\blabour\b|\btravelled\b|\bfulfil\b|\banalyse[sd]?\b|\bbehaviour[s]?\b|"
    r"\b(?:organis|optimis|recognis|specialis|realis|prioritis|categoris)"
    r"(?:e|es|ed|ing|ation|ations)\b", re.I)


def apply(text):
    for pattern, repl in REWRITES:
        if isinstance(pattern, str):
            text = text.replace(pattern, repl)
        else:
            text = pattern.sub(repl, text)
    return text


def report(name, text):
    issues = []
    for m in re.finditer(r"—|&mdash;", text):
        issues.append("EM DASH  ..." + text[max(0, m.start() - 50):m.end() + 45].replace("\n", " "))
    for m in SUSPECT.finditer(text):
        # collapse runs of whitespace so KEEP phrases still match across the
        # line breaks and double spaces left by the legacy markup
        window = " ".join(text[max(0, m.start() - 60):m.end() + 40].split())
        if any(k in window for k in KEEP):
            continue
        issues.append("SPELLING %-12r ...%s" % (m.group(0), window.replace("\n", " ")))
    for i in issues:
        print("   ! %s: %s" % (name, i))
    return issues


def main(root):
    names = sorted(f for f in os.listdir(root) if f.endswith(".html"))
    total_changed = total_issues = 0
    for name in names:
        path = os.path.join(root, name)
        with open(path, encoding="utf-8") as fh:
            before = fh.read()
        after = apply(before)
        if after != before:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(after)
            total_changed += 1
        issues = report(name, after)
        total_issues += len(issues)
        print("%-20s %s" % (name, "updated" if after != before else "unchanged"))
    print("\n%d file(s) updated, %d remaining issue(s)." % (total_changed, total_issues))
    return 1 if total_issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
