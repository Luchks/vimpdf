#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys


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
        print(result.stderr.strip())
        sys.exit(result.returncode)

    return result.stdout.strip()


def gh_json(cmd):
    return json.loads(run(cmd))


def get_issue(number):
    return gh_json([
        "gh", "issue", "view", str(number),
        "--repo", REPO,
        "--json", "number,title,state,url,body",
    ])


def parse_issue_sections(body):
    sections = {}
    current_section = None
    current_lines = []

    for line in body.splitlines():
        if line.startswith("## "):
            if current_section is not None:
                sections[current_section] = "\n".join(
                    current_lines
                ).strip()

            current_section = line[3:].strip()
            current_lines = []
        elif current_section is not None:
            current_lines.append(line)

    if current_section is not None:
        sections[current_section] = "\n".join(
            current_lines
        ).strip()

    return sections



def get_project_items():
    data = gh_json([
        "gh", "project", "item-list",
        PROJECT_NUMBER,
        "--owner", OWNER,
        "--limit", "100",
        "--format", "json",
    ])

    return data["items"]


def get_project():
    return gh_json([
        "gh", "project", "view",
        PROJECT_NUMBER,
        "--owner", OWNER,
        "--format", "json",
    ])


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
        for option in field.get("options", [])
    }

    if value not in options:
        available = ", ".join(options)
        print(f"ERROR: valor inválido para {field['name']}: {value}")
        print(f"Valores permitidos: {available}")
        sys.exit(1)

    run([
        "gh", "project", "item-edit",
        "--id", item_id,
        "--project-id", project_id,
        "--field-id", field["id"],
        "--single-select-option-id", options[value],
    ])


def set_date(item_id, project_id, field, value):
    run(
        [
            "gh",
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            project_id,
            "--field-id",
            field["id"],
            "--date",
            value,
        ]
    )

def find_project_item(issue_number):
    for item in get_project_items():
        content = item.get("content") or {}

        if content.get("number") == issue_number:
            return item

    return None


def show_issue(issue, item, sections):
    print()
    print(f'Issue #{issue["number"]}: {issue["title"]}')
    print(f'Issue State: {issue["state"]}')
    print(f'URL: {issue["url"]}')
    print()

    print("Requirements:")
    print()

    section_order = [
        "Objective",
        "Description",
        "Checklist",
        "Acceptance",
        "Evidence",
        "Expected Result",
    ]

    for section_name in section_order:
        content = sections.get(section_name)

        if content:
            print(f"{section_name}:")
            print(content)
            print()

    print("Project:")
    print(f'  Status:            {item.get("status", "—")}')
    print(f'  Priority:          {item.get("priority", "—")}')
    print(f'  Size:              {item.get("size", "—")}')
    print(f'  Spike:             {item.get("spike", "—")}')
    print(f'  Platform:          {item.get("platform", "—")}')
    print(f'  Conditional:       {item.get("conditional", "—")}')
    print(f'  Ambiguity Type:    {item.get("ambiguity Type", "—")}')
    print(f'  Ambiguity Status:  {item.get("ambiguity Status", "—")}')
    print(f'  Evidence State:    {item.get("evidence State", "—")}')
    print(f'  Verification Mode: {item.get("verification Mode", "—")}')
    print(f'  Blocker Type:      {item.get("blocker Type", "—")}')
    print(f'  Start Date:        {item.get("start Date", "—")}')
    print(f'  End Date:          {item.get("end Date", "—")}')
    print()




