
-- Complete

CREATE OR REPLACE FUNCTION CompletingTaskTriggerExtended()
RETURNS TRIGGER AS $$
DECLARE
    media_count INTEGER;
BEGIN
    IF NEW.Status = 'Done' AND OLD.Status != 'Done' THEN
        
        SELECT COUNT(*) INTO media_count
        FROM MediaLink
        WHERE TaskId = NEW.TaskId;
        
        IF media_count = 0 AND (NEW.ResultLink IS NULL OR NEW.ResultLink = '') THEN
            RAISE EXCEPTION 'At least one media link or ResultLink is required when completing task %', NEW.TaskId;
        END IF;
        
        IF NEW.ResultLink IS NOT NULL AND NEW.ResultLink != '' THEN
            IF NOT EXISTS (
                SELECT 1 FROM MediaLink 
                WHERE TaskId = NEW.TaskId AND Url = NEW.ResultLink
            ) THEN
                INSERT INTO MediaLink (Url, Description, TaskId)
                VALUES (
                    NEW.ResultLink,
                    'Task completion result: ' || NEW.Title,
                    NEW.TaskId
                );
            END IF;
        END IF;
        
        RAISE NOTICE 'Task % (%) completed. Total media links: %', 
            NEW.TaskId, NEW.Title, media_count + 1;
            
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS completing_task_trigger ON Task;

CREATE TRIGGER completing_task_trigger
AFTER UPDATE ON Task
FOR EACH ROW
WHEN (NEW.Status = 'Done' AND OLD.Status IS DISTINCT FROM 'Done')
EXECUTE FUNCTION CompletingTaskTrigger();