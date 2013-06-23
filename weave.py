#!/usr/bin/python
# -*- coding: utf-8 -*- 
import numpy as np
from scipy import weave

def c_tuple_to_image(tupla, array):
    assert(type(tupla) == type(()))
    assert(type(array) == type(np.array([])))

    codigo_em_c = """
            int i, j;
            for (i = 0; i < 3; i++){
              for (j = 0; j < 3; j++){
                if (tupla[j + i*3] == 1){
                  array[j + i*3] = 255;
                }
                else{
                  array[j + i*3] = 0;
                }
              }
            }
           """
    return weave.inline(codigo_em_c, ['tupla', 'array'])


t = (0,0,0,1,1,1,0,0,0)
n = np.array([[0,0,0],[0,0,0],[0,0,0]])

c_tuple_to_image(t,n)

print t
print n




