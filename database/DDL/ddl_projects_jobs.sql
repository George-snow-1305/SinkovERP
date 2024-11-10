CREATE TABLE projects_jobs
(
    job_id serial PRIMARY KEY,
    name varchar(254) NOT NULL,
    total float,
    unit varchar(254)
)