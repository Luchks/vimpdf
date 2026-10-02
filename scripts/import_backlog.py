#!/usr/bin/env python3

import argparse
import csv
import json
import subprocess
import sys
import time


CSV_FILE = "backlog_control_layer.csv"
REPO = "Luchks/vimpdf"
PROJECT_NUMBER = "4"
OWNER = "Luchks"


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

    fields = {}

    for field in data["fields"]:
        fields[field["name"]] = field

    return fields


def create_issue(row):
    title = f'{row["Backlog ID"]} — {row["Title"]}'

    body = f"""## Objective

{row["Objective"]}

## Description

{row["Description"]}

## Checklist

{row["Checklist"]}

## Acceptance

{row["Acceptance"]}

## Evidence

`{row["Evidence"]}`

## Expected Result

{row["Expected Result"]}

## Backlog Metadata

| Field | Value |
|---|---|
| Backlog ID | `{row["Backlog ID"]}` |
| Spike | `{row["Spike"]}` |
| Depends On | `{row["Depends On"]}` |
| Priority | `{row["Priority"]}` |
| Size | `{row["Size"]}` |
| Platform | `{row["Platform"]}` |
| Conditional | `{row["Conditional (Y/N)"]}` |
| Blocked Reason | {row["Blocked Reason"]} |
| Status | `{row["Status"]}` |
| Ambiguity Type | `{row["Ambiguity Type"]}` |
| Ambiguity Status | `{row["Ambiguity Status"]}` |
| Evidence State | `{row["Evidence State"]}` |
| Verification Mode | `{row["Verification Mode"]}` |
| Blocker Type | `{row["Blocker Type"]}` |
"""

    result = run([
        "gh", "issue", "create",
        "--repo", REPO,
        "--title", title,
        "--body", body,
    ])

    return result


def add_to_project(issue_url):
    run([
        "gh", "project", "item-add",
        PROJECT_NUMBER,
        "--owner", OWNER,
        "--url", issue_url,
    ])


def get_item_by_title(title, retries=5, delay=1):
    for attempt in range(1, retries + 1):
        items = get_project_items()
        item = items.get(title)
        if item:
            return item
        if attempt < retries:
            print(
                f"Item aún no visible en Project "
                f"(intento {attempt}/{retries}); esperando {delay}s..."
            )
            time.sleep(delay)
    return None


def set_single_select(item_id, project_id, field_id, option_id):
    run([
        "gh", "project", "item-edit",
        "--id", item_id,
        "--project-id", project_id,
        "--field-id", field_id,
        "--single-select-option-id", option_id,
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra lo que haría sin crear Issues.",
    )
    args = parser.parse_args()

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"CSV: {CSV_FILE}")
    print(f"Filas: {len(rows)}")
    print(f"Repositorio: {REPO}")
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

    priority_field = fields.get("Priority")
    size_field = fields.get("Size")

    if not priority_field:
        print("ERROR: No existe el campo Priority.")
        sys.exit(1)

    if not size_field:
        print("ERROR: No existe el campo Size.")
        sys.exit(1)

    for index, row in enumerate(rows, start=1):
        backlog_id = row["Backlog ID"]
        title = f'{backlog_id} — {row["Title"]}'

        print("=" * 70)
        print(f"[{index}/{len(rows)}] {title}")

        existing_items = get_project_items()
        item = existing_items.get(title)

        if args.dry_run:
            if item:
                print("DRY-RUN → YA EXISTE en Project; asignaría/verificaría campos.")
            else:
                print("DRY-RUN → crearía Issue y lo añadiría al Project.")
            print(f"  Priority: {row['Priority']}")
            print(f"  Size:     {row['Size']}")
            continue

        if item:
            print("YA EXISTE en Project → Reutilizando item existente.")
        else:
            print("Creando Issue...")
            issue_url = create_issue(row)
            print(f"Issue creado: {issue_url}")

            print("Añadiendo al Project...")
            add_to_project(issue_url)

            # Volvemos a consultar con retardo e intentos
            item = get_item_by_title(title)

            if not item:
                print("ERROR: Issue creado pero no encontré su Project item.")
                sys.exit(1)

        item_id = item["id"]

        # Priority
        priority_options = {
            option["name"]: option["id"]
            for option in priority_field["options"]
        }

        priority = row["Priority"].strip()

        if priority and priority in priority_options:
            print(f"Priority → {priority}")
            set_single_select(
                item_id,
                project_id,
                priority_field["id"],
                priority_options[priority],
            )
        elif not priority:
            print("Priority → vacío; se deja sin asignar.")
        else:
            print(f"AVISO: Priority desconocida: {priority}")

        # Size
        size_options = {
            option["name"]: option["id"]
            for option in size_field["options"]
        }

        size = row["Size"].strip()

        if size and size in size_options:
            print(f"Size → {size}")
            set_single_select(
                item_id,
                project_id,
                size_field["id"],
                size_options[size],
            )
        elif not size:
            print("Size → vacío; se deja sin asignar.")
        else:
            print(f"AVISO: Size desconocido: {size}")

        print("OK.")

    print()
    print("Proceso terminado.")


if __name__ == "__main__":
    main()
