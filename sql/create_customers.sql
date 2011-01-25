CREATE TABLE IF NOT EXISTS customers (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	membernum NUMERIC DEFAULT NULL UNIQUE,
	name TEXT NOT NULL,
	lastname TEXT NOT NULL,
	birthdate DATE NOT NULL,
	birthplace TEXT NOT NULL,
	birthprovince TEXT NOT NULL,
	address TEXT NOT NULL,
	city TEXT NOT NULL,
	province TEXT NOT NULL,
	activity TEXT NOT NULL,
	membershiptype TEXT NOT NULL,
	membershipyear TEXT NOT NULL,
	telephone TEXT DEFAULT NULL,
	mobile TEXT DEFAULT NULL,
	email TEXT DEFAULT NULL,
	certificatedate DATE DEFAULT NULL
);
