from openpyxl import Workbook
from openpyxl import load_workbook
import datetime

class nChart: 


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

  def update_alltime(self, start, end, articles):
    ws_report=self.get_worksheet("Statistics Report")

    ws_report["I1"].value=str(start)
    ws_report["C4"].value=str(end)

    ws_stat=self.get_worksheet("Article Downloads (All Issues)")
    row=2
    for article in articles:
      cols=[ws_stat[f"A{row}"],ws_stat[f"B{row}"],ws_stat[f"C{row}"],ws_stat[f"D{row}"],ws_stat[f"E{row}"]]
      row=row+1
      cols[0].value = f"{article.id}"
      cols[1].value = f"{article.title}"
      cols[2].value = f"{article.abstract_views}"
      cols[3].value = f"{article.galley_views}"



  def update_latest(self, articles):
    ws_stat=self.get_worksheet("Latest Issue")
    row=2
    for article in articles:
      cols=[ws_stat[f"A{row}"],ws_stat[f"B{row}"],ws_stat[f"C{row}"],ws_stat[f"D{row}"],ws_stat[f"E{row}"]]
      row=row+1
      cols[0].value = f"{article.id}"
      cols[1].value = f"{article.title}"
      cols[2].value = f"{article.abstract_views}"
      cols[3].value = f"{article.galley_views}"



