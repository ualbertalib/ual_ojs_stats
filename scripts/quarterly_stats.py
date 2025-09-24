import os
import sys
import requests
import json
import pandas as pd
from ojs import *
from journal import *
from chart import *
from quarterlyreportchart import *
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
import pprint as pp
from article import *

def get_item_title(item):
    if item["publication"]["fullTitle"]["en_US"].strip() != "":
        title=item["publication"]["fullTitle"]["en_US"]
    elif item["publication"]["fullTitle"]["fr_CA"].strip() != "":
        title=item["publication"]["fullTitle"]["fr_CA"]
    elif item["publication"]["fullTitle"]["it_IT"].strip() != "":
         title=item["publication"]["fullTitle"]["it_IT"]
    elif item["publication"]["fullTitle"]["de_DE"].strip() != "":
         title=item["publication"]["fullTitle"]["de_DE"]
    else:
         title=""

    return title


if __name__ == '__main__':
   
   # file containing a list of journals
   fname=sys.argv[1]

   # the first date of a quarter
   start_date=sys.argv[2]

   # the last date of a quarter
   end_date=sys.argv[3]

   # iStart: for a given list of journals, starting
   # from the iStart journal, skipping the one ahead
   # of iStart 
   iStart=0
   if len(sys.argv) == 5:
     iStart=int(sys.argv[4])

   #iEnd: by default iEnd=10000, kind of like infinity
   iEnd=10000
   if len(sys.argv) == 6:
    iEnd=int(sys.argv[5])

   journals = pd.read_csv(fname) 
   
   stats=[]
   col_names=["journal_title","published_submissions","published_issues","abstract_views","galley_views"]
   for ind in journals.index:
      if ind < iStart or ind > iEnd:
        continue
      articles=[]
      jtitle=journals["journal_title"][ind]
      jabbr=journals["journal_abbr"][ind]
      base_url=journals["base_url"][ind]
      token=journals["api_key"][ind]
      jnl=Journal(jabbr,base_url,token)

      print(f"journal: {jtitle},{jabbr},{base_url}")

      # get the most recent issue as constrained by 
      # the end_date.   
      #current=jnl.get_issues_asof(end_date)
      current=jnl.get_issues_asof(start_date)
      pp.pprint(current) 


      if current is None:
         continue
      for article in current["articles"]:
         for publication in article["publications"]:
            id = publication["submissionId"]
            current_article = Article(jnl.jabbr,jnl.base_url,jnl.token,id)
             
            views = current_article.get_submission_views(
                    dateStart=f"{start_date}",
                    dateEnd=f"{end_date}",
                    submissionId=f"{id}")

            if "galleyViews" not in views:
                current_article.galley_views=0
            else:
                current_article.galley_views = views["galleyViews"]
            if "abstractViews" not in views:
               current_article.abstract_views = 0
            else:
               current_article.abstract_views = views["abstractViews"]
            if "publication" in views:
                #current_article.title = views["publication"]["fullTitle"]["en_US"]
                current_article.title = get_item_title(views)
            else:
                current_article.title="Not Found"
 
            if current_article not in articles:
                 if not current_article.has_no_views():
                    articles.append(current_article)

      articles.sort(key=lambda x: x.abstract_views, reverse=True)


      for article in articles:
         print(f"Latest={article}")

      print("\nTop 10 articles:")
      #top_10 = jnl.get_top_articles(start_date=start_date,end_date=end_date)
      all_articles = jnl.get_all_articles(start_date=start_date,end_date=end_date)

      sorted_all_articles = []
      if all_articles is not None:
          for item in all_articles["items"]:
                title=get_item_title(item)
                new_article = Article(jnl.jabbr, jnl.base_url, jnl.token, 
                               item["publication"]["id"],
                               item["galleyViews"], item["abstractViews"],
                               title)

                sorted_all_articles.append(new_article)


          sorted_all_articles.sort(key=lambda x: x.galley_views, reverse=True)
  
      top_10_articles=sorted_all_articles[:10]
      
      for article in top_10_articles:
         print(f"top10 ={article}")

      quarter_name=start_date.replace("-","")[0:6]
      create_date=datetime.date.today().strftime("%B %d, %Y")
      date_range=f"{start_date} : {end_date}"
      coverage_date=date_range
      chart1=QuarterlyReportChart("../files/Updated_UAL_OJS_Quarterly_Stats_Template.xlsx",
                                 f"../reports/{jabbr}_{quarter_name}_quarterly_report.xlsx")
#   print(create_date)
      chart1.reset_charts()
      chart1.update_report(start_date,create_date,date_range,jtitle)
      chart1.update_latest(articles)
      chart1.update_alltime(start_date, end_date, top_10_articles)
      nrows=len(top_10_articles)+10
      height=chart1.get_row_height()*nrows*2
      chart1.add_top_articles_chart(
                                     x_title="Articles",
                                     y_title="Number of Views",
                                     minrow=1,
                                     maxrow=len(top_10_articles)+1,
                                     loc="B6",chart_height=height
                                   )

      nrows=len(top_10_articles)+30
      height=(len(articles)+10)*chart1.get_row_height()*2
      chart1.add_latest_issue_chart(
                                     issue_name=f"{current['identification']}",
                                     x_title="Articles",
                                     y_title="Number of Views",
                                     minrow=1,
                                     maxrow=len(articles)+1,
                                     loc=f"B{nrows}",chart_height=height
                                   )
      chart1.save_workbook()
