import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.chart import Series, Reference, BarChart
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.layout import Layout,ManualLayout
from openpyxl.styles import numbers
import datetime
from chart import Chart
from openpyxl.drawing.fill import PatternFillProperties, ColorChoice

class QuarterlyReportChart(Chart):
    
    def __init__(self,chart_template_file,chart_file):
        super().__init__(chart_template_file,chart_file)

    def update_report(self, coverage_date, create_date, date_range, title): 
        ws_report=self.get_worksheet("Statistics Report")
        ws_report["I1"]=f"{coverage_date}"
        ws_report["E2"]=f"{title}"
        ws_report["C4"]=f"{create_date}"
        ws_report["D6"]=f"Total Journal Home Page Views between {date_range}"

    
    def reset_charts(self):
        ws=self.get_worksheet("Statistics Report") 
        ws._charts.clear()
 
    def get_row_height(self):
        ws=self.get_worksheet("Statistics Report")
        height=ws.row_dimensions[1].height*0.035
        return height

    def update_latest(self, articles):
        ws_stat=self.get_worksheet("Latest Issue")

       
        # clear default data in the template
        for row in range(2,10):
          cells=[ws_stat[f"A{row}"],ws_stat[f"B{row}"],ws_stat[f"C{row}"],
                                    ws_stat[f"D{row}"],ws_stat[f"E{row}"]]   
          cells[0].value=""
          cells[1].value=""
          cells[2].value=""
          cells[3].value=""
         
        row=2
        for article in articles:
          cells=[ws_stat[f"A{row}"],ws_stat[f"B{row}"],ws_stat[f"C{row}"],
                                    ws_stat[f"D{row}"],ws_stat[f"E{row}"]]
          cells[0].number_format=numbers.BUILTIN_FORMATS[1]
          cells[0].value = article.id
          cells[1].value = f"{article.title}"
          cells[2].number_format=numbers.BUILTIN_FORMATS[1]
          cells[2].value = article.abstract_views
          cells[3].number_format=numbers.BUILTIN_FORMATS[1]
          cells[3].value = article.galley_views
          row=row+1


    def update_alltime(self, start, end, articles):
        '''
        Populates the first chart template with statistics from the Journal's 
        top 10 articles of all time.
        Also enters the start and end dates for the statistics period.
        start: str
          Start date.
        end: str
          End date.
        articles: list[Articles]
          List of top 10 articles, sorted in descending order.
        '''
        ws_report=self.get_worksheet("Statistics Report")

        #ws_report["I1"].value=str(start)
        #ws_report["C4"].value=str(end)

        ws_stat=self.get_worksheet("Article Downloads (All Issues)")
        # clear default data in the template
        for row in range(2,10):
          cells=[ws_stat[f"A{row}"],ws_stat[f"B{row}"],ws_stat[f"C{row}"],
                                    ws_stat[f"D{row}"],ws_stat[f"E{row}"]]
          cells[0].value=""
          cells[1].value=""
          cells[2].value=""
          cells[3].value=""

        row=2
        for article in articles:
            cells=[ws_stat[f"A{row}"],ws_stat[f"B{row}"],ws_stat[f"C{row}"],
                                      ws_stat[f"D{row}"],ws_stat[f"E{row}"]]
            cells[0].number_format=numbers.BUILTIN_FORMATS[1]
            cells[0].value = article.id
            cells[1].value = f"{article.title}"
            cells[2].number_format=numbers.BUILTIN_FORMATS[1]
            cells[2].value = article.abstract_views
            cells[3].number_format=numbers.BUILTIN_FORMATS[1]
            cells[3].value = article.galley_views
            row=row+1


    def add_latest_issue_chart(self,x_title="",y_title="",min_data_col=3,
                            max_data_col=4,minrow=2,maxrow=10,loc="A10",chart_height=15):

       chart1 = BarChart()
       chart1.type = "bar"
       chart1.style = 11
       chart1.width = 25
       chart1.height = chart_height
       chart1.x_axis.title = x_title
       chart1.y_axis.title = y_title
       chart1.title="Latest Issue"
       chart1.width=30
       chart1.gapWidth=30
       chart1.overlap= -20

       ws1=self.get_worksheet("Latest Issue")
       # find row height

       data = Reference(ws1, min_col=min_data_col, min_row=minrow, 
                                max_row=maxrow, max_col=max_data_col)
       cats = Reference(ws1, min_col=2, min_row=minrow+1, max_row=maxrow)
       chart1.add_data(data, titles_from_data=True)
       chart1.set_categories(cats)
       chart1.shape = 4
       chart1.dataLabels = DataLabelList()
       chart1.dataLabels.showVal = True

       chart1.legend=openpyxl.chart.legend.Legend()
       chart1.legend.position = 't' #right
       ws=self.get_worksheet("Statistics Report")

       colors = ["FFA500", "3CB371"]  # Hex codes for green and yellow

       for i, series in enumerate(chart1.series):
          series.graphicalProperties.solidFill = colors[i]

       ws.add_chart(chart1, loc)

    def add_top_articles_chart(self,x_title="",y_title="",min_data_col=3,
                            max_data_col=4,minrow=2,maxrow=10,
                            loc="A10",chart_height=15):
       chart1 = BarChart()
       chart1.type = "bar"
       chart1.style = 11
       chart1.width = 25
       chart1.height= chart_height
       chart1.x_axis.title = x_title
       chart1.y_axis.title = y_title
       chart1.title="Most Downloaded* Articles (All Articles)"
       chart1.width=30
       chart1.gapWidth=30
       chart1.overlap= -20

       ws1=self.get_worksheet("Article Downloads (All Issues)")
       # find row height

       data = Reference(ws1, min_col=min_data_col, min_row=minrow,
                                max_row=maxrow, max_col=max_data_col)
       cats = Reference(ws1, min_col=2, min_row=minrow+1, max_row=maxrow)
       chart1.add_data(data, titles_from_data=True)
       chart1.set_categories(cats)
       chart1.shape = 4
       chart1.dataLabels = DataLabelList()
       chart1.dataLabels.showVal = True
       chart1.legend=openpyxl.chart.legend.Legend()
       chart1.legend.position = 't' #right
       ws=self.get_worksheet("Statistics Report")

       # Set series colors (Green and Yellow)
       colors = ["FFA500", "3CB371"]  # Hex codes for green and yellow
       for i, series in enumerate(chart1.series):
          series.graphicalProperties.solidFill = colors[i]

       ws.add_chart(chart1, loc)