def main():
    parser = argparse.ArgumentParser(
        description="Consulta y actualiza un Issue individual de vimpdf."
    )

    parser.add_argument(
        "issue",
        type=int,
        help="Número del Issue.",
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help="Muestra el estado actual del Issue y del GitHub Project.",
    )

    parser.add_argument(
        "--status",
        choices=["Todo", "In Progress", "Done"],
        help="Actualiza el campo Status del GitHub Project.",
    )

    parser.add_argument(
        "--priority",
        choices=["P0", "P1", "P2"],
        help="Actualiza Priority.",
    )

    parser.add_argument(
        "--size",
        choices=["XS", "S", "M", "L", "XL"],
        help="Actualiza Size.",
    )

    parser.add_argument(
        "--spike",
        choices=["S00.0", "S00.1", "S00.2", "S00.3"],
        help="Actualiza Spike.",
    )

    parser.add_argument(
        "--platform",
        choices=["Win+Linux", "Linux", "Windows", "Cross-platform"],
        help="Actualiza Platform.",
    )
    parser.add_argument(
        "--conditional",
        choices=["Y", "N"],
        help="Actualiza Conditional.",
    )

    parser.add_argument(
        "--ambiguity-type",
        choices=[
            "None",
            "Evidence",
            "Technical",
            "Scope",
            "Dependency",
            "Other",
        ],
        help="Actualiza Ambiguity Type.",
    )
    parser.add_argument(
        "--verification-mode",
        choices=[
            "Inspection",
            "Documentation",
            "Test",
            "Measurement",
            "Build",
            "Runtime",
        ],
        help="Actualiza Verification Mode.",
    )

    parser.add_argument(
        "--ambiguity-status",
        choices=["N/A", "Open", "Resolved"],
        help="Actualiza Ambiguity Status.",
    )

    parser.add_argument(
        "--evidence-state",
        choices=["Not Started", "Partial", "Complete", "Blocked"],
        help="Actualiza Evidence State.",
    )

    parser.add_argument(
        "--blocker-type",
        choices=[
            "None",
            "Platform",
            "Dependency",
            "Evidence",
            "Input",
            "Toolchain",
            "Other",
        ],
        help="Actualiza Blocker Type.",
    )

    parser.add_argument(
        "--start-date",
        help="Actualiza Start Date en formato YYYY-MM-DD.",
    )

    parser.add_argument(
        "--end-date",
        help="Actualiza End Date en formato YYYY-MM-DD.",
    )

    issue_state_group = parser.add_mutually_exclusive_group()

    issue_state_group.add_argument(
        "--close",
        action="store_true",
        help="Cierra el Issue en GitHub.",
    )

    issue_state_group.add_argument(
        "--reopen",
        action="store_true",
        help="Reabre el Issue en GitHub.",
    )

    args = parser.parse_args()

    issue = get_issue(args.issue)
    sections = parse_issue_sections(issue.get("body", ""))
    item = find_project_item(args.issue)

    if not item:
        print(
            f"ERROR: Issue #{args.issue} existe, "
            "pero no fue encontrado en GitHub Project."
        )
        sys.exit(1)

    requested_changes = {
        "Status": args.status,
        "Priority": args.priority,
        "Ambiguity Status": args.ambiguity_status,
        "Evidence State": args.evidence_state,
        "Blocker Type": args.blocker_type,
        "Size": args.size,
        "Spike": args.spike,
        "Platform": args.platform,
        "Conditional": args.conditional,
        "Ambiguity Type": args.ambiguity_type,
        "Verification Mode": args.verification_mode,
        "Start Date": args.start_date,
        "End Date": args.end_date,
    }

    item_keys = {
        "Status": "status",
        "Priority": "priority",
        "Ambiguity Status": "ambiguity Status",
        "Evidence State": "evidence State",
        "Blocker Type": "blocker Type",
        "Size": "size",
        "Spike": "spike",
        "Platform": "platform",
        "Conditional": "conditional",
        "Ambiguity Type": "ambiguity Type",
        "Verification Mode": "verification Mode",
        "Start Date": "start Date",
        "End Date": "end Date",
    }

    issue_state_change = None

    if args.close:
        if issue["state"] == "CLOSED":
            print("Issue ya está CLOSED. No se modifica.")
        else:
            issue_state_change = ("Issue State", issue["state"], "CLOSED")

    elif args.reopen:
        if issue["state"] == "OPEN":
            print("Issue ya está OPEN. No se modifica.")
        else:
            issue_state_change = ("Issue State", issue["state"], "OPEN")


    changes = []

    if issue_state_change:
        changes.append(issue_state_change)


    for field_name, new_value in requested_changes.items():
        if new_value is None:
            continue

        current_value = item.get(item_keys[field_name])

        if current_value == new_value:
            print(f"{field_name} ya está en {new_value}. No se modifica.")
            continue

        changes.append((field_name, current_value, new_value))

    if changes:
        print()
        print("CAMBIOS PROPUESTOS")
        print()

        for field_name, old_value, new_value in changes:
            print(f"  {field_name}: {old_value} → {new_value}")

        print()

        answer = input(
            f"¿Aplicar estos {len(changes)} cambios? [y/N]: "
        ).strip().lower()

        if answer not in ("y", "yes"):
            print("Cancelado. No se realizaron cambios.")
            sys.exit(0)

        project = get_project()
        fields = get_project_fields()


        for field_name, _, new_value in changes:
            if field_name == "Issue State":
                if new_value == "CLOSED":
                    run(
                        [
                            "gh",
                            "issue",
                            "close",
                            str(args.issue),
                            "--repo",
                            REPO,
                        ]
                    )
                else:
                    run(
                        [
                            "gh",
                            "issue",
                            "reopen",
                            str(args.issue),
                            "--repo",
                            REPO,
                        ]
                    )

                print(f"Issue State actualizado → {new_value}")
                continue


            field = fields.get(field_name)

            if not field:
                print(
                    f"ERROR: no existe el campo "
                    f"{field_name} en GitHub Project."
                )
                sys.exit(1)

            if field_name in ("Start Date", "End Date"):
                set_date(
                    item["id"],
                    project["id"],
                    field,
                    new_value,
                )
            else:
                set_single_select(
                    item["id"],
                    project["id"],
                    field,
                    new_value,
                )

            print(f"{field_name} actualizado → {new_value}")



        # Volver a consultar GitHub para verificar el resultado real.
        issue = get_issue(args.issue)
        item = find_project_item(args.issue)


    show_issue(issue, item, sections)


if __name__ == "__main__":
    main()
