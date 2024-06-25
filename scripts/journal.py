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
            'dateStart':dateStart
#            'dateEnd':dateEnd
         }
      ) 

      jsond=resp.json()

      return jsond 
