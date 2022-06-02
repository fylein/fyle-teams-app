------------------------------------------------------------------------------
-- SCRIPTS TO REVERT THE MIGRATION CHANGES IN CASE IF REQUIRED
------------------------------------------------------------------------------

-- Script to delete a specific migration
begin;

delete 
from
    django_migrations
where
    id = <MIGRATION_ID>
;

commit;


-- Script to remove the newly added column in a table, which was added as part of migration
begin;

alter table 
    users
drop column
    fyle_org_name
;

commit;
