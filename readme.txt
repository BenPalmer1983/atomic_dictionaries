Dictionaries for Python

Elements
Isotopes


Elements
===================

Elements uses data from https://gist.github.com/GoodmanSciences/c2dd862cd38f21b0ad36b8f96b4bf1ee

Dictionary structure

elements.d
  ['info']
    ['name']
    ['source']
    ['source_file']
  ['symbols']
    [protons or symbol]
  ['elements']
    [protons]
      ['z']
      ['symbol']
      ['name']
      ['atomic_mass']
      ['neutrons']
      ['protons']
      ['electrons']
      ['period']
      ['group']
      ['phase']
      ['description']

neutrons are included and have the symbol Nn



Isotopes
===================

Isotopes uses data from JEFF 3.3 via NEA

Dictionary structure

isotopes.d
  ['info']
    ['name']
    ['source']
    ['source_file']
    ['help']
  ['isotopes']
    [Z]
      [A]
        [M]
          ['key']           1000000 * M + 1000 * Z + A
          ['element']
          ['protons']
          ['neutrons']
          ['nucleons']
          ['metastable']
          ['stable']
          ['natural_abundance']
          ['mass_to_neutron']
          ['mass_amu']
          ['half_life']
          ['decay_constant']
          ['decay_modes']
  ['symbols']
    [protons or symbol]
  ['stable']
    [Z]
      [A]
  ['unstable']
    [Z]
      [A]
  ['list']        (list of all [Z,A,M])
  ['list_tree']   
    [Z]
      [A]
        [M]
  ['gammas'] 
    [Z]
      [A]
        [M]
          [['energy']
           ['d_energy']
           ['n_factor']
           ['intensity_endf']
           ['d_intensity_endf']
           ['intensity']
           ['d_intensity']
           ['tot_int_conv_coeff']
           ['d_tot_int_conv_coeff']
           ['k_shell_int_conv_coeff']
           ['d_k_shell_int_conv_coeff']
           ['l_shell_int_conv_coeff']
           ['d_l_shell_int_conv_coeff']]
  ['gammas_array'] 
    [Z]
      [A]
        [M]               (numpy array: energy (eV), intensity (per decay)) 
  ['valid_codes']         (list of valid isotope codes according to JEFF 3.3)
  ['stable_codes']        (list of valid stable isotope codes according to JEFF 3.3)
  ['metastable_codes']    (list of valid metastable isotope codes according to JEFF 3.3) 
  ['unstable_codes']      (list of valid unstable isotope codes according to JEFF 3.3) 















