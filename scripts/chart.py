from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import numbers

import datetime

class Chart: 

  def __init__(self,chart_template_file,chart_file):
     self._chart_template_file=chart_template_file
     self._chart_file=chart_file
     self._wb=load_workbook(filename=f"{self._chart_template_file}")

  @property
  def workbook(self):
     return self._wb

  @workbook.setter
  def workbook(self,value):
    self._wb=value
   

  def get_worksheet(self, name):
    return self._wb[name] 


  def save_workbook(self):
    self._wb.save(self._chart_file)


  def update_worksheet(self,stats,name,start_row,col_names):
    today = datetime.date.today()
    first = today.replace(day=1)
    previous_month = first - datetime.timedelta(days=1)
    month_lookup = previous_month.strftime("%Y-%m")

    srs=self.get_worksheet(name)
    srs["B1"]=today
    srs["D1"]=month_lookup
    i=start_row
    for stat in stats:
      cols=[srs[f"A{i}"],srs[f"B{i}"],srs[f"C{i}"],srs[f"D{i}"],srs[f"E{i}"]]
      i=i+1
      for j in range(0,len(cols)):
         cols[j].value=stat[col_names[j]]

   

