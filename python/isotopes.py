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


  @staticmethod
  def load():
    if(isotopes.loaded == False):
      isotopes.d = pz.load(isotopes.path)
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
    
  #########################################################
  # Get isotope data
  #########################################################

  @staticmethod
  def get(Z,A,M=0):
    isotopes.load()
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
  def get_stable(Z=None):
    isotopes.load()
    if(Z is None):
      return isotopes.d['stable']  
    Z = isotopes.get_z(Z)
    if(Z is None):
      return None
    if(Z not in isotopes.d['stable'].keys()):
      return None
    return isotopes.d['stable'][Z]

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
  def get_gammas(Z,A,M=0):
    isotopes.load()
    Z = isotopes.get_z(Z)
    print(Z)
    if(Z not in isotopes.d['gammas'].keys()):
      return None
    if(A not in isotopes.d['gammas'][Z].keys()):
      return None
    if(M not in isotopes.d['gammas'][Z][A].keys()):
      return None
    return isotopes.d['gammas'][Z][A][M]


  @staticmethod
  def get_gammas_array(Z,A,M=0):
      isotopes.load()
      Z = isotopes.get_z(Z)
      print(Z)
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
  def get_z(symbol):
    isotopes.load()
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
  def get_code(Z,A,M):
    try:
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
    
    i = isotopes.get(26, 56)
    print(i)
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


    print(isotopes.get_zam(26056))
    print(isotopes.get_zam(1026056))
    print(isotopes.get_zam("A1026056"))
    print(isotopes.get_code(26, 56, 0))
    print(isotopes.get_code(26, 56, 1))
    print(isotopes.get_hr(26, 56, 1))
    print(isotopes.get_hr(26056))


isotopes.test()





