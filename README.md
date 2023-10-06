# flask_4_databases_mysql_vm
This is a repository for Assignment 4b in HHA504. 

# MySQL Setup on Azure VM

I initially set up the VM server on Azure with minimal settings to lower cost. The following is what it looks like.
![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/azure1.JPG)

This is my VM server setup
![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/azure10.JPG)

It was important to add port 3306 in Azure because that is the mySQL workbench port. 

Within Google Cloud Shell, we will try installing mySQL. 
We first updated our UBUNTU (OS) Server
```
sudo apt-get update
```
Then we installed mysql-server and mysql-client
```
sudo apt install mysql-server mysql-client
```
Then we logged in with 
```
sudo mysql
```
![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/azure3.JPG)

We can then use SQL in the shell to create or show databases. I created a database named datatb amd jason. We can then show databases.
```
show databases;
```
![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/azure4.JPG)

I also created two tables: patients and demographics.
```
CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    MRN VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE demographics (
    demographic_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    address TEXT,
    phone_number VARCHAR(15),
    email VARCHAR(100),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
```

Next, I created a new user for us to grant admin privleges to. 
```
create user `jason`@`%` identified by 'jason2023';
```
This created the user "jason" with the password of "jason2023". 
Then we need to grant privleges to that user.
```
grant all privleges on *.* to `jason`@`%` with grant option
```
We can see all the privleges granted with the following command.
```
mysql> select * from mysql.user \G
```
![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/azure5.JPG)

Then we need to update mySQL configuration settings to enable external connections. We need to edit the mysql.cnf file using nano.
```
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```
We then had to change the bind address to 0.0.0.0. This will allow all external connections. Presess CTRL + O to save and CTRL + X to exit.
Restart mySQL with 
```
/etc/init.d/mysql restart
```
We can now try connecting to mySQL Workshop to this VM server.
* We set user to our host to our IP address.
* We set user to our username created that granted all privleges. For my case it is jason.
* We set our passsword to the password that associated with that user. For my case, it was jason2023.

It connected sucessfully. 

![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/azure6.JPG)

We can see both tables I created within Google Shell on mySQL Workbench. 
I decided to insert some dummy data into the tables. I only inserted one datatype for each column. 

![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/azure8.JPG)
![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/azure9.JPG)

I did this because I had trouble inserting data from python, more on that connection later. 
![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/error.JPG)
This occurred because I did not specify "patients" within python. Most tutorials I found online started with an empty dataframe, and then they inserted a new table with new data in the table. That way, the table is specified within python. I have an existing table, so I did not know how to insert data into an existing table when it is not specified in python. 

## Connecting SQLAlchemy to mySQL
First install sqlclient and pymysql.
```
!sudo apt-get install python3-dev default-libmysqlclient-dev
!pip install pymysql
```
Then, ininstall sqlalchemy, but specifically version 1.4. 
```
pip install sqlalchemy==1.4.46
```
Then import packeges.
```
import sqlalchemy
from sqlalchemy import create_engine
```
Now, you can connect to your sql server.
```
MYSQL_HOSTNAME = '172.174.249.223'
MYSQL_USER = 'jason'
MYSQL_PASSWORD = 'jason2023'
MYSQL_DATABASE = 'testdb'

connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
engine = create_engine(connection_string)
print (engine.table_names())
```
The reason why I pip uninstalled sqlalchemy, was because when installing sqlalchemy on google colab notebook, it defaults to SQLAlchemy version 2.0. Many engine functions are different on that version. You can see the message I got in the images.
![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/azure7.JPG)
Engine.table_names is depreciated in newer versions. You can see that I did get the connection to mySQL though. 

# Integration with Flask
