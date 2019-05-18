
### Project Name: News Website Logs Analysis Statistics ...
This project sets up a **PostgreSQL** database for a **news** website.
The provided Python script **log_analysis.py*** uses the **psycopg2** library to query 
the database and produce a report that answers the following questions:

What are the most popular three articles of all time?
What are the most popular articles author of all time?
On which days did more than 1% of requests lead to errors?

### Requirements

Below are the three software components required by this project:

- Python3
- PostgreSQL Database and client command program 'psql'
- psycopg2 library

### How to setup the database

Ensure a Postgres database called 'news' is created before running below steps:

Download the newdata.sql in 
https://classroom.udacity.com/nanodegrees/nd004/parts/51200cee-6bb3-4b55-b469-7d4dd9ad7765/modules/c57b57d4-29a8-4c5f-9bb8-5d53df3e48f4/lessons/bc938915-0f7e-4550-a48f-82241ab649e3/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91

Use the psql command to create the three required tables:

psql -d news -f newsdata.sql.
Here's what this command does:

psql — the PostgreSQL command line program
-d news — connect to the database named news 
-f newsdata.sql — run the SQL statements in the file newsdata.sql



### Database Tables Definition

The schema consists of three tables:

The **authors** table includes information about the authors of articles.
The **articles** table includes the articles themselves.
The **log** table includes one entry for each time a user has accessed the site.



### Design

This program is compose of the main program and three functions.  

**main**

The main program connects to the database, get the cursor object from the connection object.  Call each of the three functions in sequence.


**get_three_most_popular_articles function**
**get_most_popular_author function**
**get_days_with_onepc_failed function**

**
On each function call the main program passes the cursor object to the function.
The function executes the embedded SQL statement using the execute() function from the curson object.
display the result.


### How to run the log analysis process

To run this script and pipe results to the output.txt

Two ways:

python log_analysis.py > output.txt

or 

./log_analysis > output.txt



### Database View


Below is the view definition used by query 2:

create view v_author_articles_access as 
SELECT au.name,art.title,art.slug,l.method,l.status,l.id
from articles art join authors au on art.author = au.id
left join log l on substring(l.path,10)=art.slug
where l.id is not null
