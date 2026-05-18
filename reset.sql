-- Wipes all rows from the taskcli tables and resets their id sequences.
-- Run in the Supabase SQL editor. Schema (tables, enum, indexes) is preserved.

truncate table tasks, projects restart identity cascade;
