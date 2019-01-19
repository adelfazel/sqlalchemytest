start transaction;
DROP TABLE if exists account;


CREATE TABLE account(
 username VARCHAR (50)  PRIMARY KEY,
 password VARCHAR (40) NOT NULL,
 created_on TIMESTAMP NOT NULL,
 last_login TIMESTAMP
);
commit;
