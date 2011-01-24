CREATE TABLE IF NOT EXISTS customers (
	membernum NUMERIC NOT NULL PRIMARY KEY,
	name TEXT NOT NULL,
	lastname TEXT NOT NULL,
	birthdate DATE NOT NULL,
	birthplace TEXT NOT NULL,
	birthprovince TEXT NOT NULL,
	address TEXT NOT NULL,
	province TEXT NOT NULL,
	city TEXT NOT NULL,
	activity TEXT NOT NULL,
	membertype TEXT NOT NULL,
	memberyear TEXT NOT NULL,
	telephone TEXT DEFAULT NULL,
	mobile TEXT DEFAULT NULL,
	email TEXT DEFAULT NULL,
	certificatedate DATE DEFAULT NULL
);
