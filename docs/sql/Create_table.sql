
/* DOMAIN: PRIORITY */
	CREATE DOMAIN Priority CHAR(7)
		CONSTRAINT ValitPriority
		CHECK(VALUE IN('Extreme','High','Average','Low'));

/* DOMAIN: STATUS */	
	CREATE DOMAIN Status CHAR(9)
		CONSTRAINT ValitStatus
		CHECK(VALUE IN('Active','Freezed','Completed','Failed','Canceled'));

/* Table: Client (IdКористувача, Ім'я, Прізвище, Роль, Електронна пошта, Зображення профілю) */
	CREATE TABLE	Client
		(ClientId	BIGSERIAL	PRIMARY KEY,
		Name	CHAR(30)	NOT NULL,
		Surname	CHAR(30)	NOT NULL,
		Email	CHAR(64)	CHECK(Email SIMILAR TO '%[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}%') UNIQUE NOT NULL,
		Avatar	CHAR(2048)	DEFAULT('idle.png') NOT NULL,
		Role	CHAR(30)	CHECK(Role IN ('No Comerce', 'Developer', 'Manager', 'Lead')) NOT NULL);
/*([a-z0-9]{6,}@[a-z]{3,}.[a-z]{2,}(.[a-z]{2,}%){0,1}){0,64}*/

/* Table: Message (IdПовідомлення, IdВідправника, IdОтримувача, Назва, Текст, Дата створення,
Посилання на маедіафайли) */
	CREATE TABLE	Message
		(MessageId	BIGSERIAL	PRIMARY KEY,
		SenderId		BIGSERIAL	REFERENCES Client(ClientId) ON DELETE NO ACTION,
		ReceiverId	BIGSERIAL	REFERENCES Client(ClientId) ON DELETE NO ACTION,
		Title		CHAR(30)	NOT NULL,
		Text		VARCHAR(500)	NOT NULL,
		Date		TIMESTAMP		NOT NULL);

/* Table: Event (IdЗаходу, Пріоритет, IdОрганізатора, Тема, Дата, Тривалість,
Посилання на маедіафайли, Опис) */
	CREATE TABLE	Event
		(EventId		BIGSERIAL	PRIMARY KEY,
		Priority		Priority		NOT NULL,
		AuthorId		BIGSERIAL	REFERENCES Client(ClientId) ON DELETE NO ACTION,
		Theme		CHAR(30)	NOT NULL,
		Description	VARCHAR(1500)	NOT NULL,
		Date		TIMESTAMP		NOT NULL,
		Duration		INTERVAL	NOT NULL,
		Link 	VARCHAR(2048)	NOT NULL);

/* Table: MediaLink( Посилання, IdАвтору, Назва) */
	CREATE TABLE	MediaLink
		(MediaLinkId		BIGSERIAL		PRIMARY KEY,
		AuthorId		BIGSERIAL	REFERENCES Client(ClientId)ON DELETE NO ACTION,
		Title		CHAR(96)	NOT NULL);

/* Table: EventHandler (IdЗаходу, IdУчасника) */
	CREATE TABLE	EventHandler
		(EventId		BIGSERIAL	REFERENCES Event(EventId) ON DELETE CASCADE,
		ClientId		BIGSERIAL	REFERENCES Client(ClientId) ON DELETE CASCADE,
		PRIMARY KEY(EventId, ClientId));

/* Table: Project (IdПроекту, IdЗавдання, Назва, Посилання на медіафайли, Статус) */
	CREATE TABLE	Project
		(ProjectId	BIGSERIAL	PRIMARY KEY,
		Title	CHAR(30)	NOT NULL,
		Status		Status		NOT NULL,
		CreationDate	DATE		NOT NULL,
		Deadline		DATE		NOT NULL);

/* Table: Task (IdЗавдання, IdПідзавдання, Пріоритет, Назва, Опис, Дата створення, Дедлайн, 
Посилання на медіафайли, Статус) */
	CREATE TABLE	Task
		(TaskId		BIGSERIAL	PRIMARY KEY,
		ProjectId		BIGSERIAL	REFERENCES Project(ProjectId) ON DELETE CASCADE,
		Title		CHAR(30)	NOT NULL,
		Priority		Priority		NOT NULL,
		Description	VARCHAR(1500)	NOT NULL,
		CreationDate	DATE		NOT NULL,
		Deadline		DATE		NOT NULL,
		Status		Status		NOT NULL DEFAULT 'Active');

