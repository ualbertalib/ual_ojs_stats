class OJS:
  def __init__(self,base_url):
     self._base_url=base_url
  
  @property
  def base_url(self):
     return self._base_url

  @base_url.setter
  def base_url(self,value):
    self._base_url=value

 
