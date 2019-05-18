
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

### How to setup the Pythyon environment

**perform the following pip install**

pip3 install psycopg2

### How to setup the database

Ensure a Postgres database called 'news' is created before running steps below:

Download the newdata.sql in 

https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip


Use the psql command to create the three required tables:

psql -d news -f newsdata.sql

**Here's what this command does**

psql — the PostgreSQL command line program
-d news — connect to the database named news 
-f newsdata.sql — run the SQL statements in the file newsdata.sql



### Database Tables Definition

The schema consists of three tables:

The **authors** table includes information about the authors of articles.

                         Table "public.authors"
 Column |  Type   |                      Modifiers                       
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    | 
 id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)




The **articles** table includes the articles themselves.

                                  Table "public.articles"
 Column |           Type           |                       Modifiers                       
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     | 
 body   | text                     | 
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)
Indexes:
    "articles_pkey" PRIMARY KEY, btree (id)
    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

The **log** table includes one entry for each time a user has accessed the site.


                                  Table "log"
 Column |           Type           |                    Modifiers                     
--------+--------------------------+--------------------------------------------------
 path   | text                     | 
 ip     | inet                     | 
 method | text                     | 
 status | text                     | 
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)



### Design

This program is compose of the main program and three functions:

The main program connects to the database, get the cursor object from the connection object.  Call each of the three functions in sequence by passing in the cursor object to the function.

When each function is called, it calls the execute function in the cursor object to run the supplied SQL statement.  Once the query result is received, it loops through the result and display the output using the approriate string formatter for all columns.



### How to run the log analysis process

**Running the script**

To run this script and pipe results to the output.txt

Two ways:

python3 log_analysis.py > output.txt

or 

./log_analysis > output.txt



### Database View


Below is the view definition used by query 2:

create view v_author_articles_access as 
SELECT au.name,art.title,art.slug,l.method,l.status,l.id
from articles art join authors au on art.author = au.id
join log l on l.path = CONCAT('/article/', art.slug) 
 