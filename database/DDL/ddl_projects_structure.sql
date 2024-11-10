CREATE TABLE projects_structure
(
    link_id serial PRIMARY KEY,
    project_id int8 REFERENCES projects (project_id) ON DELETE CASCADE,
    position int,
    section_id int8 REFERENCES projects_sections (section_id) ON DELETE CASCADE
)