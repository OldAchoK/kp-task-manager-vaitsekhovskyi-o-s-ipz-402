
-- client productivity

CREATE OR REPLACE FUNCTION GetClientTasksStatistics(p_ClientId BIGINT DEFAULT NULL)
RETURNS TABLE (
    ClientId BIGINT,
    ClientName VARCHAR(30),
    ClientSurname VARCHAR(30),
    CompletedTasks BIGINT,
    FailedTasks BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.ClientId,
        c.Name,
        c.Surname,
        COUNT(CASE 
            WHEN t.Status = 'Done' AND t.Deadline >= CURRENT_DATE 
            THEN 1 
        END) AS CompletedTasks,
        COUNT(CASE 
            WHEN t.Status IN ('To Do', 'In Progress') AND t.Deadline < CURRENT_DATE 
            THEN 1 
        END) AS FailedTasks
    FROM 
        Client c
    LEFT JOIN 
        TaskHandler th ON c.ClientId = th.ClientId
    LEFT JOIN 
        Task t ON th.TaskId = t.TaskId
    WHERE 
        p_ClientId IS NULL OR c.ClientId = p_ClientId
    GROUP BY 
        c.ClientId, c.Name, c.Surname
    ORDER BY 
        c.ClientId;
END;
$$ LANGUAGE plpgsql;


-- manager productivity


CREATE OR REPLACE FUNCTION GetManagerStatisticsDetailed(p_ManagerId BIGINT DEFAULT NULL)
RETURNS TABLE (
    ManagerId BIGINT,
    ManagerName VARCHAR(30),
    ManagerSurname VARCHAR(30),
    ManagerEmail VARCHAR(64),
    CreatedUnderTasks BIGINT,
    AssignedTasks BIGINT,
    TasksInProgress BIGINT,
    TasksToDo BIGINT,
    CancelledTasks BIGINT,
    CompletedTasks BIGINT,
    OverdueTasks BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.ClientId AS ManagerId,
        c.Name AS ManagerName,
        c.Surname AS ManagerSurname,
        c.Email AS ManagerEmail,
        
        COUNT(DISTINCT ut.UnderTaskId) AS CreatedUnderTasks,
        
        COUNT(DISTINCT th.TaskId) AS AssignedTasks,
        
        COUNT(DISTINCT CASE 
            WHEN t.Status = 'In Progress' 
            THEN t.TaskId 
        END) AS TasksInProgress,
        
        COUNT(DISTINCT CASE 
            WHEN t.Status = 'To Do' 
            THEN t.TaskId 
        END) AS TasksToDo,
        
        COUNT(DISTINCT CASE 
            WHEN t.Status = 'Cancelled' 
            THEN t.TaskId 
        END) AS CancelledTasks,
        
        COUNT(DISTINCT CASE 
            WHEN t.Status = 'Done' 
            THEN t.TaskId 
        END) AS CompletedTasks,
        
        COUNT(DISTINCT CASE 
            WHEN t.Status IN ('To Do', 'In Progress') 
                AND t.Deadline < CURRENT_DATE 
            THEN t.TaskId 
        END) AS OverdueTasks
        
    FROM 
        Client c
    LEFT JOIN 
        UnderTask ut ON c.ClientId = ut.AuthorId
    LEFT JOIN 
        TaskHandler th ON c.ClientId = th.ClientId
    LEFT JOIN 
        Task t ON th.TaskId = t.TaskId
    WHERE 
        c.Role = 'Manager'
        AND (p_ManagerId IS NULL OR c.ClientId = p_ManagerId)
    GROUP BY 
        c.ClientId, c.Name, c.Surname, c.Email
    ORDER BY 
        c.ClientId;
END;
$$ LANGUAGE plpgsql;