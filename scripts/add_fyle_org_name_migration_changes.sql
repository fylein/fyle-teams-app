------------------------------------------------------------------------------
------------------------------------------------------------------------------
-- SCRIPTS TO RUN AFTER MIGRATION CHANGES HAVE BEEN APPLIED
------------------------------------------------------------------------------
------------------------------------------------------------------------------


-- Script to take dump of all distinct fyle-org-ids from slack db
\copy (
    select 
        distinct fyle_org_id
    from
        users
) to 'slack_orgs.csv' csv header;


-- Script to use the dump to fetch the corresponding org-name for all slack orgs, inside prod dbs
create temp table slack_orgs(id varchar);

\copy slack_orgs from 'slack_orgs.csv' csv header;

\copy (
    select
        id, 
        name
    from
        orgs
    where
        id in (
            select
                id
            from
                slack_orgs
        )
) to 'slack_org_names.csv' csv header;


-- Script to update the 'fyle_org_name' column with respective org names
begin;

create temp table slack_org_names(id varchar, name varchar);

\copy slack_org_names from 'slack_org_names.csv' csv header;

update
    users
set
    users.fyle_org_name = slack_org_names.name
where 
    users.fyle_org_id = slack_org_names.id
;

commit;


------------------------------------------------------------------------------
------------------------------------------------------------------------------
-- SCRIPTS TO REVERT THE ABOVE MIGRATION CHANGE IN CASE IF REQUIRED
------------------------------------------------------------------------------
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
