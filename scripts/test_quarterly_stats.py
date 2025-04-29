import os
import sys
import requests
import json
import pandas as pd
from ojs import *
from journal import *
from test_chart import *
from quarterlyreport import *
from article import *
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook

'''
Notes:
- Note that start/end dates are currently accurate to the month only, not the day
- Note that the API can only get the top 10 articles starting from 01/01/01 (this is the earliest date it supports, and it's an issue publication date so backfiles should be fine)
- API includes all views (galley, abstract, other formats) in calculation for top 10
- Next: get the stats into excel (that's it!)
'''


def get_time_range():
   start = input("Enter the start date, using the format YYYY-MM-DD (e.g. 2023-07-01) >").strip()
   end = input("Enter the end date, using the format YYYY-MM-DD >").strip()

   start_date = datetime.datetime(int(start[:4]), int(start[5:7]),int(start[8:]))
   end_date = datetime.datetime(int(end[:4]), int(end[5:7]),int(end[8:]))

   # E.g. [['2024-09', datetime.date(2024, 9, 1)], ['2024-10', datetime.date(2024, 10, 31)]]
   return [str(start), str(end)]


if __name__ == '__main__':
   
   fname=sys.argv[1]
   journals = pd.read_csv(fname) 
   dates = get_time_range()

   stats=[]
   col_names=["journal_title","published_submissions","published_issues","abstract_views","galley_views"]
   for ind in journals.index:
      jtitle=journals["journal_title"][ind]
      jabbr=journals["journal_abbr"][ind]
      base_url=journals["base_url"][ind]
      token=journals["api_key"][ind]
      jnl=Journal(jabbr,base_url,token)
      #print(f"{jtitle},{jabbr},{base_url},{token}")
      
      current=jnl.get_issues_asof(dateEnd=f"{dates[1]}")
      #current=jnl.get_current_issue()

      articles = []
      for article in current["articles"]:
         for publication in article["publications"]:
            id = publication["submissionId"]
            current_article = Article(jnl.jabbr,jnl.base_url,jnl.token,id)
            views = current_article.get_submission_views(dateStart=f"{dates[0]}",dateEnd=f"{dates[1]}",submissionId=f"{id}")
            current_article.galley_views = views["galleyViews"]
            current_article.abstract_views = views["abstractViews"]
            current_article.title = views["publication"]["fullTitle"]["en_US"]
            #current_article = Article(jnl.jabbr,jnl.base_url,jnl.token,id,views["galleyViews"],views["abstractViews"],views["publication"]["fullTitle"]["en_US"])
            articles.append(current_article)
            #article_ids.append(publication["submissionId"])
      
      articles.sort(key=lambda x: x.galley_views, reverse=True)

      print("Most recent issue:")
      for article in articles:
         print(f"{article}")

      #Next: top 10 articles of all time

      print("\nTop 10 articles:")
      top_10 = jnl.get_top_articles()
      #print(top_10)
      top_10_articles = []
      for item in top_10['items']:
         new_article = Article(jnl.jabbr, jnl.base_url, jnl.token, item["publication"]["id"], item["galleyViews"], item["abstractViews"], item["publication"]["fullTitle"]["en_US"])
         #new_article.get_submission("29336")
         print(f"\n{new_article}")
         top_10_articles.append(new_article)
      #top_10_articles.sort(key=lambda x: x.abstract_views, reverse=True)

      chart1=nChart("../files/NEW_UAL_OJS_Report_Template_02.xlsx",f"../files/{dates[0]}_Report.xlsx")
      chart1.update_alltime(dates[0][0], dates[1][0], top_10_articles)
      chart1.save_workbook()

      chart2=nChart("../files/NEW_UAL_OJS_Report_Template_02.xlsx",f"../files/{dates[0]}_Report.xlsx")
      chart2.update_latest(articles)
      chart2.save_workbook()
