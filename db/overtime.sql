PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS records;
DROP TABLE IF EXISTS managers;
DROP TABLE IF EXISTS projects;
CREATE TABLE managers (
	work_id TEXT NOT NULL,
	password TEXT NOT NULL
);
CREATE TABLE projects (
	project_id INTEGER PRIMARY KEY AUTOINCREMENT,
	work_id TEXT NOT NULL,
	project TEXT NOT NULL
);
CREATE TABLE users (
	user_id TEXT NOT NULL,
	work_id TEXT NOT NULL,
	user_project TEXT NOT NULL
);
CREATE TABLE records (
	record_id INTEGER PRIMARY KEY AUTOINCREMENT,
	work_id TEXT NOT NULL,
	over_year INTEGER NOT NULL,
	over_month INTEGER NOT NULL,
	over_day INTEGER NOT NULL,
	over_type TEXT NOT NULL,
	time_start TEXT NOT NULL,
	time_end TEXT NOT NULL,
	time_pay TEXT NOT NULL,
	time_holiday TEXT NOT NULL,
	user_project TEXT NOT NULL
);
COMMIT;
