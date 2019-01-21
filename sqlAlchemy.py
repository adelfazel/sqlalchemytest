from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import inspect

connectionStringTemplate="mysql+mysqldb://{0}:{1}@{2}:{3}/{4}"
connectionString  = "mysql+mysqldb://jenkins:HNs72LVa@125.213.170.68:3306/Lab_VM_MVP02_Sonar"

engine = create_engine(connectionString)
db = scoped_session(sessionmaker(bind=engine))

sampleQuery =  f"Select * from account where account_id ='1'"
sampleQuery =  f"Select * from account where account_id ='234231'"

def initilize_db(username="jenkins",password="HNs72LVa",ip="125.213.170.68",port="3306",db_name="Lab_VM_MVP02_Sonar"):
    connectionString = connectionStringTemplate.format(username,password,ip,port,db_name)
    engine = create_engine(connectionString)
    db = scoped_session(sessionmaker(bind=engine))
    return db

def exist_in_database(db, query):
    return not db.execute(query).fetchone() is None
def retrieve_single_row_from_database(db, query):
    return db.execute(query).fetchone()
def retrieve_multiple_rows(db, query):
    return db.execute(query).fetchall()

exist_in_database(db, sampleQuery) # would return True

queryContent = retrieve_single_row_from_database(db, sampleQuery)
queryContent = retrieve_multiple_rows(db, sampleQuery)


# def retrieve_single_row_from_database(query, keys, **kwargs):
#     """Connect to database and retrieve a single row of data then convert it to dict
#     :param keys:
#     :param query:
#     :param kwargs:
#     """
#     data_dict = {}
#     # Setting up the database details
#     username = kwargs.pop("username", sonar_data.database_username)
#     password = kwargs.pop("password", sonar_data.database_password)
#     ip = kwargs.pop("ip", sonar_data.database_ip)
#     database = kwargs.pop("database", sonar_data.database_name)
#     logging.debug(str(datetime.datetime.now()) + " Connecting to database: %s with username: %s and password %s" % (
#     ip + "/" + database, username,password))
#     cnx = mysql.connector.connect(user=username, password=password,
#                                   host=ip,
#                                   database=database)
#     cursor = cnx.cursor(buffered=True)
#     logging.debug(str(datetime.datetime.now()) + " Executing query: " + query)
#     cursor.execute(query)
#     cnx.close()
#     data = cursor.fetchone()
#     cursor.close()
#     for (name, value) in zip(keys, data):
#         data_dict[name] = value
#     return data_dict



# def is_exist_in_database(query, **kwargs):
#     """Connect to database and check if a particular record exist
#     :param query:
#     :param kwargs:
#     """
#     # Setting up the database details
#     username = kwargs.pop("username", sonar_data.database_username)
#     password = kwargs.pop("password", sonar_data.database_password)
#     ip = kwargs.pop("ip", sonar_data.database_ip)
#     database = kwargs.pop("database", sonar_data.database_name)
#     logging.debug(str(datetime.datetime.now()) + " Connecting to database: %s with username: %s" % (
#     ip + "/" + database, username))
#     cnx = mysql.connector.connect(user=username, password=password,
#                                   host=ip,
#                                   database=database)
#     cursor = cnx.cursor(buffered=True)
#     logging.debug(str(datetime.datetime.now()) + " Executing query: " + query)
#     cursor.execute(query)
#     cnx.close()
#     data = cursor.fetchone()
#     cursor.close()
#     if len(data) != 0:
#         logging.debug(str(datetime.datetime.now()) + " At least one record have been found within the database")
#     else:
#         logging.debug(str(datetime.datetime.now()) + " No record has been found")
#     return len(data) != 0