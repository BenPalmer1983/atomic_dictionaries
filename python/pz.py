import bz2
import pickle
import _pickle as cPickle

class pz:

  @staticmethod
  def save(file_path, dict):
    with bz2.BZ2File(file_path, 'w') as f: 
      cPickle.dump(dict, f)
    
  @staticmethod
  def load(file_path):
    data = bz2.BZ2File(file_path, 'rb')
    return cPickle.load(data)
  
