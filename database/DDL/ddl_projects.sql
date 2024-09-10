CREATE TABLE projects
(
    project_id serial PRIMARY KEY,
    name varchar(254) NOT NULL,
    customer varchar(254),
    manager int8 REFERENCES users (user_id) ON DELETE CASCADE,
    owner int8 REFERENCES users (user_id) ON DELETE CASCADE,
    type varchar(254),
    adress varchar(254),
    status varchar(254),
    start_date timestamp,
    end_date timestamp,
    creation_date timestamp default now()
)