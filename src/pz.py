import bz2
import lzma
import pickle
import _pickle as cPickle

class pz:

  @staticmethod
  def save(file_path, dict, ctype="bz2"):
    if(ctype == "lzma"):
      with lzma.open(file_path, 'w') as f: 
        cPickle.dump(dict, f)
    else:
      with bz2.BZ2File(file_path, 'w') as f: 
        cPickle.dump(dict, f)
    
  @staticmethod
  def load(file_path, ctype="bz2"):
    if(ctype == "lzma"):
      with lzma.open(file_path, 'rb') as file:
        raw_data = file.read()
        data = pickle.loads(raw_data)
      return data
      with lzma.open(file_path) as f:
        data = f.read()
      return cPickle.load(data)
    else:
      data = bz2.BZ2File(file_path, 'rb')
      return cPickle.load(data)
  




