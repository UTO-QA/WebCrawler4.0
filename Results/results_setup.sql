PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS run_details (
n_run_id integer primary key autoincrement,
d_run_date date
, website text);

CREATE TABLE IF NOT EXISTS run_results (
n_res_id integer primary key autoincrement,
n_run_id integer,
v_link_url text not null,
v_status_code text,
v_comment text,
v_onPage text,
foreign key(n_run_id) references run_details(n_run_id)
);
COMMIT;
