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
     print(subs["itemsMax"])
     print(abviews)
     print(galley)
     print(pubs)
