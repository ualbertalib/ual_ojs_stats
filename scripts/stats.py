import os
import sys
import requests
import json
import pandas as pd
from ojs import *
from journal import *
import datetime

def get_previous_month():
   
   today = datetime.date.today()
   first = today.replace(day=1)
   previous_month = first - datetime.timedelta(days=1)
   month_lookup = previous_month.strftime("%Y-%m")
   return month_lookup

if __name__ == '__main__':

   fname=sys.argv[1]
   journals = pd.read_csv(fname) 
   previous_month=get_previous_month()

   stats=[]

   for ind in journals.index:
     jabbr=journals["jabbr"][ind]
     base_url=journals["base_url"][ind]
     token=journals["token"][ind]
     jnl=Journal(jabbr,base_url,token)

     subs=jnl.get_submissions()
     issues=jnl.get_issues('true')
     abviews=jnl.get_abviews(f"{previous_month}-01")
     galley=jnl.get_galley_views(f"{previous_month}-01")
     pubs=jnl.get_publications()

     stat=dict()

     stat={
        "journal abbreviation": jabbr,
        "published submissions": subs["itemsMax"],
        "published issues": issues["itemsMax"],
        "abstract views": abviews[0]["value"],
        "galley views": galley[0]["value"]
     }
     stats.append(stat)

   strs = json.dumps(stats, indent=4)
   print(strs)
