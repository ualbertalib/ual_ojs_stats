from ojs import OJS
from journal import Journal
import requests
import json
import datetime

class Article(Journal):
  def __init__(self,jabbr,base_url,token,submission_id,galley_views=-1,abstract_views=-1,title="", issue=""):
     super().__init__(jabbr,base_url,token)
     self._id=submission_id
     self._galley_views=galley_views
     self._abstract_views=abstract_views
     self._title=title
     self._issue=issue

  def __repr__(self):
     return f"\nArticle ID: {self.id}\nTitle: {self.title}\nIssue: {self.issue}\nGalley views: {self.galley_views}\nAbstract views: {self.abstract_views}"
  
  @property
  def id(self):
     return self._id

  @id.setter
  def id(self,value):
    self._id=value
  
  @property
  def galley_views(self):
     return self._galley_views
  
  @galley_views.setter
  def galley_views(self, value):
     self._galley_views=value

  @property
  def abstract_views(self):
     return self._abstract_views
  
  @abstract_views.setter
  def abstract_views(self, value):
     self._abstract_views=value

  @property
  def title(self):
     return self._title
  
  @title.setter
  def title(self, value):
     self._title=value

  @property
  def issue(self):
     return self._issue
  
  @issue.setter
  def issue(self, value):
     self._issue=value

  def get_submission_views(self, dateStart, dateEnd, submissionId):
   
      url=f"{self._base_url}/api/v1/stats/publications/{submissionId}"
   
      resp = requests.get(
         url,
         params={
				'apiToken':self._token,
				'dateStart':dateStart,
				'dateEnd':dateEnd,
			}
		)
      
      jsond=resp.json()
      
      return jsond
  
  def get_submission(self, submissionId):
     url=f"{self._base_url}/api/v1/stats/submissions/{submissionId}/publications"

     resp = requests.get(
         url,
         params={
				'apiToken':self._token,
            'submissionId':f"{str(submissionId)}",
			}
		)
     
     #print(f"{resp}")
       
     jsond=resp.json()
     
     return jsond

     



