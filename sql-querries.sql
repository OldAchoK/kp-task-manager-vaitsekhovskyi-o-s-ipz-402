DO $$
DECLARE role_name text;
BEGIN
    FOR role_name IN SELECT rolname FROM pg_roles WHERE rolname LIKE 'user_%' LOOP
        EXECUTE 'REASSIGN OWNED BY ' || quote_ident(role_name) || ' TO postgres';
        EXECUTE 'DROP OWNED BY ' || quote_ident(role_name);
        EXECUTE 'DROP ROLE ' || quote_ident(role_name);
    END LOOP;
END $$;

REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM "connect_user", "Individual", "Developer", "Manager", "Lead";
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM "connect_user", "Individual", "Developer", "Manager", "Lead";
REVOKE ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public FROM "connect_user", "Individual", "Developer", "Manager", "Lead";
REVOKE ALL PRIVILEGES ON SCHEMA public FROM "connect_user", "Individual", "Developer", "Manager", "Lead";
REVOKE ALL PRIVILEGES ON DATABASE team_db_name FROM "connect_user", "Individual", "Developer", "Manager", "Lead";

DROP OWNED BY "connect_user";
DROP OWNED BY "Individual";
DROP OWNED BY "Developer";
DROP OWNED BY "Manager";
DROP OWNED BY "Lead";

DROP TABLE IF EXISTS MediaLink CASCADE;
DROP TABLE IF EXISTS EventHandler CASCADE;
DROP TABLE IF EXISTS Event CASCADE;
DROP TABLE IF EXISTS Message CASCADE;
DROP TABLE IF EXISTS UnderTask CASCADE;
DROP TABLE IF EXISTS TaskHandler CASCADE;
DROP TABLE IF EXISTS Task CASCADE;
DROP TABLE IF EXISTS ProjectHandler CASCADE;
DROP TABLE IF EXISTS Project CASCADE;
DROP TABLE IF EXISTS TeamHandler CASCADE;
DROP TABLE IF EXISTS Team CASCADE;
DROP TABLE IF EXISTS Client CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;

DROP DOMAIN IF EXISTS PriorityDomain CASCADE;
DROP DOMAIN IF EXISTS StatusDomain CASCADE;

DROP ROLE IF EXISTS "connect_user";
DROP ROLE IF EXISTS "Individual";
DROP ROLE IF EXISTS "Developer";
DROP ROLE IF EXISTS "Manager";
DROP ROLE IF EXISTS "Lead";

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE DOMAIN PriorityDomain AS CHAR(7) CHECK(VALUE IN('Extreme','High','Average','Low'));
CREATE DOMAIN StatusDomain AS VARCHAR(20) CHECK(VALUE IN('To Do', 'In Progress', 'Review', 'Done', 'Canceled'));

