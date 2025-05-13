from openpyxl import Workbook
from openpyxl import load_workbook
import datetime
from chart import Chart
from openpyxl.chart import Series, Reference, BarChart
from openpyxl.chart.label import DataLabelList

class MonthlyReport(Chart):
    
    def __init__(self,chart_template_file,chart_file):
        super().__init__(chart_template_file,chart_file)
        
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
 
     
    def update_charts(self, stats, name):
        
       srs=self.get_worksheet(name)    
       charts=srs._charts
       for chart in charts:
        # Get the width and height in points and convert to pixels (1 point = 1/72 inch, 1 inch = 96 pixels)
         width_points = chart.width
         height_points = chart.height
         chart.width=30
         print(f"Width={width_points}, Height={height_points}")
         if width_points is not None and height_points is not None:
             width_pixels = (width_points / 72) * 96
             height_pixels = (height_points / 72) * 96
     
             print(f" Width = {width_pixels}, Height={height_pixels}")

         #chart.series[0]=Series("TotalPublication","Statistics!$A$3:$A$6","Statistics!$E$3:$E$6",1)
         #data_range = series.values.coord 
         #print(series.tagname)
         #print(series.title)

 
         #ws=self.get_worksheet("Statistics")
         #values = Reference(ws,range_string="$A$3:$A$6,$B$3:$B$6")  # Initial data range
         #series = Series(values, title="Total Publication")
         series_formula="=SERIES(,,Statistics!$B$3:$B$5,Statistics!$A$3:$A$5,1)"
         chart.series[0].values=series_formula

    def add_chart(self,x_title="",y_title="",min_data_col=2,max_data_col=2,minrow=3,maxrow=10,loc="A10"):
       chart1 = BarChart()
       chart1.type = "bar"
       chart1.style = 11
       chart1.width = 25
       chart1.x_axis.title = x_title 
       chart1.y_axis.title = y_title 

       ws1=self.get_worksheet("Statistics")
       data = Reference(ws1, min_col=min_data_col, min_row=minrow, max_row=maxrow, max_col=max_data_col)
       cats = Reference(ws1, min_col=1, min_row=minrow, max_row=maxrow)
       chart1.add_data(data, titles_from_data=False)
       chart1.set_categories(cats)
       chart1.shape = 4
       chart1.dataLabels = DataLabelList() 
       chart1.dataLabels.showVal = True
       chart1.legend=None
       ws=self.get_worksheet("Report")
       ws.add_chart(chart1, loc)
 
