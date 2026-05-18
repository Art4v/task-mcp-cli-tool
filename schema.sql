-- Run once in the Supabase SQL editor.

create table if not exists projects (
  id            bigserial primary key,
  title         text not null,
  description   text not null default '',
  start_date    date not null,
  end_date      date not null,
  no_of_stages  int  not null check (no_of_stages > 0)
);

do $$
begin
  if not exists (select 1 from pg_type where typname = 'task_status') then
    create type task_status as enum ('todo', 'in_progress', 'done');
  end if;
end$$;

create table if not exists tasks (
  id           bigserial primary key,
  project_id   bigint not null references projects(id) on delete cascade,
  title        text not null,
  description  text not null default '',
  status       task_status not null default 'todo',
  assigned_to  text not null default '',
  stage        int  not null check (stage >= 1),
  start_date   date not null,
  end_date     date not null
);

create index if not exists tasks_project_id_idx on tasks(project_id);

alter table projects disable row level security;
alter table tasks    disable row level security;
