#!/usr/bin/env python3

import csv
import json
import subprocess
import sys


CSV_FILE = "backlog_control_layer.csv"
PROJECT_NUMBER = "4"
OWNER = "Luchks"

FIELD_VALUE_MAP = {
    "Verification Mode": {
        "Automated Test": "Test",
        "Comparison": "Test",
        "Decision": "Inspection",
        "Manual Observation": "Inspection",
        "Physical Measurement": "Measurement",
    },
    "Ambiguity Type": {
        "Decision": "Other",
    },
    "Blocker Type": {
        "Missing Input": "Input",
        "External Decision": "Other",
    },
}


def run(cmd):
    result = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print("ERROR:", " ".join(cmd))
        print(result.stderr)
        sys.exit(result.returncode)

    return result.stdout.strip()


def gh_json(cmd):
    return json.loads(run(cmd))


def get_project_items():
    data = gh_json([
        "gh", "project", "item-list",
        PROJECT_NUMBER,
        "--owner", OWNER,
        "--format", "json",
    ])

    items = {}

    for item in data["items"]:
        title = item.get("title")
        if title:
            items[title] = item

    return items


def get_project_fields():
    data = gh_json([
        "gh", "project", "field-list",
        PROJECT_NUMBER,
        "--owner", OWNER,
        "--format", "json",
    ])

    return {
        field["name"]: field
        for field in data["fields"]
    }


def set_single_select(item_id, project_id, field, value):
    options = {
        option["name"]: option["id"]
        for option in field["options"]
    }

    field_name = field["name"]
    original_value = value
    mapped_value = FIELD_VALUE_MAP.get(field_name, {}).get(
        original_value,
        original_value,
    )

    if mapped_value != original_value:
        print(
            f"{field_name} → {original_value} "
            f"(Project: {mapped_value})"
        )

    if mapped_value not in options:
        print(
            f"AVISO: valor desconocido para "
            f"{field_name}: {original_value!r}"
        )
        return

    run([
        "gh", "project", "item-edit",
        "--id", item_id,
        "--project-id", project_id,
        "--field-id", field["id"],
        "--single-select-option-id", options[mapped_value],
    ])


def main():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"CSV: {CSV_FILE}")
    print(f"Filas: {len(rows)}")
    print(f"Project: #{PROJECT_NUMBER}")
    print()

    project = gh_json([
        "gh", "project", "view",
        PROJECT_NUMBER,
        "--owner", OWNER,
        "--format", "json",
    ])

    project_id = project["id"]

    fields = get_project_fields()
    items = get_project_items()

    field_names = [
        "Spike",
        "Platform",
        "Conditional",
        "Ambiguity Type",
        "Ambiguity Status",
        "Evidence State",
        "Verification Mode",
        "Blocker Type",
    ]

    for name in field_names:
        if name not in fields:
            print(f"ERROR: falta el campo Project: {name}")
            sys.exit(1)

    for index, row in enumerate(rows, start=1):
        backlog_id = row["Backlog ID"]
        title = f'{backlog_id} — {row["Title"]}'

        print("=" * 70)
        print(f"[{index}/{len(rows)}] {title}")

        item = items.get(title)

        if not item:
            print("ERROR: no existe Project item para este Issue.")
            print(f"       {title}")
            sys.exit(1)

        item_id = item["id"]

        values = {
            "Spike": row["Spike"].strip(),
            "Platform": row["Platform"].strip(),
            "Conditional": row["Conditional (Y/N)"].strip(),
            "Ambiguity Type": row["Ambiguity Type"].strip(),
            "Ambiguity Status": row["Ambiguity Status"].strip(),
            "Evidence State": row["Evidence State"].strip(),
            "Verification Mode": row["Verification Mode"].strip(),
            "Blocker Type": row["Blocker Type"].strip(),
        }

        for field_name, value in values.items():
            print(f"{field_name} → {value}")

            set_single_select(
                item_id,
                project_id,
                fields[field_name],
                value,
            )

        print("OK.")

    print()
    print("Sincronización terminada.")


if __name__ == "__main__":
    main()
