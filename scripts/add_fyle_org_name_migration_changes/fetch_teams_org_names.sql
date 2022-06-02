-- Script to take dump of all distinct fyle-org-ids from slack db
\c fyle_teams_db

\copy (
    select 
        distinct fyle_org_id
    from
        users
) to 'teams_orgs.csv' csv header;


-- Script to use the dump to fetch the corresponding org-name for all teams orgs, inside prod dbs
\c prod

create temp table teams_orgs(id varchar);

\copy teams_orgs from 'teams_orgs.csv' csv header;

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
                teams_orgs
        )
) to 'fyle_orgs.csv' csv header;
