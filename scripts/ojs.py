class OJS:
  """
  OJS is a base class that represents an OJS host. It has a base URL that
  represents the host. For example, https://journals.library.ualberta.ca/

  ...

  Attributes
  -----------------------------------------------------------------------
  base_url: str
      the host url, i.e., https://journals.library.ualberta.ca/
  
  """
  def __init__(self,base_url):
     self._base_url=base_url
  
  @property
  def base_url(self):
     # get base_url
     return self._base_url
    

  @base_url.setter
  def base_url(self,value):
    # set base_url
    self._base_url=value

 
