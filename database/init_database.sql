CREATE TABLE users
(
    user_id serial PRIMARY KEY,
    name varchar(254) NOT NULL,
    role varchar(254),
    email varchar(254),
    phone_number varchar(254),
    creation_date timestamp default now(),
    update_date timestamp default now()
);

CREATE TABLE projects_folders
(
    folder_id serial PRIMARY KEY,
    name varchar(254) NOT NULL,
    color varchar(254) NOT NULL,
    update_date timestamp default now(),
    creation_date timestamp default now()
);


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
);

CREATE TABLE projects_folders_structure
(
    link_id serial PRIMARY KEY,
    type varchar(254) NOT NULL,
    parent_folder int8 REFERENCES projects_folders (folder_id) ON DELETE CASCADE,
    child_folder int8 REFERENCES projects_folders (folder_id) ON DELETE CASCADE,
    child_project int8 REFERENCES projects (project_id) ON DELETE CASCADE,
    update_date timestamp default now(),
    creation_date timestamp default now()
);

INSERT INTO projects_folders (folder_id, name, color)
VALUES ('0', 'root', 'white');