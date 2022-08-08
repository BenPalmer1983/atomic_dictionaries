#
#   Makes isotopes dictionary files isotopes.pz gammas.pz
#
#

import numpy
import hashlib
from pz import pz
import pickle
import _pickle as cPickle




class isotopes_make:

  element_file = "../data_files/elements.csv"
  jeff_file = "../data_files/JEFF33-rdd_all.asc"
  dict_file_pz = "../dictionaries/isotopes.pz"
  dict_file_p = "../dictionaries/isotopes.p"
  hashes = "../dictionaries/hashes.txt"
  data_source = {"JEFF 3.3 via NEA", "https://gist.github.com/GoodmanSciences/c2dd862cd38f21b0ad36b8f96b4bf1ee"}
  stable = {}
  unstable = {}
  observationally_stable = {}
  symbols = {}
  isotopes = {}
  gammas = {}
  gammas_array = {}
  list = []
  list_tree = {}

  valid_codes = []
  stable_codes = []
  unstable_codes = []
  observationally_stable_codes = []

  metastable_codes = []

  def run():
    d = {}
    d['info'] = {}
    d['info']['name'] = "Isotopes"
    d['info']['source'] = isotopes_make.data_source
    d['info']['source_file'] = {isotopes_make.jeff_file, isotopes_make.element_file}
    d['info']['help'] = """
This data is from  the JEFF 3.3 data file and a GitHub project.


Dictionary split into several parts.
'info'
'isotopes'
'symbols'
'stable'
'unstable'
'list'
'list_tree'
'gammas'
'gammas_array'


Isotope keys for each isotope:
'key': None,    
'element': None,  
'protons': None, 
'neutrons': None, 
'nucleons': None, 
'metastable': None, 
'stable': False,
'natural_abundance': 0.0,
'mass_to_neutron': None,
'mass_amu': None,
'half_life': None,
'decay_modes': {},






    """

    isotopes_make.load_symbols()
    isotopes_make.load_jeff()

    d['isotopes'] = isotopes_make.isotopes
    d['symbols'] = isotopes_make.symbols
    d['stable'] = isotopes_make.stable
    d['unstable'] = isotopes_make.unstable
    d['observationally_stable'] = isotopes_make.observationally_stable
    d['list'] = isotopes_make.list
    d['list_tree'] = isotopes_make.list_tree
    d['gammas'] = isotopes_make.gammas
    d['gammas_array'] = isotopes_make.gammas_array
    d['valid_codes'] = isotopes_make.valid_codes
    d['stable_codes'] = isotopes_make.stable_codes
    d['metastable_codes'] = isotopes_make.metastable_codes
    d['unstable_codes'] = isotopes_make.unstable_codes
    d['observationally_stable_codes'] = isotopes_make.observationally_stable_codes


    # Save as pickle
    with open(isotopes_make.dict_file_p, 'wb') as f:
      pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)


    # Save as pz
    pz.save(isotopes_make.dict_file_pz, d, 'lzma')
  

    # Save hash
    fh = open(isotopes_make.hashes, 'w')
 
    phash = hashlib.sha256()
    with open(isotopes_make.dict_file_p, 'rb') as f:
      fb = f.read(1048576)
      while len(fb) > 0:
        phash.update(fb)
        fb = f.read(1048576)

    fh.write("Pickle:" + "\n")
    fh.write(phash.hexdigest() + "\n")
 
    pzhash = hashlib.sha256()
    with open(isotopes_make.dict_file_pz, 'rb') as f:
      fb = f.read(1048576)
      while len(fb) > 0:
        pzhash.update(fb)
        fb = f.read(1048576)

    fh.write("Pickle Zipped:" + "\n")
    fh.write(pzhash.hexdigest() + "\n")
    
    fh.close()


    #print(isotopes_make.symbols)
    #isotopes_make.load_jeff(isotopes_make.data_file)


  def load_symbols():
    neutron = 'Nn'.strip().capitalize()
    isotopes_make.symbols[0] = neutron
    isotopes_make.symbols[neutron] = 0
    fh = open(isotopes_make.element_file, 'r')
    for line in fh:
      fields = line.split(",")
      try:
        # Symbols
        protons = int(fields[0])
        symbol = str(fields[2]).strip().capitalize()
        isotopes_make.symbols[protons] = symbol
        isotopes_make.symbols[symbol] = protons
      except:
        pass
    fh.close()


  @staticmethod      
  def load_jeff():
    blocks_451 = {}   
    blocks_457 = {}  
    # Read into MF -> MT
    fh = open(isotopes_make.jeff_file, 'r')    
    n = 0
    for row in fh:
      n = n + 1
      mf = int(row[70:72])
      mt = int(row[72:75])
      mat = int(row[66:70])
      row_num = int(row[75:]) 
      if(mt == 451):
        if(mat not in blocks_451.keys()):
          blocks_451[mat] = []
        blocks_451[mat].append(row[:-1])
      if(mt == 457):
        if(mat not in blocks_457.keys()):
          blocks_457[mat] = []
        blocks_457[mat].append(row[:-1])
    fh.close()
       
    # Process blocks
    for k in blocks_451.keys():
      isotopes_make.jeff_block(blocks_451[k], blocks_457[k])


  @staticmethod    
  def jeff_block(blocks_451, blocks_457):
    isotope = {
    'key': None,    
    'element': None,  
    'protons': None, 
    'neutrons': None, 
    'nucleons': None, 
    'metastable': None, 
    'stable': False,
    'natural_abundance': 0.0,
    'mass_to_neutron': None,
    'mass_amu': None,
    'half_life': None,
    'decay_constant': None,
    'decay_modes': {},
    }

    gammas = None
    gammas_array = None
    
    for row in blocks_451:
      if("STABLE NUCLEUS" in row):
        isotope['stable'] = True
      elif("NATURAL ABUNDANCE" in row):
        isotope['natural_abundance'] = float(row[19:31].strip().replace(" ","")) / 100.0    # 0.0 to 1.0
  
    for row in blocks_451:
      l = []
      l.append(row[0:11])
      l.append(row[11:22])
      l.append(row[22:33])
      l.append(row[33:44])
      l.append(row[44:55])
      l.append(row[55:66]) 
      mat = int(row[66:70])
      mf = int(row[70:72])
      mt = int(row[72:75])
      row_num = int(row[75:]) 
      #print(l[0],l[1],l[2],l[3],l[4],l[5],mat,mf,mt, row_num)  
    
      if(row_num == 1):
        isotope['key'] = int(isotopes_make.read_float(l[0]))
        isotope['protons'], isotope['neutrons'], isotope['nucleons'] = isotopes_make.read_isotope_code(isotope['key'])
        isotope['element'] = isotopes_make.symbols[isotope['protons']]
        isotope['mass_to_neutron'] = float(isotopes_make.read_float(l[1]))
        isotope['mass_amu'] = isotope['mass_to_neutron'] * 1.00866531
      elif(row_num == 2):
        if(int(isotopes_make.read_float(l[3])) == 0):
          isotope['metastable'] = int(isotopes_make.read_float(l[3]))
        else:
          isotope['metastable'] = int(isotopes_make.read_float(l[3]))
          isotope['key'] = isotope['key'] + 1000000 * int(isotopes_make.read_float(l[3]))
          
          
          
    # ONLY PROCESS 457 IF UNSTABLE
    #if(not isotope['stable'] and (isotope['key'] == 41090 or isotope['key'] == 39104 or isotope['key'] == 27055)):
    if(not isotope['stable']):
      #  and (isotope['key'] == 41090 or isotope['key'] == 39104)
      #  and isotope['key'] == 39104
      # and isotope['key'] == 41090
      # print(isotope['key'])
    
      n_rows = len(blocks_457)
      loop = True
      a_rows = -1
      b_rows = -1
      discrete = 0
      n = 0
      
      modes = {  10: ['B-',1,-1, True], 
                 15: ['B-, N',-1,0, True],
                 20: ['B+',-1,1, True],
                 30: ['IT',0,0, True],
                 40: ['A',-2,-2, True],
                 50: ['N',0,-1, True],
                 60: ['SF',0,0, False],
              }
      
      while(n < n_rows and loop):
        l, mat, mf, mt, row_num = isotopes_make.read_row(blocks_457[n])
        #print(blocks_457[n])
        if(row_num == 2):
          isotope['half_life'] = float(isotopes_make.read_float(l[0]))   
          isotope['half_life_error'] = float(isotopes_make.read_float(l[1]))    
          a_points = int(l[4])
          a_rows = int(numpy.ceil(a_points / 6))
          isotope['decay_constant'] = numpy.log(2) / isotope['half_life']
    
        elif(a_rows > 0 and row_num == 3 + a_rows):
          isotope['spin_parity'] = float(isotopes_make.read_float(l[0]))   
          b_points = int(l[4])
          b_rows = int(numpy.ceil(b_points / 6))   
          #print(row_num, b_points, b_rows)
          
        elif(b_rows > 0 and row_num >= 3 + a_rows + 1 and row_num <= 3 + a_rows + b_rows):
          #print("....",blocks_457[n])
          mode_n = int(10 * isotopes_make.read_float(l[0]))
          if(mode_n in modes.keys()):
            mode = modes[mode_n]
            if(mode[3]):              
              mode_text = mode[0]
              to_p = isotope['protons'] + mode[1]
              to_n = isotope['neutrons'] + mode[2]
              to_meta = int(isotopes_make.read_float(l[1]))
              qvalue = float(isotopes_make.read_float(l[2]))            # In eV
              branching_factor = float(isotopes_make.read_float(l[4]))  # 0.0 to 1.0              
              #print(mode_text, to_p, to_n, to_meta, qvalue, branching_factor)
              
              to_key = to_meta * 1000000 + 1000 * to_p + (to_p + to_n)            
              isotope['decay_modes'][to_key] = {}
              isotope['decay_modes'][to_key]['branching_factor'] = branching_factor
              isotope['decay_modes'][to_key]['to_meta'] = to_meta
              isotope['decay_modes'][to_key]['qvalue'] = qvalue

         
        elif(row_num > 3 + a_rows + b_rows):
          try:
            if(float(isotopes_make.read_float(l[0])) == 0.0 and float(isotopes_make.read_float(l[1])) == 0.0 and int(l[3]) == 0 and int(l[5]) > 0):
              #print(blocks_457[n])
              
              n = n + 1

              gamma_rows = int(l[5])
              l, mat, mf, mt, row_num = isotopes_make.read_row(blocks_457[n])
              nfact = float(isotopes_make.read_float(l[0])) 
              
              gammas = []
              gammas_array = numpy.zeros((gamma_rows, 2,),)
              if(isotope['protons'] == 27 and isotope['nucleons'] == 55):
                print(gamma_rows)
              for gn in range(gamma_rows):
                           
                n = n + 1


                l, mat, mf, mt, row_num = isotopes_make.read_row(blocks_457[n])
                
                # First row
                energy = float(isotopes_make.read_float(l[0]))   # eV
                d_energy = float(isotopes_make.read_float(l[1])) # eV
         
                # Second row
                n = n + 1
                l, mat, mf, mt, row_num = isotopes_make.read_row(blocks_457[n])
        
                intensity_endf = float(isotopes_make.read_float(l[2]))
                d_intensity_endf = float(isotopes_make.read_float(l[3]))
                intensity = nfact * float(isotopes_make.read_float(l[2]))
                d_intensity = nfact * float(isotopes_make.read_float(l[3]))

                # Third row                
                n = n + 1
                l, mat, mf, mt, row_num = isotopes_make.read_row(blocks_457[n])
            
                tot_int_conv_coeff = float(isotopes_make.read_float(l[0]))
                d_tot_int_conv_coeff = float(isotopes_make.read_float(l[1]))
                k_shell_int_conv_coeff = float(isotopes_make.read_float(l[2]))
                d_k_shell_int_conv_coeff = float(isotopes_make.read_float(l[3]))
                l_shell_int_conv_coeff = float(isotopes_make.read_float(l[4]))
                d_l_shell_int_conv_coeff = float(isotopes_make.read_float(l[5]))

               
          
                gammas.append({
                  'energy': energy,
                  'd_energy': d_energy,
                  'n_factor': nfact,
                  'intensity_endf': intensity_endf,
                  'd_intensity_endf': d_intensity_endf,
                  'intensity': intensity,
                  'd_intensity': d_intensity,
                  'tot_int_conv_coeff': tot_int_conv_coeff,
                  'd_tot_int_conv_coeff': d_tot_int_conv_coeff,
                  'k_shell_int_conv_coeff': k_shell_int_conv_coeff,
                  'd_k_shell_int_conv_coeff': d_k_shell_int_conv_coeff,
                  'l_shell_int_conv_coeff': l_shell_int_conv_coeff,
                  'd_l_shell_int_conv_coeff': d_l_shell_int_conv_coeff,
                })
                
                # Store in array
                gammas_array[gn, 0] = energy
                gammas_array[gn, 1] = intensity
                

                #if(isotope['protons'] == 27 and isotope['nucleons'] == 55):
                #  print(gn)

                # Increment gn
                gn = gn + 1
              
              
          except:
            pass
          
          
        # Increment  
        n = n + 1

    # STORE

    Z = isotope['protons']
    A = isotope['nucleons']
    M = isotope['metastable']

    # List of all isotopes
    isotopes_make.list.append([Z,A,M])

    # List tree
    if(Z not in isotopes_make.list_tree.keys()):
      isotopes_make.list_tree[Z] = {}
    if(A not in isotopes_make.list_tree[Z].keys()):
      isotopes_make.list_tree[Z][A] = []  
    isotopes_make.list_tree[Z][A].append(M)
    
    # Store Isotopes
    if(Z not in isotopes_make.isotopes.keys()):
      isotopes_make.isotopes[Z] = {}
    if(A not in isotopes_make.isotopes[Z].keys()):
      isotopes_make.isotopes[Z][A] = {}  
    isotopes_make.isotopes[Z][A][M] = isotope

    # Stable / Unstable
    if(isotope['stable']):
      if(Z not in isotopes_make.stable.keys()):
        isotopes_make.stable[Z] = []
      if(A not in isotopes_make.stable[Z]):
        isotopes_make.stable[Z].append(A) 
    else:
      if(Z not in isotopes_make.unstable.keys()):
        isotopes_make.unstable[Z] = []
      if(A not in isotopes_make.unstable[Z]):
        isotopes_make.unstable[Z].append(A) 

    # Observationally stable
    if(isotope['stable'] or isotope['natural_abundance']>0.0):
      if(Z not in isotopes_make.observationally_stable.keys()):
        isotopes_make.observationally_stable[Z] = []
      if(A not in isotopes_make.observationally_stable[Z]):
        isotopes_make.observationally_stable[Z].append(A) 



    # Store Gammas
    if(Z not in isotopes_make.gammas.keys()):
      isotopes_make.gammas[Z] = {}
    if(A not in isotopes_make.gammas[Z].keys()):
      isotopes_make.gammas[Z][A] = {}  
    isotopes_make.gammas[Z][A][M] = gammas

    if(Z not in isotopes_make.gammas_array.keys()):
      isotopes_make.gammas_array[Z] = {}
    if(A not in isotopes_make.gammas_array[Z].keys()):
      isotopes_make.gammas_array[Z][A] = {}  
    isotopes_make.gammas_array[Z][A][M] = gammas_array

    code = M * 1000000 + Z * 1000 + A 
    if(code not in isotopes_make.valid_codes):
      isotopes_make.valid_codes.append(code)
    if(isotope['stable']):
      if(code not in isotopes_make.stable_codes):
        isotopes_make.stable_codes.append(code)
    else:
      if(code not in isotopes_make.unstable_codes):
        isotopes_make.unstable_codes.append(code)
    if(isotope['stable'] or isotope['natural_abundance']>0.0):
      if(code not in isotopes_make.observationally_stable_codes):
        isotopes_make.observationally_stable_codes.append(code)
    if(isotope['metastable'] > 0):
      isotopes_make.metastable_codes.append(code)
        

    #isotopes_make.isotopes
    #print(isotope['key'], isotope['metastable'])

    """
    # Store
    isotopes.jeffdata[isotope['key']] = isotope    

    # Add to isotopes
    if(isotope['protons'] not in isotopes.isotopes.keys()):
      isotopes.isotopes[isotope['protons']] = {
              'mass': 0.0,
              'element': isotope['element'],
              'stable': [],
              'unstable': [],
              }
    if(isotope['stable']):
      isotopes.isotopes[isotope['protons']]['stable'].append(isotope['key'])
      isotopes.isotopes[isotope['protons']]['mass'] = isotopes.isotopes[isotope['protons']]['mass'] + isotope['mass_amu'] * isotope['natural_abundance']
    else:
      isotopes.isotopes[isotope['protons']]['unstable'].append(isotope['key'])
    """  
  
  








  @staticmethod
  def read_row(row):   
    l = []
    l.append(row[0:11])
    l.append(row[11:22])
    l.append(row[22:33])
    l.append(row[33:44])
    l.append(row[44:55])
    l.append(row[55:66]) 
    mat = int(row[66:70])
    mf = int(row[70:72])
    mt = int(row[72:75])
    row_num = int(row[75:])    
    return l, mat, mf, mt, row_num
      
  @staticmethod
  def read_float(inp):
    out = ''
    if('e' not in inp.lower()):
      for i in range(len(inp)):
        if(i>1 and inp[i] == '+'):
          out = out + 'e'
        elif(i>1 and inp[i] == '-'):
          out = out + 'e-'
        elif(inp[i] != ' '):
          out = out + inp[i]
    else:
      out = inp
    return float(out)


  @staticmethod
  def read_int(inp):
    out = ''
    if('e' not in inp.lower()):
      for i in range(len(inp)):
        if(i>1 and inp[i] == '+'):
          out = out + 'e'
        elif(i>1 and inp[i] == '-'):
          out = out + 'e-'
        elif(inp[i] != ' '):
          out = out + inp[i]
    else:
      out = inp
    return int(numpy.floor(float(out)))




  @staticmethod
  def read_isotope_code(code):
    protons = int(numpy.floor(code/1000))
    nucleons = int(code - 1000 * protons)
    neutrons = nucleons - protons
    return protons, neutrons, nucleons
   
  @staticmethod
  def isotope_code(code):
    metastable = int(numpy.floor(code/1000000))
    code = code - metastable * 1000000
    protons = int(numpy.floor(code/1000))
    nucleons = int(code - 1000 * protons)
    neutrons = nucleons - protons
    return metastable, protons, neutrons, nucleons 

  













isotopes_make.run()




