CREATE TABLE IF NOT EXISTS reaper_results (
    project_id                integer NOT NULL,
    architecture              double precision DEFAULT NULL,
    community                 double precision DEFAULT NULL,
    continuous_integration    double precision DEFAULT NULL,
    documentation             double precision DEFAULT NULL,
    history                   double precision DEFAULT NULL,
    license                   double precision DEFAULT NULL,
    management                double precision DEFAULT NULL,
    project_size              double precision DEFAULT NULL,
    repository_size           double precision DEFAULT NULL,
    state                     varchar(255) DEFAULT NULL,
    stars                     double precision DEFAULT NULL,
    unit_test                 double precision DEFAULT NULL,
    score                     double precision DEFAULT NULL,
    PRIMARY KEY (project_id)
);
