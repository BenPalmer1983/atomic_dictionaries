import numpy
from pz import pz

class elements:

  path = "../dictionaries/elements.pz"
  loaded = False
  d = None
  v = True

  def set(path):
    elements.path = path

  def load():
    if(elements.loaded == False):
      elements.d = pz.load(elements.path)
      elements.loaded = True

  def get(inp):
    elements.load()
    z = elements.get_z(inp)
    if(z is None):
      return None
    return elements.d['elements'][z]


  def get_z(symbol):
    elements.load()
    try:
      e = int(symbol)
    except:
      e = symbol.strip().capitalize()        
    if(e not in elements.d['symbols'].keys()):
      return None
    if(isinstance(e, int)): 
      return e
    return elements.d['symbols'][e]

  def get_symbol(z):
    elements.load()
    try:
      e = int(z)
    except:
      e = z.strip().capitalize()        
    if(e not in elements.d['symbols'].keys()):
      return None
    if(not isinstance(e, int)): 
      return e
    return elements.d['symbols'][e]

  def test():
    print("==================================================")
    print("TESTING")
    print("==================================================")


    e = elements.get_z("pd")
    print(e)


    e = elements.get_symbol("26")
    print(e)

    e = elements.get_symbol(92)
    print(e)

    e = elements.get(92)
    print(e)

    e = elements.get("u")
    print(e)

    e = elements.get("ut")
    print(e)

elements.test()