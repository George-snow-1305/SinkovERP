CREATE TABLE users
(
    user_id serial PRIMARY KEY,
    name varchar(254) NOT NULL,
    role varchar(254),
    email varchar(254),
    phone_number varchar(254),
    creation_date timestamp,
    update_date timestamp,
)