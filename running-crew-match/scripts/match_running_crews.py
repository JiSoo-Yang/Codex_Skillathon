#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from crew_matcher import match_crews


def main() -> None:
    parser = argparse.ArgumentParser(description="Match running crews from bundled demo data.")
    parser.add_argument("--region", default="")
    parser.add_argument("--day", default="")
    parser.add_argument("--time", default="")
    parser.add_argument("--level", default="")
    parser.add_argument("--goal", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--data", default="")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    result = match_crews(
        region=args.region,
        day=args.day,
        time=args.time,
        level=args.level,
        goal=args.goal,
        notes=args.notes,
        limit=args.limit,
        data_path=args.data or None,
    )

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"mode: {result['mode']}")
    if result["assumptions"]:
        print("assumptions:")
        for item in result["assumptions"]:
            print(f"- {item}")
    print("results:")
    for entry in result["results"]:
        print(f"- {entry['name']} | {entry['area']} | {entry['schedule']}")
        print(f"  fit: {entry['level_fit']}")
        print(f"  reason: {entry['reason']}")
        print(f"  source: {entry['source_url']}")


if __name__ == "__main__":
    main()
