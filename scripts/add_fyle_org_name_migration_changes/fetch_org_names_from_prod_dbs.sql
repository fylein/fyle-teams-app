-- Script to take the dump of org-names for all orgs, inside both prod dbs
\copy (
    select
        id, 
        name
    from
        orgs
) to 'fyle_orgs.csv' csv header;

