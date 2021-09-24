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

    fh = open(elements_make.data_file, 'r')
    for line in fh:
      fields = line.split(",")
      try:
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
        d['elements'][protons]['group'] = int(fields[8]) 
        d['elements'][protons]['phase'] = str(fields[9]).strip().capitalize() 


        d['elements'][protons]['description'] = str(fields[15]).strip().capitalize() 

      except:
        pass
    fh.close()

    pz.save(elements_make.dict_file, d, 'lzma')


elements_make.run()




# AtomicNumber,Element,Symbol,AtomicMass,NumberofNeutrons,
#NumberofProtons,NumberofElectrons,Period,Group,Phase,
#Radioactive,Natural,Metal,Nonmetal,Metalloid,
#Type,AtomicRadius,Electronegativity,FirstIonization,Density,
#MeltingPoint,BoilingPoint,NumberOfIsotopes,Discoverer,Year,
#SpecificHeat,NumberofShells,NumberofValence
