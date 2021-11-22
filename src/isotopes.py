import numpy
from pz import pz

class isotopes:

  path = "../dictionaries/isotopes.pz"
  loaded = False
  d = None
  v = True

  @staticmethod
  def set(path):
    isotopes.path = path
    isotopes.load()


  @staticmethod
  def load():
    if(isotopes.loaded == False):
      isotopes.d = pz.load(isotopes.path, 'lzma')
      isotopes.loaded = True


  @staticmethod 
  def info():
    isotopes.load()
    print("Name:        ", end="")
    print(isotopes.d['info']['name'])
    print("Source:      ", end="")
    print(isotopes.d['info']['source'])
    print("Source File: ", end="")
    print(isotopes.d['info']['source_file'])
 
  @staticmethod   
  def help():
    isotopes.load()
    print(isotopes.d['info']['help'])



  @staticmethod 
  def summary():
    isotopes.load()
    print("Isotope count:       ", len(isotopes.d['valid_codes']))
    print("Stable isotopes:     ", len(isotopes.d['stable_codes']))
    print("Unstable isotopes:   ", len(isotopes.d['unstable_codes']))
    print("Metastable isotopes: ", len(isotopes.d['metastable_codes']))
    print()

    
  #########################################################
  # Get isotope data
  #########################################################

  @staticmethod
  def get(in_a, in_b=None, in_c=None, check=True):
    isotopes.load()
    inp = isotopes.inp(in_a, in_b, in_c, check)
    isotope_code, Z, A, M = inp['code'], inp['Z'], inp['A'], inp['M']
    if(Z not in isotopes.d['isotopes'].keys()):
      return None
    if(A not in isotopes.d['isotopes'][Z].keys()):
      return None
    if(M not in isotopes.d['isotopes'][Z][A].keys()):
      return None
    return isotopes.d['isotopes'][Z][A][M]



  #########################################################
  # Get list
  #########################################################

  @staticmethod
  def get_list():
    isotopes.load()
    return isotopes.d['list']

  @staticmethod    
  def get_list_len():
    isotopes.load()
    return len(isotopes.d['list'])

  @staticmethod
  def get_list_tree():
    isotopes.load()
    return isotopes.d['list_tree']
 
  @staticmethod     
  def get_list_tree_len():
    isotopes.load()
    return len(isotopes.d['list_tree'])



  #########################################################
  # Get stable/unstable
  #########################################################

  @staticmethod
  def get_stable(Z=None, obs=True):
    isotopes.load()
    Z = isotopes.get_z(Z)
    d = 'stable'
    if(obs):
      d = 'observationally_stable'
    if(Z is None):
      return isotopes.d[d]  
    Z = isotopes.get_z(Z)
    if(Z is None):
      return None
    if(Z not in isotopes.d[d].keys()):
      return None
    return isotopes.d[d][Z]


  @staticmethod
  def get_stable_code(Z=None):
    isotopes.load()
    Z = isotopes.get_z(Z)
    if(Z == None):
      return None
    A_list = isotopes.get_stable(Z)
    if(isotopes.check_none(A_list)):
      return None
    codes = []
    for A in A_list:
      codes.append(isotopes.get_code(Z,A,0))
    return codes


  @staticmethod
  def get_stable_abundances(Z=None, obs=True):
    isotopes.load()
    Z = isotopes.get_z(Z)
    d = 'stable'
    if(obs):
      d = 'observationally_stable'
    if(Z is None):
      return None
    if(Z not in isotopes.d[d].keys()):
      return None
    A_list = isotopes.d[d][Z]
    result = {}
    for A in A_list:
      icode = isotopes.get_code(Z,A,0)
      Z,A,M = isotopes.get_zam(icode)
      result[icode] = isotopes.d['isotopes'][Z][A][M]['natural_abundance']
    return result


  @staticmethod
  def get_unstable(Z=None):
    isotopes.load()
    if(Z is None):
      return isotopes.d['unstable']  
    Z = isotopes.get_z(Z)
    if(Z is None):
      return None
    if(Z not in isotopes.d['unstable'].keys()):
      return None
    return isotopes.d['unstable'][Z]
   



  #########################################################
  # Get gammas
  #########################################################

  @staticmethod
  def get_gammas(in_a, in_b=None, in_c=None, check=True):
    isotopes.load()
    inp = isotopes.inp(in_a, in_b, in_c, check)
    isotope_code, Z, A, M = inp['code'], inp['Z'], inp['A'], inp['M']
    if(Z not in isotopes.d['gammas'].keys()):
      return None
    if(A not in isotopes.d['gammas'][Z].keys()):
      return None
    if(M not in isotopes.d['gammas'][Z][A].keys()):
      return None
    return isotopes.d['gammas'][Z][A][M]


  @staticmethod
  def get_gammas_array(in_a, in_b=None, in_c=None, check=True):
    isotopes.load()
    inp = isotopes.inp(in_a, in_b, in_c, check)
    isotope_code, Z, A, M = inp['code'], inp['Z'], inp['A'], inp['M']
    if(Z not in isotopes.d['gammas_array'].keys()):
      return None
    if(A not in isotopes.d['gammas_array'][Z].keys()):
      return None
    if(M not in isotopes.d['gammas_array'][Z][A].keys()):
      return None
    return isotopes.d['gammas_array'][Z][A][M]



  #########################################################
  # Misc
  ######################################################### 
  
  @staticmethod
  def is_valid(in_a, in_b=None, in_c=None, check=True):
    inp = isotopes.inp(in_a, in_b, in_c, check)
    isotope_code, Z, A, M = inp['code'], inp['Z'], inp['A'], inp['M']
    if(isotope_code in isotopes.d['valid_codes']):
      return True
    return False

  @staticmethod
  def get_z(symbol):
    isotopes.load()
    if(symbol == None):
      return None
    try:
      e = int(symbol)
    except:
      e = symbol.strip().capitalize()        
    if(e not in isotopes.d['symbols'].keys()):
      return None
    if(isinstance(e, int)): 
      return e
    return isotopes.d['symbols'][e]

  @staticmethod
  def get_symbol(z):
    isotopes.load()
    try:
      e = int(z)
    except:
      e = z.strip().capitalize()        
    if(e not in isotopes.d['symbols'].keys()):
      return None
    if(not isinstance(e, int)): 
      return e
    return isotopes.d['symbols'][e]

  @staticmethod
  def get_zam(code):
    try:
      code = int(code)
    except:
      return None
    M = int(numpy.floor(code/1000000))
    code = code - M * 1000000
    Z = int(numpy.floor(code/1000))
    A = int(code - 1000 * Z)
    return Z, A, M 

  @staticmethod
  def get_code(Z,A=None,M=None):
    if(Z == None):
      return None
    if(A == None and M == None):
      try:
        code = int(Z)
      except:
        return None
      return code
    if(M == None):
      M = 0
    try:
      Z = isotopes.get_z(Z)
      Z = int(Z)
      A = int(A)
      M = int(M)
    except:
      return None
    return M * 1000000 + Z * 1000 + A 

  @staticmethod
  def get_codes(in_a, in_b=None, in_c=None, in_d=None, in_e=None, in_f=None):
    code_a = None
    code_b = None
    if(in_b is None):
      isotope_a_Z, isotope_a_A, isotope_a_M = isotopes.get_zam(in_a)
      code_a = isotopes.get_code(isotope_a_Z, isotope_a_A, isotope_a_M)
      code_b = None
    elif(in_c==None):
      isotope_a_Z, isotope_a_A, isotope_a_M = isotopes.get_zam(in_a)
      isotope_b_Z, isotope_b_A, isotope_b_M = isotopes.get_zam(in_b)
      code_a = isotopes.get_code(isotope_a_Z, isotope_a_A, isotope_a_M)
      code_b = isotopes.get_code(isotope_b_Z, isotope_b_A, isotope_b_M)
    elif(in_d==None):
      plot_all = True
      isotope_a_Z, isotope_a_A, isotope_a_M = in_a, in_b, in_c
      code_a = isotopes.get_code(isotope_a_Z, isotope_a_A, isotope_a_M)
      code_b = None
    elif(not (in_a==None or in_b==None or in_c==None or in_d==None or in_e==None or in_f==None)):
      isotope_a_Z, isotope_a_A, isotope_a_M = in_a, in_b, in_c
      isotope_b_Z, isotope_b_A, isotope_b_M = in_d, in_e, in_f
      code_a = isotopes.get_code(isotope_a_Z, isotope_a_A, isotope_a_M)
      code_b = isotopes.get_code(isotope_b_Z, isotope_b_A, isotope_b_M)
    return code_a, code_b


  @staticmethod
  def get_hr(in_a, in_b=None, in_c=None):
    isotopes.load()
    if(in_b == None):
      Z, A, M = isotopes.get_zam(in_a)
    else:
      Z, A, M = in_a, in_b, in_c
    if(Z not in isotopes.d['symbols'].keys()):
      return None
    elif(isotopes.d['symbols'][Z] == None):
      return None
    else:
      meta = ""
      if(M > 0):
        meta = "(meta " + str(M) + ")"
      return str(A) + isotopes.d['symbols'][Z] + meta


  @staticmethod
  def get_dir_hr(in_a, in_b=None, in_c=None):
    isotopes.load()
    if(in_b == None):
      Z, A, M = isotopes.get_zam(in_a)
    else:
      Z, A, M = in_a, in_b, in_c
    if(Z not in isotopes.d['symbols'].keys()):
      return None
    elif(isotopes.d['symbols'][Z] == None):
      return None
    else:
      code = isotopes.get_code(Z, A, M)
      meta = ""
      if(M > 0):
        meta = "_meta_" + str(M)
      return str(code) + "_" + str(A) + isotopes.d['symbols'][Z] + meta

  @staticmethod
  def get_printable_name(in_a, in_b=None, in_c=None, check=True):
    isotopes.load()
    inp = isotopes.inp(in_a, in_b, in_c, check)
    isotope_code, Z, A, M = inp['code'], inp['Z'], inp['A'], inp['M']
    meta = ""
    if(M > 0):
      meta = " (meta " + str(M) + ")"
    return str(Z) + " " + inp['symbol'] + " " + str(A) + meta
  

  @staticmethod
  def isotope_table(isotope_list, percentage_list=None, print_out=False):
    if(not isotopes.check_none(percentage_list)):
      if(len(isotope_list) != len(percentage_list)):
        percentage_list = None
    if(not isotopes.check_none(percentage_list)):
      percentage_list, isotope_list = zip(*sorted(zip(percentage_list, isotope_list), reverse=True))
    
    if(isotopes.check_none(percentage_list)):
      percentage_list = []
      for i in range(len(isotope_list)):
        percentage_list.append("-")
     
    out =       "####################################################\n"
    out = out + "                     Isotopes                       \n"
    out = out + "####################################################\n"
    out = out + '  '
    out = out + '{:14}'.format("Isotope")
    out = out + '{:20}'.format("Percentage by Mass")

    out = out + "\n"
    for i in range(len(isotope_list)):
      out = out + '  '
      out = out + '{:14}'.format(isotopes.get_printable_name(isotope_list[i]))
      if(percentage_list[i] == "-"):
        out = out + "-"
      else:
        out = out + '{0:7f}'.format(percentage_list[i])
      out = out + "\n"

      
    if(print_out):
      print(out)
    return out


  #########################################################
  # Decay Data
  #########################################################

  @staticmethod
  def get_decay_modes(in_a, in_b=None, in_c=None, check=True):
    isotopes.load()
    inp = isotopes.inp(in_a, in_b, in_c, check)
    isotope_code, Z, A, M = inp['code'], inp['Z'], inp['A'], inp['M']
    if(isotope_code in isotopes.d['unstable_codes']):
      return isotopes.d['isotopes'][Z][A][M]['decay_modes']

  @staticmethod
  def is_stable(Z, A=None, M=None, obs=True):
    isotope_code = isotopes.get_code(Z,A,M)
    Z, A, M = isotopes.get_zam(isotope_code)
    if(obs):
      if(isotope_code in isotopes.d['observationally_stable_codes']):
        return True      
    else:
      if(isotope_code in isotopes.d['stable_codes']):
        return True
    return False

  @staticmethod
  def is_unstable(Z, A=None, M=None):
    isotope_code = isotopes.get_code(Z,A,M)
    Z, A, M = isotopes.get_zam(isotope_code)
    if(isotope_code in isotopes.d['unstable_codes']):
      return True
    return False

  @staticmethod
  def is_metastable(Z, A=None, M=None):
    isotope_code = isotopes.get_code(Z,A,M)
    Z, A, M = isotopes.get_zam(isotope_code)
    if(isotope_code in isotopes.d['metastable_codes']):
      return True
    return False






  @staticmethod
  def inp(in_a, in_b=None, in_c=None, check=True):
    isotopes.load()
    out = {
          'ok': False,
          'valid': False,
          'Z': None,
          'A': None,
          'M': None,
          'symbol': None,
          'isotope_code': None,
          'code': None,
          }
    if(in_a is None):
      return out
    if(not isinstance(in_a, int)):
      in_a = in_a.strip().capitalize()
      if(in_a in isotopes.d['symbols'].keys()):
        in_a = isotopes.d['symbols'][in_a]
      else:
        return out
    if(in_a != None and in_b == None and in_c == None):
      Z, A, M = isotopes.get_zam(in_a)
      isotope_code = isotopes.get_code(Z, A, M)
    elif(in_a != None and in_b != None and in_c == None):
      try:
        Z, A, M = in_a, in_b, 0
        isotope_code = isotopes.get_code(Z, A, M)
      except:
        return out
    elif(in_a != None and in_b != None and in_c != None):
      try:
        Z, A, M = in_a, in_b, in_c
        isotope_code = isotopes.get_code(Z, A, M)
      except:
        return out
    else:
      return out
    try:
      out['Z'], out['A'], out['M'] = Z, A, M
      out['code'] = isotope_code
      out['isotope_code'] = isotope_code
      out['symbol'] = isotopes.d['symbols'][Z]
      if(check):
        if(isotope_code in isotopes.d['valid_codes']):
          out['ok'] = True
          out['valid'] = True
      else:
        out['ok'] = True
      return out
    except:
      return out


  #########################################################
  # Get isotope properties
  #########################################################
   
  def get_natural_abundance(Z,A=None,M=None):
    isotopes.load()
    icode = isotopes.get_code(Z,A,M)
    if(icode == None):
      return None
    if(icode not in isotopes.d['valid_codes']):
      return None
    Z, A, M = isotopes.get_zam(icode)
    return isotopes.d['isotopes'][Z][A][M]['natural_abundance']

  def get_mass_amu(Z,A=None,M=None):
    isotopes.load()
    icode = isotopes.get_code(Z,A,M)
    if(icode == None):
      return None
    if(icode not in isotopes.d['valid_codes']):
      return None
    Z, A, M = isotopes.get_zam(icode)
    return isotopes.d['isotopes'][Z][A][M]['mass_amu']

  def get_decay_constant(Z,A=None,M=None):
    isotopes.load()
    icode = isotopes.get_code(Z,A,M)
    if(icode == None):
      return None
    if(icode not in isotopes.d['valid_codes']):
      return None
    Z, A, M = isotopes.get_zam(icode)
    return isotopes.d['isotopes'][Z][A][M]['decay_constant']

  def get_half_life(Z,A=None,M=None):
    isotopes.load()
    icode = isotopes.get_code(Z,A,M)
    if(icode == None):
      return None
    if(icode not in isotopes.d['valid_codes']):
      return None
    Z, A, M = isotopes.get_zam(icode)
    return isotopes.d['isotopes'][Z][A][M]['half_life']



  #########################################################
  # Misc
  #########################################################
   
  def check_none(inp):
    if(isinstance(inp, list)):
      return False
    if(isinstance(inp, dict)):
      return False
    if(inp == None):
      return True

  #########################################################
  # Test
  #########################################################

  def test():
    print("==================================================")
    print("TESTING")
    print("==================================================")
    print()

    isotopes.info()
    isotopes.help()
    isotopes.summary()


    print(isotopes.inp(26056))
    print(isotopes.inp("Fe", 56))
    print(isotopes.inp("Fe", 52, 1))
    print(isotopes.inp(26, 52, 1))
    print(isotopes.inp(26, 56))
    print()


    print(isotopes.get_stable(26))
    print(isotopes.get_stable("Fe"))
    print(isotopes.get_stable("Pb"))
    print(isotopes.get_stable("U"))
    print(isotopes.get_unstable("U"))
    print(isotopes.get_list_len())
    print(isotopes.get_list_tree_len())
    #print(isotopes.get_gammas("Co", 55, 0))
    print(isotopes.get_gammas_array("Co", 55, 0))


    print(isotopes.get_z(26))
    print(isotopes.get_z("fe"))
    print(isotopes.get_symbol(26))
    print(isotopes.get_symbol("fe"))


    """

    print(isotopes.get_zam(26056))
    print(isotopes.get_zam(1026056))
    print(isotopes.get_zam("A1026056"))
    print(isotopes.get_code(26, 56, 0))
    print(isotopes.get_code(26, 56, 1))
    print(isotopes.get_hr(26, 56, 1))
    print(isotopes.get_hr(26056))
    print(isotopes.get_decay_modes(83214))
    """
    #print(isotopes.zam_code(82,210))
    #print(isotopes.zam_code("Fe",56))
    #print(isotopes.zam_code("26",56))
    #print(isotopes.zam_code("Fe",53,1))
    #print(isotopes.zam_code(26,53,1))

    i = isotopes.get(26, 56)
    print(i)
    print()

    print(isotopes.get_z("Co"))
    print(isotopes.get_code("Co", 55))


    print(isotopes.get_stable_code('Fe'))
    for A in isotopes.d['isotopes'][26]:
      print(isotopes.d['isotopes'][26][A])
      print()

    print(isotopes.d['isotopes'][24][50])
    print()
    print(isotopes.get_stable_code('Cr'))
    print(isotopes.get_stable_abundances('Cr'))
    print(isotopes.get_natural_abundance('Fe', 56))
    print(isotopes.get_mass_amu('Fe', 56))


    print("Isotope Table")
    isotope_list = [26056, 26055, 24054]
    percentage_list = None
    isotopes.isotope_table(isotope_list, percentage_list)
    print()
    isotope_list = [24054, 26056, 26055]
    percentage_list = [10.0,70.0,20.0]
    isotopes.isotope_table(isotope_list, percentage_list)
    print()


def main():
  isotopes.test()

if __name__ == "__main__":
    main()    








