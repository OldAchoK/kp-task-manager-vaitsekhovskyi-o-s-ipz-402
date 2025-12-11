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