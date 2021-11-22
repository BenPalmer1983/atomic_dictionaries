from pz import pz
from isotopes import isotopes
import os
import numpy
import matplotlib.pyplot as plt
import time



class talys:

  path_talys = "data"
  path_isotopes = "data/isotopes.pz"
  loaded = False


  @staticmethod
  def info():
    talys.load()
    print(talys.d['info'])

  @staticmethod
  def help():
    talys.load()
    print(talys.d['help'])


  @staticmethod
  def set(path_talys, path_isotopes):
    talys.path_talys = path_talys
    talys.path_isotopes = path_isotopes
    isotopes.set(path_isotopes)

  @staticmethod
  def load():
    if(talys.loaded == False):
      #talys.d = pz.load(talys.path_talys)
      talys.d = {}
      talys.d['info'] = pz.load(talys.path_talys + "/info.pz", 'lzma')
      talys.d['metastable'] = pz.load(talys.path_talys + "/metastable.pz", 'lzma')
      talys.d['levels'] = pz.load(talys.path_talys + "/levels.pz", 'lzma')
      talys.d['residual_xs'] = pz.load(talys.path_talys + "/residual_xs.pz", 'lzma')
      talys.d['particle_xs'] = pz.load(talys.path_talys + "/particle_xs.pz", 'lzma')
      talys.d['elastic_xs'] = pz.load(talys.path_talys + "/elastic_xs.pz", 'lzma')
      talys.d['nonelastic_xs'] = pz.load(talys.path_talys + "/nonelastic_xs.pz", 'lzma')
      talys.loaded = True

  ############################
  # Residuals
  ############################

  @staticmethod
  def get_residual_targets(projectile):
    talys.load()
    residual_targets = []
    for Z in talys.d['residual_xs'][projectile].keys():
      for A in talys.d['residual_xs'][projectile][Z].keys():
        for M in talys.d['residual_xs'][projectile][Z][A].keys():
          target = isotopes.inp(Z, A, M)
          residual_targets.append(target['isotope_code'])
    return residual_targets    
 
  @staticmethod
  def get_residuals(projectile, Z, A=None, M=None):
    talys.load()
    target = isotopes.inp(Z, A, M)
    Z = target['Z']
    A = target['A']
    M = target['M']
    if(projectile not in talys.d['residual_xs'].keys()):
      return None
    if(Z not in talys.d['residual_xs'][projectile].keys()):
      return None
    if(A not in talys.d['residual_xs'][projectile][Z].keys()):
      return None
    if(M not in talys.d['residual_xs'][projectile][Z][A].keys()):
      return None
    return talys.d['residual_xs'][projectile][Z][A][M].keys()

  @staticmethod
  def get_rxs(projectile, in_a, in_b=None, in_c=None, in_d=None, in_e=None, in_f=None):
    talys.load()
    isotope_a, isotope_b = isotopes.get_codes(in_a, in_b, in_c, in_d, in_e, in_f) 
    result = {}
    a = isotopes.inp(isotope_a)
    Za = a['Z']
    Aa = a['A']
    Ma = a['M']
    
    if(not talys.exists('residual_xs', projectile, Za, Aa, Ma)):
      return None

    if(isotope_b != None):
      b = isotopes.inp(isotope_b)
      Zb = b['Z']
      Ab = b['A']
      Mb = b['M']

      if(not talys.exists('residual_xs', projectile, Za, Aa, Ma, isotope_b)):
        return None
      result[isotope_b] = talys.d['residual_xs'][projectile][Za][Aa][Ma][isotope_b]

    else:
      result = talys.d['residual_xs'][projectile][Za][Aa][Ma]

    return result

  

  ############################
  # Particles
  ############################

  @staticmethod
  def get_particle_targets(projectile):
    talys.load()
    particle_targets = []
    for Z in talys.d['particle_xs'][projectile].keys():
      for A in talys.d['particle_xs'][projectile][Z].keys():
        for M in talys.d['particle_xs'][projectile][Z][A].keys():
          target = isotopes.inp(Z, A, M)
          particle_targets.append(target['isotope_code'])
    return particle_targets    

  @staticmethod
  def get_particles(projectile, Z, A=None, M=None):
    talys.load()
    target = isotopes.inp(Z, A, M)
    Z = target['Z']
    A = target['A']
    M = target['M']
    if(projectile not in talys.d['particle_xs'].keys()):
      return None
    if(Z not in talys.d['particle_xs'][projectile].keys()):
      return None
    if(A not in talys.d['particle_xs'][projectile][Z].keys()):
      return None
    if(M not in talys.d['particle_xs'][projectile][Z][A].keys()):
      return None
    return talys.d['particle_xs'][projectile][Z][A][M].keys()



  @staticmethod
  def get_pxs(projectile, in_a, in_b=None, in_c=None, in_d=None):
    talys.load()
    result = {}

    if(in_a != None and in_b == None):
      target_code = in_a
      particle = None
    elif(in_a != None and in_b != None and in_c == None):
      target_code = in_a
      particle = in_b.lower()
    elif(in_a != None and in_b != None and in_c != None and in_d == None):
      target_code = isotopes.get_code(in_a, in_b, in_c)
      particle = None
    elif(in_a != None and in_b != None and in_c != None and in_d != None):
      target_code = isotopes.get_code(in_a, in_b, in_c)
      particle = in_d.lower()
    else:
      return None

    a = isotopes.inp(target_code)
    Za = a['Z']
    Aa = a['A']
    Ma = a['M']
    
    if(not talys.exists('particle_xs', projectile, Za, Aa, Ma)):
      return None

    if(particle != None):
      if(not talys.exists('particle_xs', projectile, Za, Aa, Ma, particle)):
        return None
      result[particle] = talys.d['particle_xs'][projectile][Za][Aa][Ma][particle]
    else:
      result = talys.d['particle_xs'][projectile][Za][Aa][Ma]
    return result




  ############################
  # Plot Residuals
  ############################


  @staticmethod
  def plot_rxs(path, projectile, in_a, in_b=None, in_c=None, in_d=None, in_e=None, in_f=None):
    talys.load()
    target_code, residual_code = isotopes.get_codes(in_a, in_b, in_c, in_d, in_e, in_f) 

    rxs = talys.get_rxs(projectile, target_code, residual_code)
    
    linestyle = ["solid", "dashed", "dashdot", "dotted"]
    colours = ["#009933","#CC9900","#0033CC","#CC3300","#6600CC","#000066","#333300","#FF0000","#FF9966","#009999","#993366","#66FF33","#FF0066","#00FFFF","#FFFF00","#990000","#663300"]
    
    plt.figure(figsize=(12,8))
    n = 0
    for residual_code in rxs.keys():     
      rp_xs = rxs[residual_code]
      t_hr = isotopes.get_hr(target_code) 
      r_hr = isotopes.get_hr(residual_code) 
      label = t_hr.strip() + " - " + r_hr.strip()
      if(rp_xs is not None):
        lc = n % len(colours)
        ls = int(numpy.floor(n / len(colours))) % len(linestyle)

        plt.plot(rp_xs[:,0], rp_xs[:,1], label=label, color=colours[lc], linestyle=linestyle[ls])
        n = n + 1
    cols = (max(1,int(numpy.floor(len(rxs)/10))))

    talys.make_dir(path)
    if(len(rxs)>1):
      file_name = "rxs_" + str(target_code) + "_all.eps"
    else:
      file_name = "rxs_" + str(target_code) + "_" + str(residual_code) + ".eps"
    file_path = path + "/" + file_name

    plt.xlabel('Energy (MeV)')
    plt.ylabel('Cross-section (Barns)')
    plt.title('Target-Residual Cross Section')
    plt.legend(fontsize="xx-small", ncol=cols)
    plt.grid(True)
    plt.savefig(file_path, type='eps')
    plt.close('all') 


  @staticmethod
  def plot_rxs_all(path):
    talys.load()
    for projectile in talys.d['residual_xs'].keys():
      targets = talys.get_residual_targets(projectile)
      talys.make_dir(path + "/" + projectile.strip())
      for t in targets:
        talys.plot_rxs(path + "/" + projectile.strip(), projectile, t)






  ############################
  # Plot Particles
  ############################


  @staticmethod
  def plot_pxs(path, projectile, in_a, in_b=None, in_c=None, in_d=None):
    talys.load()

    if(in_a != None and in_b == None):
      target_code = in_a
      particle = None
    elif(in_a != None and in_b != None and in_c == None):
      target_code = in_a
      particle = in_b.lower()
    elif(in_a != None and in_b != None and in_c != None and in_d == None):
      target_code = isotopes.get_code(in_a, in_b, in_c)
      particle = None
    elif(in_a != None and in_b != None and in_c != None and in_d != None):
      target_code = isotopes.get_code(in_a, in_b, in_c)
      particle = in_d.lower()
    else:
      return None

    pxs = talys.get_pxs(projectile, target_code, particle)

    
    linestyle = ["solid", "dashed", "dashdot", "dotted"]
    colours = ["#009933","#CC9900","#0033CC","#CC3300","#6600CC","#000066","#333300","#FF0000","#FF9966","#009999","#993366","#66FF33","#FF0066","#00FFFF","#FFFF00","#990000","#663300"]
    
    plt.figure(figsize=(12,8))
    n = 0
    for particle in pxs.keys():     
      pp_xs = pxs[particle]
      t_hr = isotopes.get_hr(target_code) 
      r_hr = particle
      label = t_hr.strip() + " - " + r_hr.strip()
      if(pp_xs is not None):
        lc = n % len(colours)
        ls = int(numpy.floor(n / len(colours))) % len(linestyle)

        plt.plot(pp_xs[:,0], pp_xs[:,1], label=label, color=colours[lc], linestyle=linestyle[ls])
        n = n + 1
    cols = (max(1,int(numpy.floor(len(pxs)/10))))

    talys.make_dir(path)
    if(len(pxs)>1):
      file_name = "pxs_" + str(target_code) + "_all.eps"
    else:
      file_name = "pxs_" + str(target_code) + "_" + str(particle) + ".eps"
    file_path = path + "/" + file_name

    plt.xlabel('Energy (MeV)')
    plt.ylabel('Cross-section (Barns)')
    plt.title('Target-Residual Cross Section')
    plt.legend(fontsize="xx-small", ncol=cols)
    plt.grid(True)
    plt.savefig(file_path, type='eps')
    plt.close('all') 


  @staticmethod
  def plot_pxs_all(path):
    talys.load()
    for projectile in talys.d['particle_xs'].keys():
      targets = talys.get_particle_targets(projectile)
      talys.make_dir(path + "/" + projectile.strip())
      for t in targets:
        talys.plot_pxs(path + "/" + projectile.strip(), projectile, t)


  ############################
  # Search XS
  ############################

  """
  Enter energy e in MeV
  Projectile type (p etc)
  Either target isotope or target and residual
  """

  @staticmethod
  def search_rxs(e, projectile, in_a, in_b=None, in_c=None, in_d=None, in_e=None, in_f=None):
    talys.load()
    target_code, residual_code = isotopes.get_codes(in_a, in_b, in_c, in_d, in_e, in_f) 
    rxs = talys.get_rxs(projectile, target_code, residual_code)
    results = {}    

    if(rxs == None):
      return results

    if(residual_code != None):
      rp_xs = rxs[residual_code]
      e_xs = talys.get_xs(e, rp_xs)
      if(not (e_xs == None or e_xs == 0.0)):
        results[residual_code] = e_xs
    else:
      for residual_code in rxs.keys():     
        rp_xs = rxs[residual_code]
        e_xs = talys.get_xs(e, rp_xs)
        if(not (e_xs == None or e_xs == 0.0)):
          results[residual_code] = e_xs
    
    return results

  @staticmethod
  def get_xs(e, xs):
    if(e >= xs[0,0] and e <= xs[-1,0]):
      n = int(((e - xs[0,0])  / (xs[-1,0] - xs[0,0])) * len(xs[:,0]))
      if(n < 0):
        n = 0
      if(n>len(xs[:,0])-1):
        n = len(xs[:,0])-1
      return xs[n,1] + (xs[n+1,1] - xs[n,1]) * ((e - xs[n,0]) / (xs[n+1,0] - xs[n,0]))
    else:
      return None
     

  ############################
  # Misc
  ############################

  @staticmethod
  def exists(lib, projectile, Z, A, M, code=None):    
    if(projectile not in talys.d[lib].keys()):
      return False
    if(Z not in talys.d[lib][projectile].keys()):
      return False
    if(A not in talys.d[lib][projectile][Z].keys()):
      return False
    if(M not in talys.d[lib][projectile][Z][A].keys()):
      return False
    if(code != None):
      if(code not in talys.d[lib][projectile][Z][A][M].keys()):
        return False
    return True

  @staticmethod
  def get_file_path(file_path):
    file_path = file_path.strip()
    if(file_path[0] != "/"):
      root = os.getcwd()
      file_path = root + "/" + file_path
    file_path = file_path.split("/")
    path = ""
    for i in range(1,len(file_path) - 1):
      path = path + "/" + file_path[i]
    return path

  @staticmethod
  def get_path(path):
    path = path.strip()
    if(path[0] != "/"):
      root = os.getcwd()
      path = root + "/" + path
    return path

  @staticmethod
  def make_dir(dir):
    dirs = dir.split("/")
    try:
      dir = ''
      for i in range(len(dirs)):
        dir = dir + dirs[i]
        if(not os.path.exists(dir) and dir.strip() != ''):
          os.mkdir(dir) 
        dir = dir + '/'
      return True
    except:
      return False


  @staticmethod
  def test():
    print("Test")
    print("Load data")
    st = time.time()
    talys.set("../data/talys", "../data/isotopes.pz") 
    talys.load()
    print("Load time: ", time.time() - st)


    """
    print()
    print("Residual targets")
    targets = talys.get_residual_targets('p')
    print(targets)


    print()
    print("Fe56 Residual XS")
    pxs = talys.get_rxs('p', 26, 56, 0)
    print(pxs)


    print()
    print("Plot 56fe_55co")
    talys.plot_rxs('56fe_55co', 'p', 26, 56, 0, 25, 55, 0)


    print()
    print("Particle targets")
    targets = talys.get_particle_targets('p')
    print(targets)

    print()
    print("Fe56 Particles")
    particles = talys.get_particles('p', 26, 56)
    print(particles)


    print()
    print("Fe56 Particle XS")
    pxs = talys.get_pxs('p', 26, 56, 0)
    print(pxs)

    print()
    print("Fe56 Particle XS Alpha")
    pxs = talys.get_pxs('p', 26, 56, 0, 'alpha')
    print(pxs)


    print()
    print("Plot 56fe alpha")
    talys.plot_pxs('56fe_alpha', 'p', 26, 56, 0, 'alpha')


    print()
    print("Plot 56fe particles")
    talys.plot_pxs('56fe_particles', 'p', 26, 56, 0)
    

    print()
    print("Plot all residuals")
    talys.plot_rxs_all("all_residual_xs")


    print()
    print("Plot all particles")
    talys.plot_pxs_all("all_particle_xs")
    """

    talys.search_rxs(2.1, 'p', 26056)
    print()
    talys.search_rxs(2.1002, 'p', 26056)
    print()
    results = talys.search_rxs(22.095666, 'p', 26056)
    print(results)
    results = talys.search_rxs(22.095666, 'p', 26, 56, 0)
    print(results)

    results = talys.search_rxs(22.095666, 'p', 26056, 27056)
    print(results)

    #plot_pxs


def main():
  talys.test()

if __name__ == "__main__":
    main()    
