import sys
from datetime import date

from ..db import client
from ..models import Status


TABLE = "tasks"


def _get_project(project_id: int) -> dict:
    res = client().table("projects").select("*").eq("id", project_id).execute()
    if not res.data:
        sys.exit(f"Project #{project_id} not found")
    return res.data[0]


def _validate_stage(stage: int, project: dict) -> None:
    if stage < 1 or stage > project["no_of_stages"]:
        sys.exit(f"Stage must be 1..{project['no_of_stages']} for project #{project['id']}")


def _validate_dates(start: date, end: date) -> None:
    if end < start:
        sys.exit("end date must be on or after start date")


def _format(row: dict) -> str:
    return (
        f"[{row['status']:<11}] #{row['id']} (proj {row['project_id']}, stage {row['stage']}): {row['title']}\n"
        f"  description: {row['description']}\n"
        f"  assigned:    {row['assigned_to'] or '-'}\n"
        f"  dates:       {row['start_date']} -> {row['end_date']}"
    )


def add(args) -> None:
    project = _get_project(args.project)
    _validate_stage(args.stage, project)
    _validate_dates(args.start, args.end)

    payload = {
        "project_id": args.project,
        "title": args.title,
        "description": args.description,
        "status": args.status,
        "assigned_to": args.assigned_to,
        "stage": args.stage,
        "start_date": args.start.isoformat(),
        "end_date": args.end.isoformat(),
    }
    res = client().table(TABLE).insert(payload).execute()
    print(f"[+] Created task #{res.data[0]['id']}: {args.title}")


def list_(args) -> None:
    q = client().table(TABLE).select("*")
    if args.project is not None:
        q = q.eq("project_id", args.project)
    if args.status is not None:
        q = q.eq("status", args.status)
    res = q.order("id").execute()
    if not res.data:
        print("No tasks.")
        return
    for row in res.data:
        print(_format(row))
        print()


def show(args) -> None:
    res = client().table(TABLE).select("*").eq("id", args.id).execute()
    if not res.data:
        sys.exit(f"Task #{args.id} not found")
    print(_format(res.data[0]))


def update(args) -> None:
    existing = client().table(TABLE).select("*").eq("id", args.id).execute()
    if not existing.data:
        sys.exit(f"Task #{args.id} not found")
    current = existing.data[0]

    payload = {}
    if args.title is not None:
        payload["title"] = args.title
    if args.description is not None:
        payload["description"] = args.description
    if args.status is not None:
        payload["status"] = args.status
    if args.assigned_to is not None:
        payload["assigned_to"] = args.assigned_to
    if args.stage is not None:
        project = _get_project(current["project_id"])
        _validate_stage(args.stage, project)
        payload["stage"] = args.stage
    if args.start is not None:
        payload["start_date"] = args.start.isoformat()
    if args.end is not None:
        payload["end_date"] = args.end.isoformat()

    if not payload:
        sys.exit("Nothing to update. Provide at least one field.")

    merged = {**current, **payload}
    start = date.fromisoformat(merged["start_date"]) if isinstance(merged["start_date"], str) else merged["start_date"]
    end = date.fromisoformat(merged["end_date"]) if isinstance(merged["end_date"], str) else merged["end_date"]
    _validate_dates(start, end)

    client().table(TABLE).update(payload).eq("id", args.id).execute()
    print(f"[+] Updated task #{args.id}")


def delete(args) -> None:
    existing = client().table(TABLE).select("id").eq("id", args.id).execute()
    if not existing.data:
        sys.exit(f"Task #{args.id} not found")
    client().table(TABLE).delete().eq("id", args.id).execute()
    print(f"[-] Deleted task #{args.id}")
