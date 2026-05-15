import sys
from datetime import date

from ..db import client


TABLE = "projects"


def _validate_dates(start: date, end: date) -> None:
    if end < start:
        sys.exit("end date must be on or after start date")


def _format(row: dict) -> str:
    return (
        f"#{row['id']}: {row['title']}\n"
        f"  description: {row['description']}\n"
        f"  dates:       {row['start_date']} -> {row['end_date']}\n"
        f"  stages:      {row['no_of_stages']}"
    )


def add(args) -> None:
    _validate_dates(args.start, args.end)
    if args.stages < 1:
        sys.exit("--stages must be >= 1")
    payload = {
        "title": args.title,
        "description": args.description,
        "start_date": args.start.isoformat(),
        "end_date": args.end.isoformat(),
        "no_of_stages": args.stages,
    }
    res = client().table(TABLE).insert(payload).execute()
    print(f"[+] Created project #{res.data[0]['id']}: {args.title}")


def list_(args) -> None:
    res = client().table(TABLE).select("*").order("id").execute()
    if not res.data:
        print("No projects.")
        return
    for row in res.data:
        print(_format(row))
        print()


def show(args) -> None:
    res = client().table(TABLE).select("*").eq("id", args.id).execute()
    if not res.data:
        sys.exit(f"Project #{args.id} not found")
    print(_format(res.data[0]))


def update(args) -> None:
    payload = {}
    if args.title is not None:
        payload["title"] = args.title
    if args.description is not None:
        payload["description"] = args.description
    if args.start is not None:
        payload["start_date"] = args.start.isoformat()
    if args.end is not None:
        payload["end_date"] = args.end.isoformat()
    if args.stages is not None:
        if args.stages < 1:
            sys.exit("--stages must be >= 1")
        payload["no_of_stages"] = args.stages

    if not payload:
        sys.exit("Nothing to update. Provide at least one field.")

    existing = client().table(TABLE).select("*").eq("id", args.id).execute()
    if not existing.data:
        sys.exit(f"Project #{args.id} not found")

    merged = {**existing.data[0], **payload}
    start = date.fromisoformat(merged["start_date"]) if isinstance(merged["start_date"], str) else merged["start_date"]
    end = date.fromisoformat(merged["end_date"]) if isinstance(merged["end_date"], str) else merged["end_date"]
    _validate_dates(start, end)

    client().table(TABLE).update(payload).eq("id", args.id).execute()
    print(f"[+] Updated project #{args.id}")


def delete(args) -> None:
    existing = client().table(TABLE).select("id").eq("id", args.id).execute()
    if not existing.data:
        sys.exit(f"Project #{args.id} not found")
    client().table(TABLE).delete().eq("id", args.id).execute()
    print(f"[-] Deleted project #{args.id} (and its tasks)")
