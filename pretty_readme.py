#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate Markdown tables from Beatmania IIDX Dan course dictionaries.

Expected globals (paste above or import):
  - dan_courses_sp:     dict[str, dict[str, list[str]]]  # Singles
  - dan_courses_dp:  dict[str, dict[str, list[str]]]  # Doubles

Output: README.md
"""

from collections import defaultdict
from typing import Dict, List, Tuple


from courses import dan_courses_sp, dan_courses_dp  
# -----------------------------------------------------------------------------------

# Chronological game order (used to sort table rows):
GAME_ORDER = [
    "7th style", "8th style", "9th style", "10th style",
    "11 IIDX RED", "12 HAPPY SKY", "13 DistorteD", "14 GOLD",
    "15 DJ TROOPERS", "16 EMPRESS", "17 SIRIUS", "18 Resort Anthem",
    "19 Lincle", "20 tricoro", "21 SPADA", "22 PENDUAL",
    "23 copula", "24 SINOBUZ", "25 CANNON BALLERS", "26 Rootage",
    "26 Rootage (offline)",  # special DP case
    "27 HEROIC VERSE", "28 BISTROVER", "29 CastHour", "30 RESIDENT",
    "31 EPOLIS", "32 Pinky Crush",
]

# Dan order (table sections):
DAN_ORDER = [
    "1st Dan", "2nd Dan", "3rd Dan", "4th Dan", "5th Dan",
    "6th Dan", "7th Dan", "8th Dan", "9th Dan", "10th Dan",
    "Chuuden", "Kaiden",
]

def order_games(keys: List[str]) -> List[str]:
    """Sort game keys by canonical chronology, then any unknowns alphabetically."""
    index = {name: i for i, name in enumerate(GAME_ORDER)}
    return sorted(keys, key=lambda k: (index.get(k, 10_000), k))

def max_stage_len(section: Dict[str, List[str]]) -> int:
    """Max number of stage entries across games in one Dan section."""
    m = 0
    for stages in section.values():
        m = max(m, len(stages))
    return m

def render_table_for_dan(dan_name: str, section: Dict[str, List[str]]) -> str:
    """
    Render a single Dan section to a Markdown table.
    Columns: Game | Stage 1 .. Stage N (N = max stages in this Dan).
    """
    if not section:
        return ""

    cols = max_stage_len(section)
    header = ["Game"] + [f"Stage {i}" for i in range(1, cols + 1)]
    sep    = ["---"] * (cols + 1)

    lines = []
    lines.append(f"### {dan_name}\n")
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(sep) + " |")

    for game in order_games(list(section.keys())):
        stages = section[game]
        row = [game] + stages + [""] * (cols - len(stages))
        # Escape pipes in song titles (rare, but safe)
        row = [cell.replace("|", r"\|") for cell in row]
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")  # trailing newline
    return "\n".join(lines)

def render_markdown(datasets: List[Tuple[str, Dict[str, Dict[str, List[str]]]]]) -> str:
    """
    datasets: list of (section_title, data_dict) pairs.
      data_dict shape: { dan_name: { game_name: [stages...] } }
    """
    out = []
    out.append("# Beatmania IIDX Dan Courses\n")
    for title, data in datasets:
        out.append(f"## {title}\n")
        # Iterate Dans
        known = [d for d in DAN_ORDER if d in data]
        extras = sorted([d for d in data.keys() if d not in DAN_ORDER])
        for dan_name in known + extras:
            out.append(render_table_for_dan(dan_name, data[dan_name]))
    return "\n".join(out)

def main():
    # Check presence of expected dicts
    globs = globals()
    missing = [name for name in ("dan_courses_sp", "dan_courses_dp") if name not in globs]
    if missing:
        raise SystemExit(
            "Missing dictionaries: "
            + ", ".join(missing)
            + "\nPaste your `dan_courses_sp` and `dan_courses_dp` above, "
              "or import them before running this script."
        )

    md = render_markdown([
        ("Singles Play", globals()["dan_courses_sp"]),
        ("Doubles Play", globals()["dan_courses_dp"]),
    ])

    out_path = "README.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("python 2d dictionary of all AC dan courses from 7th dan - kaiden feel free to add PR with new stuff or kyu courses I am just lazy \n")
        f.write(md)

    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
