start transaction;
DROP TABLE if exists books;

CREATE TABLE books (
isbn VARCHAR (15) PRIMARY KEY,
title VARCHAR (400) NOT NULL,
author VARCHAR (400) NOT NULL,
year INTEGER NOT NULL
);
commit;
