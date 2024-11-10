CREATE TABLE projects_sections_structure
(
    link_id serial PRIMARY KEY,
    section_id int8 REFERENCES projects_sections (section_id) ON DELETE CASCADE,
    type varchar(50) CHECK (type IN ('job', 'head')
    position int8,
    heading_id varchar(50),
    job_id int8 REFERENCES projects_jobs (job_id) ON DELETE CASCADE
    UNIQUE (section_id, position)
    UNIQUE (heading_id)
    UNIQUE (job_id)
)