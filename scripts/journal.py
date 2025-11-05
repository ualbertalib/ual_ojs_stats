from ojs import OJS
import requests
import json
import datetime
import time
import pprint
import logging

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


  def get_submissions(self,status=3):
       
      url=f"{self._base_url}/api/v1/submissions"

      resp = requests.get(
         url,
         params={'apiToken':self._token, 'status':status}
      )

      jsond=resp.json()

      return jsond

  def get_issues(self,is_published='true'):
       
      url=f"{self._base_url}/api/v1/issues"

      resp = requests.get(
         url,
         params={'apiToken':self._token, 
                 'isPublished':f"'{is_published}'"
                }
      )
   
      jsond=resp.json()

      return jsond

  def get_publications(self, dateStart='2001-01-01',dateEnd=datetime.date.today()):

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



  def get_galley_views(self, dateStart='2001-01-01',
                       dateEnd=str(datetime.date.today().strftime("%Y-%m-%d")),
                       timelineInterval='month'):

      url=f"{self._base_url}/api/v1/stats/publications/galley"

      resp = requests.get(
         url,
         params={
            'apiToken':self._token,
            'timelineInterval': timelineInterval,
            'dateStart': dateStart,
            'dateEnd': dateEnd
         }
      ) 

      jsond=resp.json()

      return jsond 


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

     # get all the issues that were published     
     # by default, the issues are sorted by
     # "datePublished" in "DESC" order. 
     resp = requests.get(
         url,
         params={'apiToken':self._token,
                 'isPublished': True
                }
	)
     
     jsond=resp.json()
   
     # Find most recent issue, based on dateEnd
     if "items" not in jsond:
       return None

     for item in jsond['items']:
        issue_id = item['id']
        if (item['datePublished'][:7] <= dateEnd): 
           logging.info(f"Latest Issue={item}")
           break

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

  def get_all_articles(self,count=100, 
                            start_date="2001-01-01",
                            end_date=str(datetime.date.today().strftime("%Y-%m-%d"))
                            ):
       url = f"{self._base_url}/api/v1/stats/publications"
       max_retries=3
       delay_seconds=1
       all_articles = None
       current_offset = 0 # This will track the offset for each request

       iteration=0
       while True:
           retries = 0
           success = False
           current_page_items = [] # Initialize for each loop iteration

           iteration=iteration+1
           logging.info(f"Iteration = {iteration}")
           while retries < max_retries and not success:
               try:
                   response = requests.get(
                      url, 
                      params={
                        'apiToken': self._token,
                        'count': count,
                        'dateStart': start_date,
                        'dateEnd': end_date,
                        'orderDirection': 'DESC',
                        'offset': current_offset
                      } 
                      )

                   if response.status_code == 200:
                       current_page_items = response.json()
                       success = True
                   elif response.status_code == 401:
                       logging.error("Error: Unauthorized. Check your API token.")
                       return None # Critical error, cannot proceed
                   else:
                       logging.error(f"API Error (Status {response.status_code}): {response.text}")
                       retries += 1
                       time.sleep(delay_seconds * (2 ** retries)) # Exponential backoff
               except requests.exceptions.RequestException as e:
                   logging.error(f"Network Error: {e}")
                   retries += 1
                   time.sleep(delay_seconds * (2 ** retries)) # Exponential backoff

           if not success:
               logging.error(f"Failed to retrieve data for offset {current_offset} after {max_retries} attempts. Stopping.")
               return None

           # Add the items from the current page to our total list
           logging.info(f"current_page_items= {current_page_items}")
           if all_articles == None:
              all_articles=current_page_items
           else:
              items=current_page_items["items"]
              all_articles["items"].extend(items)
        
           # Check if this was the last page (fewer items than 'count' implies no more data)
           items=current_page_items["items"]
           if len(items) < count:
               break # No more items to retrieve

           current_offset += count # Prepare for the next page
           time.sleep(delay_seconds) # Wait a bit before the next request

       logging.info(f"Successfully retrieved a total of {len(all_articles)} articles.")
       return all_articles

 
  def get_top_articles(self,top=100,start_date="2001-01-01",end_date=str(datetime.date.today().strftime("%Y-%m-%d"))):
     url = f"{self._base_url}/api/v1/stats/publications"
     jsond=None 
     resp = requests.get(
         url,
         params={
	    'apiToken': self._token,
            'count': top,
            'dateStart': start_date, 
            'dateEnd': end_date, 
            'orderDirection': 'DESC',
         }
		)
     
     if resp.status_code == 200:
        jsond=resp.json()
      
     return jsond

  def get_contexts(self,searchPhrase=""):
     url = f"{self._base_url}/api/v1/contexts"

     resp = requests.get(
         url,
         params={
            'apiToken': self._token,
            'searchPhrase': self._jabbr, 
            'count': '1'
         }
                )

     jsond=resp.json()

     return jsond

  def get_main_page_views(self,date_start,date_end):

      url = f"{self._base_url}/api/v1/stats/publications"

      resp = requests.get(
         url,
         params={
            'apiToken': self._token,
            'assocType': 259,
            'assocId':1,
            'contextId':1,
            'metricType':"ojs::counter",
            'dateStart': date_start,
            'dateEnd': date_end
         }
       )

      jsond=resp.json()

      return jsond


  #
  # check connectivity with an given API Token
  #
  def verify_ojs_token(self):
      url = f"{self._base_url}/api/v1/stats/publications/abstract"  
      headers = {
          "Authorization": f"Bearer {self._token}",
          "Accept": "application/json"
      }

      try:
          response = requests.get(url, headers=headers, timeout=20)
          if response.status_code == 200:
              return True
          else:
              return False
      except requests.RequestException as e:
            return False

