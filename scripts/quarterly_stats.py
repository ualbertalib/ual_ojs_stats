import os
import sys
import requests
import json
import pandas as pd
from ojs import *
from journal import *
from chart import *
from quarterlyreport import *
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook

def get_previous_quarter():
   today = datetime.date.today()
   first = today.replace(day=1)
   month_three = first - datetime.timedelta(days=1)
   month_lookup_three = month_three.strftime("%Y-%m")
   
   first = month_three.replace(day=1)
   month_two = first - datetime.timedelta(days=1)
   month_lookup_two = month_two.strftime("%Y-%m")
   
   first = month_two.replace(day=1)
   month_one = first - datetime.timedelta(days=1)
   month_lookup_one = month_one.strftime("%Y-%m")
   months = [[month_lookup_one, month_one], [month_lookup_two, month_two], [month_lookup_three, month_three]]

   return months


if __name__ == '__main__':
   
   fname=sys.argv[1]
   journals = pd.read_csv(fname) 
   months = get_previous_quarter()

   stats=[]
   col_names=["journal_title","published_submissions","published_issues","abstract_views","galley_views"]
   for ind in journals.index:
      jtitle=journals["journal_title"][ind]
      jabbr=journals["journal_abbr"][ind]
      base_url=journals["base_url"][ind]
      token=journals["api_key"][ind]
      jnl=Journal(jabbr,base_url,token)
    
      print(f"{jtitle},{jabbr},{base_url},{token}")
         
      for month in months:

         subs=jnl.get_submissions()
         issues=jnl.get_issues('true')
         abviews=jnl.get_abviews(dateStart=f"{month[0]}-01",dateEnd=f"{month[1]}")
         galley=jnl.get_galley_views(dateStart=f"{month[0]}-01")
         #galley=jnl.get_galley_views(dateStart="2024-03-01",timelineInterval='month')
         pubs=jnl.get_publications()
   
         stat=dict()
   
         stat={
            "journal_title":jtitle,
            "journal_abbreviation": jabbr,
            "published_submissions": subs["itemsMax"],
            "published_issues": issues["itemsMax"],
            "abstract_views": abviews[0]["value"],
            "galley_views": galley[0]["value"]
         }
         stats.append(stat)
         #end loop
   strs = json.dumps(stats, indent=4)
   print(strs)

   chart1=QuarterlyReport("../files/UAL_OJS_Report.xlsx","../files/report.xlsx")
   chart1.update_worksheet(stats,"Journals",4,col_names)
   chart1.save_workbook() 


   chart2=QuarterlyReport("../files/UAL_OJS_Quarterly_Report_Template.xlsx",f"../files/quarterly_report.xlsx")
   chart2.update_monthly_views(stats,str(months[0][0]),str(datetime.date.today().strftime("%Y-%m-%d")),col_names)
   chart2.update_monthly_views(stats,str(months[1][0]),str(datetime.date.today().strftime("%Y-%m-%d")),col_names)
   chart2.update_monthly_views(stats,str(months[2][0]),str(datetime.date.today().strftime("%Y-%m-%d")),col_names)
   chart2.save_workbook()
