import os
import sys
import requests
import json
import pandas as pd
from ojs import *
from journal import *
from chart import *
from monthlyreport import *
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
import pprint

def get_previous_month():   
   today = datetime.date.today()
   first = today.replace(day=1)
   previous_month = first - datetime.timedelta(days=1)
   month_lookup = previous_month.strftime("%Y-%m")
   return [month_lookup, previous_month]

if __name__ == '__main__':
   
   fname=sys.argv[1]
   journals = pd.read_csv(fname) 
   previous_month=get_previous_month()

   stats=[]
   col_names=["journal_title","published_submissions","published_issues","abstract_views","galley_views"]
   for ind in journals.index:
     jtitle=journals["journal_title"][ind]
     jabbr=journals["journal_abbr"][ind]
     base_url=journals["base_url"][ind]
     token=journals["api_key"][ind]
     jnl=Journal(jabbr,base_url,token)

     print(f"{jtitle},{jabbr},{base_url},{token}")

     subs=jnl.get_submissions()
     issues=jnl.get_issues('true')
     abviews=jnl.get_abviews(dateStart=f"{previous_month[0]}-01",dateEnd=f"{previous_month[1]}")
     galley=jnl.get_galley_views(dateStart=f"{previous_month[0]}-01")
     pubs=jnl.get_publications()

     stat=dict()

     pprint.pprint(subs)
     print("\n\n")
     stat={
        "journal_title":jtitle,
        "journal_abbreviation": jabbr,
        "published_submissions": subs["itemsMax"],
        "published_issues": issues["itemsMax"],
        "abstract_views": abviews[0]["value"],
        "galley_views": galley[0]["value"]
     }
     stats.append(stat)

   strs = json.dumps(stats, indent=4)
   print(strs)


   chart1=MonthlyReport("../files/UAL_OJS_Monthly_Report_Template.xlsx",f"../reports/monthly_report_{str(previous_month[0]).replace('-','')}.xlsx")

   chart1.update_monthly_views(stats,str(previous_month[0]),str(datetime.date.today().strftime("%Y-%m-%d")),col_names)

   max_row=len(stats)
   row=7
   gap=3
   location=f"B{row}"
   chart1.add_chart(x_title="Total Submissions",y_title="Journal",min_data_col=2,max_data_col=2,minrow=3,maxrow=max_row,loc=location)

   rows=row+len(stats)+gap
   location=f"B{rows}"
   chart1.add_chart(x_title="Total Published Issues",y_title="Journal",min_data_col=3,max_data_col=3,minrow=3,maxrow=max_row,loc=location)


   rows=row+2*(len(stats)+gap)
   location=f"B{rows}"
   chart1.add_chart(x_title="Total Abstract Views",y_title="Journal",min_data_col=4,max_data_col=4,minrow=3,maxrow=max_row,loc=location)

   rows=row+3*(len(stats)+gap)
   location=f"B{rows}"
   chart1.add_chart(x_title="Total Galley Views",y_title="Journal",min_data_col=4,max_data_col=4,minrow=3,maxrow=max_row,loc=location)

   chart1.save_workbook()
