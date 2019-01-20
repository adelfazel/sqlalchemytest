CREATE TABLE bookreviews(
username VARCHAR (50) REFERENCES account(username),
isbn VARCHAR (15) REFERENCES books(isbn),
comment varchar (5000) not NULL,
stars smallint not NULL,
created_on TIMESTAMP NOT NULL,
CONSTRAINT username_isbn PRIMARY KEY (username,isbn)
);

CREATE TABLE account(
 username VARCHAR (50)  PRIMARY KEY,
 email VARCHAR (355) UNIQUE NOT NULL,
 password VARCHAR (40) NOT NULL,
 created_on TIMESTAMP NOT NULL,
 last_login TIMESTAMP
);

CREATE TABLE books (
isbn VARCHAR (15) PRIMARY KEY,
title VARCHAR (400) NOT NULL,
author VARCHAR (400) NOT NULL,
year INTEGER NOT NULL
);
