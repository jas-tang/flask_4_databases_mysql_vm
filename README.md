# flask_4_databases_mysql_vm
This is a repository for Assignment 4b in HHA504. 

# MySQL Setup on Azure VM

I initially set up the VM server on Azure with minimal settings to lower cost. If I have time, I will try replicating this in GCP. The following is what it looks like.
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
Then import packages.
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

I created an app.py file. I followed this [link](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application#step-2-setting-up-the-database-and-model) as a guideline. 
```
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI using PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jason:jason2023@172.174.249.223:3306/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

class Patients(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    MRN = db.Column(db.String(50), nullable=False)

class Demographics(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    patients = Patients.query.all()
    demographics = Demographics.query.all()
    return render_template('index.html', patients=patients, demographics=demographics)

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
```
Some highlights: 
* Imported flask packages
* Imported SQLAlchemy
* Using ```Flask(__name___)``` created a flask application, assigning it to app.
* Used app.config and set it to my Azure VM server
* Initialized the SQLAlchemy instance
* Created two classes, one for each table
* Created an index.html to connect

Index.HTML: 
```
<!DOCTYPE html>
<html>
<head>
    <title>Flask mySQL SqlAlchemy</title>
  
</head>
<!-- Tailwind CSS via CDN -->
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>

<body class="bg-gray-200">

<header class="bg-red-600 text-white p-4">
    <h1 class="text-2xl">Flask with sqlAlchemy and mySQL on Azure</h1>
</header>

<table class="border-collapse border border-gray-400">
    <thead>
        <tr>
            <th class="border border-gray-400 p-2">Patient ID</th>
            <th class="border border-gray-400 p-2">MRN</th>
            <th class="border border-gray-400 p-2">First Name</th>
            <th class="border border-gray-400 p-2">Last Name</th>
            <th class="border border-gray-400 p-2">Date of Birth</th>
            <th class="border border-gray-400 p-2">Address</th>
            <th class="border border-gray-400 p-2">Phone Number</th>
            <th class="border border-gray-400 p-2">Email</th>
        </tr>
    </thead>
    <tbody>
        {% for patient in patients %}
            <tr>
                <td class="border border-gray-400 p-2">{{ patient.patient_id }}</td>
                <td class="border border-gray-400 p-2">{{ patient.MRN }}</td>
                {% for demographic in demographics %}
                    <td class="border border-gray-400 p-2">{{ demographic.first_name }}</td>
                    <td class="border border-gray-400 p-2">{{ demographic.last_name }}</td>
                    <td class="border border-gray-400 p-2">{{ demographic.date_of_birth }}</td>
                    <td class="border border-gray-400 p-2">{{ demographic.address }}</td>
                    <td class="border border-gray-400 p-2">{{ demographic.phone_number }}</td>
                    <td class="border border-gray-400 p-2">{{ demographic.email }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
</table>


<footer class="bg-red-600 text-white p-4 mt-6">
    <p>Check <a href="https://github.com/jas-tang/flask_4_databases_mysql_vm">Github</a> for more information</p>
</footer>

<style>
    a:link {
      color: green;
      background-color: transparent;
      text-decoration: none;
    }
    a:visited {
      color: pink;
      background-color: transparent;
      text-decoration: none;
    }
    a:hover {
      color: red;
      background-color: transparent;
      text-decoration: underline;
    }
    a:active {
      color: yellow;
      background-color: transparent;
      text-decoration: underline;
    }
    </style>

</body>
</html>
```
I added additional customizations, like separating the data in boxes. I also linked my github as a link as well. 
This is the result: 
![](https://github.com/jas-tang/flask_4_databases_mysql_vm/blob/main/images/flask.JPG)

If I have time, I will try deploying this as a Flask Application. 
