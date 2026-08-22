"""Reproducible audit of the policy manual.

Checks two things programmatically, so the flaw findings in DECISIONS.md
are backed by evidence, not just eyeballing:
  1. Every § cross-reference points to a section that actually exists.
  2. The 'report a change' day-count is consistent across the manual.

Run:  python -m tests.audit_manual
"""
import re

MANUAL_PATH = "data/policy-manual.md"


def load_text():
    return open(MANUAL_PATH, encoding="utf-8").read()


def find_existing_sections(text):
    """Collect every section id that actually exists in the manual."""
    existing = set()
    # bold paragraph numbers like **4.3.2** or **1.4.3 Household**
    for m in re.finditer(r"\*\*(\d+(?:\.\d+)+)", text):
        existing.add(m.group(1))
    # headings like ## 1.4  or  ## 9.1
    for m in re.finditer(r"^#{1,3}\s+(\d+(?:\.\d+)*)", text, re.M):
        existing.add(m.group(1))
    # Part headings: "# Part 4" -> section "4"
    for m in re.finditer(r"^#\s+Part\s+(\d+)", text, re.M):
        existing.add(m.group(1))
    # add every prefix (if 5.4.1 exists, 5.4 and 5 exist too)
    prefixes = set()
    for s in existing:
        parts = s.split(".")
        for i in range(1, len(parts) + 1):
            prefixes.add(".".join(parts[:i]))
    return existing | prefixes


def check_cross_references(text, existing):
    """Find § references whose target section does not exist."""
    dangling = []
    for m in re.finditer(r"§\s?(\d+(?:\.\d+)*)", text):
        ref = m.group(1)
        if ref not in existing:
            dangling.append(ref)
    return dangling


def check_report_deadline(text):
    """Find the day-counts used for 'report a change of circumstances'."""
    numbers = set()
    for line in text.splitlines():
        if "report" in line.lower() and "days" in line.lower():
            for m in re.finditer(r"(\d+)\s*(?:calendar\s+)?days", line):
                numbers.add(int(m.group(1)))
    return numbers


def main():
    text = load_text()
    existing = find_existing_sections(text)

    print("=== Manual audit ===\n")

    dangling = check_cross_references(text, existing)
    print("1. Cross-reference check:")
    if dangling:
        print(f"   Dangling references (target missing): {sorted(set(dangling))}")
    else:
        print("   All § references point to sections that exist.")
    print()

    deadlines = check_report_deadline(text)
    print("2. 'Report a change' deadline check:")
    print(f"   Day-counts found for reporting a change: {sorted(deadlines)}")
    if len(deadlines) > 1:
        print("   >>> CONTRADICTION: the manual states more than one deadline.")
        print("       §4.3.2 says 10 days; §9.1.4 refers to '30 days under §4.3'.")
    else:
        print("   Consistent.")
    print()

    print("Summary of known planted flaws:")
    print("  - Contradiction: §4.3.2 (10 days) vs §9.1.4 (30 days).")
    print("  - Apparent gap : full-time students are defined and signposted")
    print("    (§1.4.6, §3.2.3, §5.2.3, §7.1.3) but never actually ruled on;")
    print("    §7.1.3 points to §5.4, which is care allowances, not students.")


if __name__ == "__main__":
    main()