from ojs import OJS
import requests
import json
import datetime

class Journal(OJS):
  def __init__(self,jabbr,base_url,token):
     super().__init__(base_url)
     self._jabbr=jabbr
     self._token=token
  
  @property
  def jabbr(self):
     return self._jabbr

  @jabbr.setter
  def jabbr(self,value):
    self._jabbr=value

  @property
  def token(self):
     return self._token

  @token.setter
  def token(self,value):
    self._token=value

  #FURL="${url}${journal}/index.php/${journal}/api/v1/issues


  def get_submissions(self,status=3):
       
      #url=f"{self._base_url}/{self._jabbr}/index.php/{self._jabbr}/api/v1/submissions"
      url=f"{self._base_url}/api/v1/submissions"

      resp = requests.get(
         url,
         params={'apiToken':self._token, 'status':status}
      )

      jsond=resp.json()

      return jsond

  def get_issues(self,is_published='true'):
       
      #url=f"{self._base_url}/{self._jabbr}/index.php/{self._jabbr}/api/v1/issues"
      url=f"{self._base_url}/api/v1/issues"

      resp = requests.get(
         url,
         params={'apiToken':self._token, 'isPublished':f"'{is_published}'"}
      )
   
      jsond=resp.json()

      return jsond

  def get_publications(self, dateStart='2001-01-01',dateEnd=datetime.date.today()):

      #url=f"{self._base_url}/{self._jabbr}/index.php/{self._jabbr}/api/v1/stats/publications"
      url=f"{self._base_url}/api/v1/stats/publications"

      resp = requests.get(
         url,
         params={
            'apiToken':self._token,
            'dateStart':dateStart,
            'dateEnd':dateEnd
         }
      )

      jsond=resp.json()

      return jsond


  def get_abviews(self, dateStart='2001-01-01',dateEnd=datetime.date.today()):

      #url=f"{self._base_url}/{self._jabbr}/index.php/{self._jabbr}/api/v1/stats/publications/abstract"
      url=f"{self._base_url}/api/v1/stats/publications/abstract"

      resp = requests.get(
         url,
         params={
            'apiToken':self._token,
            'dateStart':dateStart,
            'dateEnd':dateEnd
         }
      ) 

      jsond=resp.json()

      return jsond 

#  def get_galley_views(self, dateStart='2001-01-01',dateEnd=datetime.date.today()):
  def get_galley_views(self, dateStart='2001-01-01',timelineInterval='month'):

      #url=f"{self._base_url}/{self._jabbr}/index.php/{self._jabbr}/api/v1/stats/publications/galley"
      url=f"{self._base_url}/api/v1/stats/publications/galley"

      resp = requests.get(
         url,
         params={
            'apiToken':self._token,
            'timelineInterval': timelineInterval,
            'dateStart': dateStart
#            'dateEnd':dateEnd
         }
      ) 

      jsond=resp.json()

      return jsond 

   ### New additions ###

  def get_current_issue(self):
      url = f"{self._base_url}/api/v1/issues/current"
      
      resp = requests.get(
         url,
         params={
	         'apiToken':self._token
         }
		)
      
      jsond=resp.json()
      
      return jsond
  
  
  def get_issues_asof(self, dateEnd):
     url = f"{self._base_url}/api/v1/issues"
     
     resp = requests.get(
         url,
         params={
	         'apiToken': self._token,
         }
		)
     
     jsond=resp.json()
   
      # Find most recent issue, based on dateEnd
     for item in jsond['items']:
        issue_id = item['id']
        if (item['datePublished'][:7] <= dateEnd): 
           break
        
     #print(f"Issue ID: {issue_id}")


     #issue_id = jsond['items'][0]['datePublished']

     url2 = f"{self._base_url}/api/v1/issues/{issue_id}"
     
     resp = requests.get(
         url2,
         params={
	         'apiToken': self._token,
            'issueId': issue_id,
         }
		)
     
     jsond2 = resp.json()
     
     
     return jsond2
 
  def get_top_articles(self):
     url = f"{self._base_url}/api/v1/stats/publications"
      
     resp = requests.get(
         url,
         params={
      
	         'apiToken': self._token,
            'count': '10',
            'dateStart': '2001-01-01', # For some reason necessary for the query to work - 01/01/01 is the earliest date the API supports
            'orderDirection': 'DESC',
         }
		)
     
     jsond=resp.json()
      
     return jsond