/* Leads email */
CREATE VIEW LeadEmails AS
SELECT Email
FROM Client
WHERE Role = 'Lead';

/*No commerce emails*/
CREATE VIEW ManagerEmails AS
SELECT Email
FROM Client
WHERE Role = 'Manager';

/*Client emails*/
CREATE VIEW ManagerEmails AS
SELECT Email
FROM Client
WHERE Role = 'Individual';

/*Users rating*/
CREATE OR REPLACE VIEW client_ranking_view AS
SELECT 
    client.clientid,
    client.name,
    client.surname,

    RANK() OVER (ORDER BY COUNT(DISTINCT teamhandler.teamid) DESC) AS team_rank,
    RANK() OVER (ORDER BY COUNT(DISTINCT projecthandler.projectid) DESC) AS project_rank,
    RANK() OVER (ORDER BY COUNT(DISTINCT undertask.undertaskid) DESC) AS undertask_rank,
    RANK() OVER (ORDER BY COUNT(DISTINCT event.eventid) DESC) AS events_rank

FROM client
LEFT JOIN teamhandler ON client.clientid = teamhandler.clientid
LEFT JOIN projecthandler ON projecthandler.teamid = teamhandler.teamid
LEFT JOIN undertask ON client.clientid = undertask.developerid
LEFT JOIN event ON client.clientid = event.authorid

GROUP BY client.clientid, client.name, client.surname;

DROP VIEW client_ranking_view;
SELECT * FROM client_ranking_view;


/*Project structure*/
CREATE OR REPLACE VIEW project_structure_hierarchy AS
WITH RECURSIVE project_structure(projectid, name, level, project_title, path) AS (
    SELECT 
        p.projectid,
        p.title::TEXT AS name,
        1 AS level,
        p.title::TEXT AS project_title,
        p.projectid::TEXT AS path
    FROM project p

    UNION ALL

    SELECT 
        child.projectid,
        child.name,
        child.level,
        parent.project_title,
        parent.path || '-' || child.id::TEXT AS path
    FROM project_structure parent
    JOIN (
        SELECT 
            t.projectid,
            t.taskid AS id,
            ('-- ' || t.title) AS name,
            2 AS level,
            t.taskid AS parent_id
        FROM task t

        UNION ALL

        SELECT 
            t.projectid,
            st.undertaskid AS id,
            ('---- ' || st.title) AS name,
            3 AS level,
            st.taskid AS parent_id
        FROM undertask st
        JOIN task t ON st.taskid = t.taskid
    ) AS child
    ON (parent.level = 1 AND child.level = 2 AND child.projectid = parent.projectid)
       OR (parent.level = 2 AND child.level = 3 AND child.parent_id::TEXT = SPLIT_PART(parent.path, '-', array_length(string_to_array(parent.path, '-'), 1)))
)