/* Table: UnderTask (IdПідзавдання, Назва, Опис, Дата створення, Дата завершення, 
Посилання на маедіафайли, Статус, Автор, Виконавець) */
	CREATE TABLE	UnderTask
		(UnderTaskId	BIGSERIAL	PRIMARY KEY,
		DeveloperId	BIGSERIAL	REFERENCES Client(ClientId) ON DELETE NO ACTION,
		AuthorId		BIGSERIAL	REFERENCES Client(ClientId) ON DELETE NO ACTION,
		Title		CHAR(30)	NOT NULL,
		Description	VARCHAR(1500)	NOT NULL,
		CreationDate	DATE		NOT NULL,
		CompletionDate	DATE CHECK(CompletionDate>=CreationDate or NULL),
		Status		Status		NOT NULL DEFAULT 'Active');

/* Table: UnderTaskHandler (IdЗавдання, IdПідзавдання) */
	CREATE TABLE	UnderTaskHandler
		(TaskId		BIGSERIAL	REFERENCES Task(TaskId) ON DELETE CASCADE,
		UnderTaskId		BIGSERIAL	REFERENCES UnderTask(UnderTaskId) ON DELETE CASCADE,
		PRIMARY KEY(TaskId, UnderTaskId));

/* Table: TaskHandler (IdЗавдання, IdУчасника) */
	CREATE TABLE	TaskHandler
		(TaskId		BIGSERIAL	REFERENCES Task(TaskId) ON DELETE CASCADE,
		ClientId		BIGSERIAL	REFERENCES Client(ClientId) ON DELETE CASCADE,
		PRIMARY KEY(TaskId, ClientId));

/* Table: UnderTaskMedialink (Медіапосилання, IdПідзавдання) */
	CREATE TABLE	UnderTaskMedialink
		(MediaLinkId		BIGSERIAL	REFERENCES MediaLink(MediaLinkId) ON DELETE CASCADE,
		UnderTaskId		BIGSERIAL	REFERENCES UnderTask(UnderTaskId) ON DELETE CASCADE,
		PRIMARY KEY(MediaLinkId, UnderTaskId));

/* Table: EventMedialink (IdМедіапосилання, IdЗаходу) */
	CREATE TABLE	EventMedialink
		(MediaLinkId		BIGSERIAL	REFERENCES MediaLink(MediaLinkId) ON DELETE CASCADE,
		EventId		BIGSERIAL	REFERENCES Event(EventId) ON DELETE CASCADE,
		PRIMARY KEY(MediaLinkId, EventId));

/* Table: MessageMedialink (IdМедіапосилання, IdПовідомлення) */
	CREATE TABLE	MessageMedialink
		(MediaLinkId		BIGSERIAL	REFERENCES MediaLink(MediaLinkId) ON DELETE CASCADE,
		MessageId		BIGSERIAL	REFERENCES Message(MessageId) ON DELETE CASCADE,
		PRIMARY KEY(MediaLinkId, MessageId));

/* Table: Team (IdКоманди, Назва, Опис) */
	CREATE TABLE	Team
		(TeamId	BIGSERIAL	PRIMARY KEY,
		Title	CHAR(30)	NOT NULL,
		Description	CHAR(30)	NOT NULL);

/* Table: TeamHandler (IdКоманди, IdУчасника) */
	CREATE TABLE	TeamHandler
		(TeamId		BIGSERIAL	REFERENCES Team(TeamId) ON DELETE CASCADE,
		ClientId		BIGSERIAL	REFERENCES Client(ClientId) ON DELETE CASCADE,
		PRIMARY KEY(TeamId, ClientId));

/* Table: ProjectHandler (IdКоманди, IdПроекту) */
	CREATE TABLE	ProjectHandler
		(TeamId		BIGSERIAL	REFERENCES Team(TeamId) ON DELETE CASCADE,
		ProjectId		BIGSERIAL	REFERENCES Project(ProjectId) ON DELETE CASCADE,
		PRIMARY KEY(TeamId, ProjectId));
