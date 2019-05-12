



To run this script:

Two ways:

python log_analysis.py

or 

./log_analysis 


Design

This program is compose of the main program and three functions.  
The main program connects to the database, get the cursor object from the connection.  Call three functions in sequence and passed the cursor objec to the function.
The three functions execute the SQL statement display the result.



Below is the view definition used by query 2:

create view v_author_articles_access as 
SELECT au.name,art.title,art.slug,l.method,l.status,l.id
from articles art join authors au on art.author = au.id
left join log l on substring(l.path,10)=art.slug
where l.id is not null