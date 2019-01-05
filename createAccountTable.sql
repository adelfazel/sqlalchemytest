start transaction;
DROP TABLE if exists account;


CREATE TABLE account(
 username VARCHAR (50)  PRIMARY KEY,
 email VARCHAR (355) UNIQUE NOT NULL,
 password VARCHAR (40) NOT NULL,
 created_on TIMESTAMP NOT NULL,
 last_login TIMESTAMP
);
commit;
