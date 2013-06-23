#!/usr/bin/python
# -*- coding: utf-8 -*- 
import numpy as np
from scipy import weave

def c_tuple_to_image(tupla, array):
    assert(type(tupla) == type(()))
    assert(type(array) == type(np.array([])))

    codigo_em_c = """
            int max = tupla.length();
            int i, j;
            for (i = 0; i <= 2; i++){
              for (j = 0; j <= 2; j++){
                if (tupla[j + i*3] == 1){
                  printf ("Epa ");
                }
              }
            }
           """
    return weave.inline(codigo_em_c, ['tupla', 'array'])


t = (0,0,0,1,1,1,0,0,0)
n = np.array([])

c_tuple_to_image(t,n)


#for i in xrange(3):
#  for j in xrange(3):
#    print j + i*3



