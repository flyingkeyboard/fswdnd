#!/usr/bin/python3

import psycopg2
import pandas as pd
from datetime import datetime

def get_data(cur,sql):
    cur.execute(sql)
    result=cur.fetchall()
    return (result)

def get_three_most_popular_articles(cur):
    """
    Input parameter: cursor of the database session
    Return parameter: None

    Query 1:
    What are the most popular three articles of all time
    """
    sql="""with log_detail as (select substr(path,10) path,id from log where length(path)>5) 
,art_det as (select a.title,det.id 
from log_detail det left join articles a on det.path = a.slug) 
select title,count(id) as access_count from art_det group by title order by 2 desc limit 3"""
    res=get_data(cur,sql)
    print("The result of the most popular three articles of all time:\n")
    for rw in res:
        print("\"{0}\" --- {1} views".format(rw[0],rw[1]))
    
def get_most_popular_author(cur):
    """
    Input parameter: cursor of the database session
    Return parameter: None

    Query 2:
    What are the most popular articles author of all time
    """
    sql="""select a.name ,a.count_views   from ( 
select name ,count(id) as count_views from v_author_articles_access 
group by name order by 2 desc) a"""
    res=get_data(cur,sql)
    print("The result of the most popular articles author of all time:\n")
    for rw in res:
        print("{} --- {} views".format(rw[0],rw[1]))

def get_days_with_onepc_failed(cur):


    """
    Input parameter: cursor of the database session
    Return parameter: None

    Query 3:
    On which days did more than 1% of requests lead to errors?
    """
    sql="""with day_rec as (select date_trunc('day', time) as days, status,id from log)
,total as (select days,count(id) as total from day_rec group by days),
error_total as (select days,count(id) as err_total from day_rec where status = '404 NOT FOUND' group by days ),
err_percent as (
select a.days,a.total,b.err_total,((b.err_total*1.00)/(a.total*1.00))*100.0 as percent
from 
total a join error_total b on a.days = b.DAYS)
select days ,round(percent,1) as err_txt
from err_percent 
where percent>1"""
    res=get_data(cur,sql)
    print("On which days did more than 1% of requests lead to errors:\n")
    for rw in res:
        print("{} --- {}% errors".format(datetime.strftime(rw[0],'%B %d, %Y'),rw[1]))


def main():
    conn = psycopg2.connect("dbname=news")
    cur = conn.cursor()
    get_three_most_popular_articles(cur)
    print("\n")
    get_most_popular_author(cur)
    print("\n")
    get_days_with_onepc_failed(cur)
    conn.close()
    

if __name__ == "__main__":
    main()