CREATE TABLE django_session (
    session_key varchar(40) NOT NULL PRIMARY KEY,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
CREATE INDEX django_session_expire_date_idx ON django_session (expire_date);

CREATE TABLE Client (
    ClientId BIGSERIAL PRIMARY KEY,
    Name VARCHAR(30) NOT NULL,
    Surname VARCHAR(30) NOT NULL,
    Email VARCHAR(64) UNIQUE NOT NULL,
    Avatar VARCHAR(2048) DEFAULT 'idle.png' NOT NULL,
    Role VARCHAR(30) CHECK(Role IN ('No Commerce', 'Developer', 'Manager', 'Lead', 'Individual')) NOT NULL
);

CREATE TABLE Team (
    TeamId BIGSERIAL PRIMARY KEY,
    Title VARCHAR(50) NOT NULL,
    Description VARCHAR(255) NOT NULL
);

CREATE TABLE TeamHandler (
    id BIGSERIAL PRIMARY KEY,
    TeamId BIGINT REFERENCES Team(TeamId) ON DELETE CASCADE,
    ClientId BIGINT REFERENCES Client(ClientId) ON DELETE CASCADE,
    CONSTRAINT teamhandler_unique UNIQUE (TeamId, ClientId)
);

CREATE TABLE Project (
    ProjectId BIGSERIAL PRIMARY KEY,
    Title VARCHAR(50) NOT NULL,
    Status StatusDomain NOT NULL DEFAULT 'To Do',
    MediaLink VARCHAR(2048),
    CreationDate DATE NOT NULL DEFAULT CURRENT_DATE,
    Deadline DATE NOT NULL
);

CREATE TABLE ProjectHandler (
    id BIGSERIAL PRIMARY KEY,
    TeamId BIGINT REFERENCES Team(TeamId) ON DELETE CASCADE,
    ProjectId BIGINT REFERENCES Project(ProjectId) ON DELETE CASCADE,
    CONSTRAINT projecthandler_unique UNIQUE (TeamId, ProjectId)
);

CREATE TABLE Task (
    TaskId BIGSERIAL PRIMARY KEY,
    ProjectId BIGINT REFERENCES Project(ProjectId) ON DELETE CASCADE,
    Title VARCHAR(100) NOT NULL,
    Priority PriorityDomain NOT NULL,
    Description VARCHAR(1500) NOT NULL,
    CreationDate DATE NOT NULL DEFAULT CURRENT_DATE,
    Deadline DATE NOT NULL,
    Status StatusDomain NOT NULL DEFAULT 'To Do',
    ResultLink VARCHAR(2048)
);

CREATE TABLE TaskHandler (
    id BIGSERIAL PRIMARY KEY,
    TaskId BIGINT REFERENCES Task(TaskId) ON DELETE CASCADE,
    ClientId BIGINT REFERENCES Client(ClientId) ON DELETE CASCADE,
    CONSTRAINT taskhandler_unique UNIQUE (TaskId, ClientId)
);

CREATE TABLE UnderTask (
    UnderTaskId BIGSERIAL PRIMARY KEY,
    TaskId BIGINT REFERENCES Task(TaskId) ON DELETE CASCADE,
    DeveloperId BIGINT REFERENCES Client(ClientId) ON DELETE SET NULL,
    AuthorId BIGINT REFERENCES Client(ClientId) ON DELETE SET NULL,
    Title VARCHAR(100) NOT NULL,
    Description VARCHAR(1500) NOT NULL,
    CreationDate DATE NOT NULL DEFAULT CURRENT_DATE,
    CompletionDate DATE,
    Status StatusDomain NOT NULL DEFAULT 'To Do',
    ResultLink VARCHAR(2048)
);

CREATE TABLE Message (
    MessageId BIGSERIAL PRIMARY KEY,
    SenderId BIGINT REFERENCES Client(ClientId) ON DELETE CASCADE,
    ReceiverId BIGINT REFERENCES Client(ClientId) ON DELETE CASCADE,
    Title VARCHAR(100) NOT NULL,
    Text VARCHAR(1500) NOT NULL,
    Date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE Event (
    EventId BIGSERIAL PRIMARY KEY,
    Priority PriorityDomain NOT NULL,
    AuthorId BIGINT REFERENCES Client(ClientId) ON DELETE CASCADE,
    Theme VARCHAR(100) NOT NULL,
    Description VARCHAR(1500) NOT NULL,
    Date TIMESTAMP NOT NULL,
    Duration INTERVAL NOT NULL,
    Link VARCHAR(2048)
);

CREATE TABLE EventHandler (
    id BIGSERIAL PRIMARY KEY,
    EventId BIGINT REFERENCES Event(EventId) ON DELETE CASCADE,
    ClientId BIGINT REFERENCES Client(ClientId) ON DELETE CASCADE,
    CONSTRAINT eventhandler_unique UNIQUE (EventId, ClientId)
);

CREATE TABLE MediaLink (
    MediaLinkId BIGSERIAL PRIMARY KEY,
    Url VARCHAR(2048) NOT NULL,
    Description VARCHAR(255),
    TaskId BIGINT REFERENCES Task(TaskId) ON DELETE CASCADE,
    UnderTaskId BIGINT REFERENCES UnderTask(UnderTaskId) ON DELETE CASCADE,
    MessageId BIGINT REFERENCES Message(MessageId) ON DELETE CASCADE,
    EventId BIGINT REFERENCES Event(EventId) ON DELETE CASCADE
);

CREATE ROLE "connect_user" WITH LOGIN PASSWORD 'connect_pass';
ALTER ROLE "connect_user" CREATEROLE;

CREATE ROLE "Individual" NOLOGIN;
CREATE ROLE "Developer" NOLOGIN;
CREATE ROLE "Manager" NOLOGIN;
CREATE ROLE "Lead" NOLOGIN;

GRANT "Individual", "Developer", "Manager", "Lead" TO "connect_user" WITH ADMIN OPTION;

GRANT ALL ON SCHEMA public TO "connect_user";
GRANT ALL ON ALL TABLES IN SCHEMA public TO "connect_user";
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO "connect_user";

GRANT ALL ON ALL TABLES IN SCHEMA public TO "Individual", "Developer", "Manager", "Lead";
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO "Individual", "Developer", "Manager", "Lead";

INSERT INTO Client (Name, Surname, Email, Role) VALUES
('Ivan', 'Sadikov', 'dev@test.com', 'Developer'),
('Petr', 'Samuraj', 'man@test.com', 'Manager'),
('Olga', 'Levanskaya', 'lead@test.com', 'Lead'),
('Alex', 'Katsyrberg', 'client@test.com', 'Individual'),
('Mark', 'Newbie', 'mark@test.com', 'Developer');

CREATE ROLE "user_1" WITH LOGIN PASSWORD '123' IN ROLE "Developer";
GRANT "user_1" TO "connect_user";

CREATE ROLE "user_2" WITH LOGIN PASSWORD '123' IN ROLE "Manager";
GRANT "user_2" TO "connect_user";

CREATE ROLE "user_3" WITH LOGIN PASSWORD '123' IN ROLE "Lead";
GRANT "user_3" TO "connect_user";

CREATE ROLE "user_4" WITH LOGIN PASSWORD '123' IN ROLE "Individual";
GRANT "user_4" TO "connect_user";

CREATE ROLE "user_5" WITH LOGIN PASSWORD '123' IN ROLE "Developer";
GRANT "user_5" TO "connect_user";

INSERT INTO Project (Title, Status, Deadline) VALUES
('Website Redesign', 'In Progress', '2025-12-31'),
('Mobile App', 'To Do', '2026-03-15');

INSERT INTO Task (ProjectId, Title, Priority, Description, Deadline, Status) VALUES
(1, 'Fix Login', 'High', 'Bug fix', '2025-12-01', 'To Do'),
(1, 'Setup DB', 'Extreme', 'Init SQL', '2025-11-20', 'Done'),
(2, 'Design UI', 'Average', 'Create mockups', '2026-01-10', 'In Progress');

INSERT INTO TaskHandler (TaskId, ClientId) VALUES
(1, 1),
(2, 5),
(3, 1);

INSERT INTO UnderTask (TaskId, DeveloperId, AuthorId, Title, Description, Status) VALUES
(1, 1, 2, 'Update login form', 'Add validation', 'To Do'),
(1, 5, 2, 'Test login flow', 'Write unit tests', 'To Do');

INSERT INTO Message (SenderId, ReceiverId, Title, Text) VALUES
(3, 1, 'Welcome', 'Welcome to the team Ivan!'),
(2, 5, 'Task assigned', 'Please check your new task');

INSERT INTO Event (Priority, AuthorId, Theme, Description, Date, Duration) VALUES
('High', 3, 'Sprint Planning', 'Plan next sprint tasks', '2025-12-15 10:00:00', '02:00:00'),
('Average', 2, 'Code Review', 'Review recent commits', '2025-12-12 14:00:00', '01:00:00');

INSERT INTO EventHandler (EventId, ClientId) VALUES
(1, 1), (1, 2), (1, 3), (1, 5),
(2, 1), (2, 5);

