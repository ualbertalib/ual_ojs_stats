from ojs import OJS
from journal import Journal
import requests
import json
import datetime

class Article(Journal):
  '''
   Article is a class that represents one article from an issue of
   an OJS journal.

   Attributes:
     jabbr: str
        Journal abbreviation. Inherited from Journal class.
     base_url: str
        Base URL of the OJS instance. Inherited from the OJS class via 
        the Journal class.
     token: str
        API token corresponding to the journal. Ingherited from 
        the Journal class.
     id: int
        The unique id assigned to a submission in OJS.
     galley_views: int
        The number of views of the article fulltext. -1 by default.
     abstract_views: int
        The number of views of the article abstract. -1 by default.
     Title: str
        The title of the article. Empty string by default.
     Issue: str
        The id of the article's issue. Empty string by default.
  '''
  def __init__(self,jabbr,base_url,
               token,submission_id,galley_views=0,
               abstract_views=0,title="", issue=""):
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

  def __eq__(self, other):
     if not isinstance(other, Article):
        return NotImplemented
     return self._id == other.id and self._title == other.title

  def __hash__(self):
     return hash(self._id,self._title)


  def has_no_views(self):
     return self._abstract_views == 0 and self._galley_views == 0    

  def get_submission_views(self, dateStart, dateEnd, submissionId):
      '''
      Gets the views of an Article from a given time period.
      dateStart: str
         Start date.
      dateEnd: str
         End date.
      submissionId: str
         ID of the article (assigned in OJS).
      '''

      url=f"{self._base_url}/api/v1/stats/publications/{submissionId}"
   
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
