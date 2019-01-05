start transaction;
DROP TABLE if exists bookreviews;


CREATE TABLE bookreviews(
username VARCHAR (50) REFERENCES account(username),
isbn VARCHAR (15) REFERENCES books(isbn),
comment varchar (5000) not NULL,
stars smallint not NULL,
created_on TIMESTAMP NOT NULL,
CONSTRAINT username_isbn PRIMARY KEY (username,isbn)

);
commit;
