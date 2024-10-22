import os
import sys
import requests
import json
import pandas as pd
from ojs import *
from journal import *
from chart import *
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook


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

     print(f"Processing: {jtitle},{jabbr},{base_url}")

     subs=jnl.get_submissions()
     issues=jnl.get_issues('true')
     abviews=jnl.get_abviews(dateStart=f"{previous_month[0]}-01",dateEnd=f"{previous_month[1]}")
     galley=jnl.get_galley_views(dateStart=f"{previous_month[0]}-01")
     #galley=jnl.get_galley_views(dateStart="2024-03-01",timelineInterval='month')
     pubs=jnl.get_publications()

     stat=dict()

     stat={
        "journal_title":jtitle,
        "journal_abbreviation": jabbr,
        "published_submissions": subs["itemsMax"] if "itemsMax" in subs else "0",
        "published_issues": issues["itemsMax"] if "itemsMax" in issues else "0",
        "abstract_views": abviews[0]["value"] if "error" not in abviews else "0",
        "galley_views": galley[0]["value"] if "error" not in galley else "0"
     }
     stats.append(stat)
     print(f"Finished {jtitle}") 

   strs = json.dumps(stats, indent=4)
   print(strs)

   chart1=Chart("../files/UAL_OJS_Report.xlsx","../reports/report.xlsx")
   chart1.update_worksheet(stats,"Journals",4,col_names)
   chart1.save_workbook() 


   f_monthly_report=f"../reports/monthly_report_{str(previous_month[0]).replace('-','')}.xlsx"
   chart2=Chart("../files/UAL_OJS_Monthly_Report_Template.xlsx",f_monthly_report)
   chart2.update_monthly_views(stats,str(previous_month[0]),str(datetime.date.today().strftime("%Y-%m-%d")),col_names)
   chart2.save_workbook()

   f_quarterly_report=f"../reports/quarterly_report_{str(previous_month[0]).replace('-','')}.xlsx"
   chart3=Chart("../files/UAL_OJS_Quarterly_Report_Template.xlsx",f_quarterly_report)
   chart3.update_quarterly_views(stats,str(previous_month[0]),str(datetime.date.today().strftime("%Y-%m-%d")),col_names)
   chart3.save_workbook()
