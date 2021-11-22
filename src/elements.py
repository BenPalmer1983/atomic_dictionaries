# Data source https://gist.github.com/GoodmanSciences/c2dd862cd38f21b0ad36b8f96b4bf1ee

import numpy
from pz import pz

class elements:

  path = "../dictionaries/elements.pz"
  loaded = False
  d = None
  v = True

  @staticmethod
  def set(path):
    elements.path = path

  @staticmethod
  def load():
    if(elements.loaded == False):
      elements.d = pz.load(elements.path, 'lzma')
      elements.loaded = True

  @staticmethod
  def get(inp):
    elements.load()
    z = elements.get_z(inp)
    if(z is None):
      return None
    return elements.d['elements'][z]

  @staticmethod
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

  @staticmethod
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



  @staticmethod
  def to_csv(output_file):
    fh = open(output_file, 'w')
    for p in sorted(elements.d['elements'].keys()):
      fh.write(str(elements.d['elements'][p]['z']) + ",") 
      fh.write(str(elements.d['elements'][p]['symbol']) + ",")
      fh.write(str(elements.d['elements'][p]['name']) + ",")
      fh.write(str(elements.d['elements'][p]['atomic_mass']) + ",")
      fh.write(str(elements.d['elements'][p]['protons']) + ",")
      fh.write(str(elements.d['elements'][p]['neutrons']) + ",")
      fh.write(str(elements.d['elements'][p]['electrons']) + ",")
      fh.write(str(elements.d['elements'][p]['period']) + ",")
      fh.write(str(elements.d['elements'][p]['group']) + ",")
      fh.write(str(elements.d['elements'][p]['phase']) + ",")
      fh.write(str(elements.d['elements'][p]['radioactive']) + ",")
      fh.write(str(elements.d['elements'][p]['natural']) + ",")
      fh.write(str(elements.d['elements'][p]['metal']) + ",")
      fh.write(str(elements.d['elements'][p]['nonmetal']) + ",")
      fh.write(str(elements.d['elements'][p]['metalloid']) + ",")
      fh.write(str(elements.d['elements'][p]['type']) + ",")
      fh.write(str(elements.d['elements'][p]['atomic_radius']) + ",")
      fh.write(str(elements.d['elements'][p]['electronegativity']) + ",")
      fh.write(str(elements.d['elements'][p]['first_ionization']) + ",")
      fh.write(str(elements.d['elements'][p]['density']) + ",")
      fh.write(str(elements.d['elements'][p]['melting_point']) + ",")
      fh.write(str(elements.d['elements'][p]['boiling_point']) + ",")
      fh.write(str(elements.d['elements'][p]['num_of_isotopes']) + ",")
      fh.write(str(elements.d['elements'][p]['discoverer']) + ",")
      fh.write(str(elements.d['elements'][p]['year']) + ",")
      fh.write(str(elements.d['elements'][p]['specific_heat']) + ",")
      fh.write(str(elements.d['elements'][p]['num_shells']) + ",")
      fh.write(str(elements.d['elements'][p]['num_valence']) + "\n")
    fh.close()



  @staticmethod
  def test():
    # set path to the pickled elements dictionary
    elements.set("../dictionaries/elements.pz")

    # Load dictionary (not necessary, as will be checked and loaded if not already loaded)
    elements.load()

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


    e = elements.to_csv("output.csv")



def main():
  elements.test()

if __name__ == "__main__":
    main()    

