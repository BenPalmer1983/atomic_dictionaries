#
#   Makes elements dictionary file elements.pz
#
#

from pz import pz





class elements_make:
  data_file = "../data_files/elements.csv"
  dict_file = "../dictionaries/elements.pz"
  data_source = "https://gist.github.com/GoodmanSciences/c2dd862cd38f21b0ad36b8f96b4bf1ee"
  

  def run():
    d = {}
    d['info'] = {}
    d['info']['name'] = "Elements"
    d['info']['source'] = elements_make.data_source
    d['info']['source_file'] = elements_make.data_file
    
    d['symbols'] = {}
    d['elements'] = {}
     
    neutron = 'Nn'.strip().capitalize()
    d['symbols'][0] = neutron
    d['symbols'][neutron] = 0

    lines = []
    fh = open(elements_make.data_file, 'r')
    for line in fh:
      fields = line.strip().split(",")
      if(len(fields) == 28):
        lines.append(fields)

    for i in range(1, len(lines)):
      fields = lines[i]

      # Symbols
      protons = int(fields[0])
      symbol = str(fields[2]).strip().capitalize()
      d['symbols'][protons] = symbol
      d['symbols'][symbol] = protons

      # Elements
      name = str(fields[1]).strip().capitalize()

      d['elements'][protons] = {}
      d['elements'][protons]['z'] = protons 
      d['elements'][protons]['symbol'] = symbol 
      d['elements'][protons]['name'] = name 
      d['elements'][protons]['atomic_mass'] = float(fields[3]) 
      d['elements'][protons]['neutrons'] = int(fields[4]) 

      d['elements'][protons]['protons'] = int(fields[5]) 
      d['elements'][protons]['electrons'] = int(fields[6]) 
      d['elements'][protons]['period'] = int(fields[7]) 
      if(fields[8].strip() == ""):
        d['elements'][protons]['group'] = None
      else:
        d['elements'][protons]['group'] = int(fields[8]) 
      d['elements'][protons]['phase'] = str(fields[9]).strip().capitalize() 

      d['elements'][protons]['radioactive'] = elements_make.truefalse(fields[10])
      d['elements'][protons]['natural'] = elements_make.truefalse(fields[11])
      d['elements'][protons]['metal'] = elements_make.truefalse(fields[12])
      d['elements'][protons]['nonmetal'] = elements_make.truefalse(fields[13])
      d['elements'][protons]['metalloid'] = elements_make.truefalse(fields[14])


      d['elements'][protons]['type'] = str(fields[15]).strip().capitalize() 
      d['elements'][protons]['atomic_radius'] = elements_make.read_float(fields[16]) 
      d['elements'][protons]['electronegativity'] = elements_make.read_float(fields[17]) 
      d['elements'][protons]['first_ionization'] = elements_make.read_float(fields[18]) 
      d['elements'][protons]['density'] = elements_make.read_float(fields[19]) 

      d['elements'][protons]['melting_point'] = elements_make.read_float(fields[20]) 
      d['elements'][protons]['boiling_point'] = elements_make.read_float(fields[21]) 
      d['elements'][protons]['num_of_isotopes'] = elements_make.read_int(fields[22]) 
      d['elements'][protons]['discoverer'] = elements_make.read_float(fields[23]) 
      d['elements'][protons]['year'] = elements_make.read_int(fields[24]) 

      d['elements'][protons]['specific_heat'] = elements_make.read_float(fields[25]) 
      d['elements'][protons]['num_shells'] = elements_make.read_int(fields[26])
      d['elements'][protons]['num_valence'] = elements_make.read_int(fields[27])


    fh.close()

    pz.save(elements_make.dict_file, d, 'lzma')

  def truefalse(inp):
    inp = str(inp).strip().lower()
    if(len(inp) == 0):
      return False
    if(inp[0] == "y"):
      return True
    else:
      return False

  def read_float(inp):
    inp = str(inp).strip()
    if(inp == ""):
      return None
    try:
      return float(inp)
    except:
      return None

  def read_int(inp):
    inp = str(inp).strip()
    if(inp == ""):
      return None
    try:
      return int(inp)
    except:
      return None

elements_make.run()




# AtomicNumber,Element,Symbol,AtomicMass,NumberofNeutrons,
#NumberofProtons,NumberofElectrons,Period,Group,Phase,
#Radioactive,Natural,Metal,Nonmetal,Metalloid,
#Type,AtomicRadius,Electronegativity,FirstIonization,Density,
#MeltingPoint,BoilingPoint,NumberOfIsotopes,Discoverer,Year,
#SpecificHeat,NumberofShells,NumberofValence
