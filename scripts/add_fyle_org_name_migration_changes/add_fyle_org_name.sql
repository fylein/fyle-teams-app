------------------------------------------------------------------------------
-- SCRIPTS TO RUN AFTER MIGRATION CHANGES HAVE BEEN APPLIED
------------------------------------------------------------------------------

-- Connect to teams db on prod

-- Script to update the 'fyle_org_name' column with respective org names
begin;

create temp table fyle_orgs(id varchar, name varchar);

-- fyle_orgs.csv contains combined orgs from both the prod dbs
\copy fyle_orgs from 'fyle_orgs.csv' csv header;

update
    users
set
    users.fyle_org_name = fyle_orgs.name
where 
    users.fyle_org_id = fyle_orgs.id
;

commit;
