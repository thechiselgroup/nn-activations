import sys
import numpy as np

class Decorator():

    def __init__(self,input_id="test"):
        self.count = 0
        self.input_id = input_id

    def reset_count(self):
        self.count = 0

    def torch_decorator(self, fun):
        def wrapper(*args,**kwargs):
            r = fun(*args,**kwargs)
            self.count += 1
            #TODO what is the best way of taking the arg originally and passing it in as a filename?
            #fun.__name__ will be a string like ReLU or conv that identifies the type of function
            filename = sys.argv[2]+""+str(self.count)+"_"+fun.__name__+"_"+self.input_id

            #this can be replaced with any side effect
            np.save(filename, r.data.numpy())

            return r
        return wrapper

