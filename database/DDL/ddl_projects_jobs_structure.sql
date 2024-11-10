CREATE TABLE projects_jobs_structure
(
    link_id serial,
    job_id int8 REFERENCES projects_jobs (job_id) ON DELETE CASCADE,
    position int8,
    resources_id int8 REFERENCES projects_resources (resource_id) ON DELETE CASCADE
    UNIQUE (job_id, position)
)