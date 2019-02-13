#!/usr/bin/env python3

import sys
sys.path.append('../')

from iplot import *
import numpy as np

my_graph = graph('Cosine "bullet"')

x_0 = 0; x_1 = 2*np.pi
x_list = [(i / 20)% (2*np.pi) for i in range(100)] #5 loops, 20 points long

# Plot cos function to default line (default color is blue)
# No need for x values; completely automatic
my_graph.plot(f=np.cos,line=True,xlims=(x_0,x_1))

# Plot yellow bullet
my_graph.newline(color='y')
for x in x_list:
    rate(200)
    my_graph.plot(x=x,y=np.cos(x),num_points=1,line=False)
