#!/usr/bin/env python3

# Inline animated PLOTting
# by Ben Woods
#
# Fully copyleft! Released under the GNU GPL v3.0 licence.
#
# "Sometimes people have already decided who you are without your story shining through."
#   -  Mae Jemison
#
# Last edit: 13.02.19

import numpy as np
import matplotlib.pyplot as plt
import time

# Refresh rate
def rate(N):
    time.sleep(1/N)
    
class graph:
    '''2D graph class. Makes an animated object.'''
    # Error handling
    def _lims_handling(self,name,lims):
        if lims is not None:
            if type(lims) != tuple:
                # Error handling for non-tuple input
                raise TypeError('Only tuple supported for type({}).'.format(name))
            else:
                if len(lims) != 2:
                    # Error handling for incorrect number of values
                    raise ValueError('Incorrect number of xlims given ({}) instead of 2.'.format(len(lims)))
                else:
                    if False in [(type(i) in [float,int,
                                              *(getattr(np,'int'+j) for j in ['','8','16','32','64']),
                                              *(getattr(np,'float'+j) for j in ['','16','32','64','128'])]) for i in lims]:
                        # Error handling for incorrect type for values
                        raise ValueError('Only float,int supported for values of {}.'.format(name))
                    else:
                        setattr(self,name,lims)
    def __init__(self,title=None):
        # Initialise graph object.
        plt.ion()
        self.fig = plt.figure()
        self.ax = plt.axes()
        self.x = None
        self.y = None
        self.color = 0
        self.__colors = ['b','g','r','c','m','y','k']
        self.title = plt.title(title)
        self.xlims = (-5,5)
        self.ylims = (-5,5)
        self._wait = True
    def newline(self,**kwargs):
        '''Generate a new line to add to the graph. Automatic color cycling.'''
        
        ###
        
        # Cycle through native colors using modulo, or grab the color
        if 'color' in kwargs: 
            if kwargs['color'] is None:
                # Cycle
                self.color = (self.color+1) % 7
            else:
                if kwargs['color'] not in self.__colors:
                    # Unsupported error
                    raise NameError('Color not in self.__colors.')
                else:
                    # Grab color
                    self.color = self.__colors.index(kwargs['color'])
        else:
            # Default setting is to cycle
            self.color = (self.color+1) % 7
        
        # Grab xlims and ylims as optional arguments.
        for name in ['xlims','ylims']:
            if name in kwargs:
                self._lims_handling(name,kwargs[name])
        
        # Reinitialise x and y co-ordinates
        self.x = None
        self.y = None
        
        #Wait on
        self._wait = True
    def plot(self,**kwargs):
        '''Plot to the current line.'''        
        # Grab xlims and ylims as optional arguments.
        for name in ['xlims','ylims']:
            if name in kwargs:
                self._lims_handling(name,kwargs[name])
        
        # Grab x and y values as optional arguments.
        for name in ['x','y']:
            if name == 'y' and 'f' in kwargs:
                # Specifying f supercedes y
                pass
            else:
                # Makes x and y values in the correct format (list)
                if name not in kwargs:
                    # Generate x and y values dynamically (i.e. self.xlims)
                    kwargs[name] = np.linspace(*getattr(self,name+'lims'),50)
                else:
                    if type(kwargs[name]) != list:
                        # Reformat if not a list
                        if type(kwargs[name]) == np.ndarray:
                            # numpy.ndarray reformatting
                            kwargs[name] = kwargs[name].tolist()
                        elif type(kwargs[name]) in [float,int,
                                                    *(getattr(np,'int'+j) for j in ['','8','16','32','64']),
                                                    *(getattr(np,'float'+j) for j in ['','16','32','64','128'])]:
                            # single point formatting
                            kwargs[name] = [kwargs[name]]
                        else:
                            # Unsupported error
                            print(type(kwargs[name]))
                            raise ValueError('Only (numpy.ndarray, float, int) supported for values of {}.'.format(name))
                ###
                # Update self.x and self.y
                if getattr(self,name) is None:
                    # Overwrite self.x, self.y
                    setattr(self,name,kwargs[name])
                else:
                    # Grab num_points as optional argument
                    if 'num_points' in kwargs:
                        if type(kwargs['num_points']) in [float,int,
                                                    *(getattr(np,'int'+j) for j in ['','8','16','32','64']),
                                                    *(getattr(np,'float'+j) for j in ['','16','32','64','128'])]:
                            if len(getattr(self,name)) >= kwargs['num_points']:
                                # Overwrite self.x, self.y if num_points exceeded
                                setattr(self,name,kwargs[name])
                            else:
                                # Concatenate lists for self.x, self.y
                                setattr(self,name,getattr(self,name) + kwargs[name])
                        else:
                            # Unsupported error
                            print(type(kwargs[name]))
                            raise ValueError('Only (numpy.ndarray, float, int) supported for values of {}.'.format(name))
                    else:
                        # Concatenate lists for self.x, self.y
                        setattr(self,name,getattr(self,name) + kwargs[name])
        
        # Grab f function as optional argument.
        if 'f' in kwargs:
            if str(type(kwargs['f'])).split('\'')[1] in ['function','numpy.ufunc']:
                # Use the argument if it is indeed a function
                if len(kwargs['x']) == 1:
                    # single point formatting
                    kwargs['y'] = [kwargs['f'](kwargs['x'])]
                else:
                    # generation via list comprehension
                    kwargs['y'] = [i for i in kwargs['f'](kwargs['x'])]
            else:
                # Unsupported error
                raise ValueError('Only (function, numpy.ufunc) supported for values of {}.'.format('f'))
            
            if self.y is None:
                # Overwrite self.y
                self.y = kwargs['y']
            else:
                # Concatenate lists for self.y
                self.y += kwargs['y']
        
        # Pop the last line if wait is off
        if self._wait == True:
            self._wait = False
        else:
            self.ax.lines.pop()
        
        # Grab line flag as optional argument
        if 'line' in kwargs:
            if kwargs['line'] == False:
                # cross plotting
                self.ax.plot(self.x,self.y,
                             linestyle='',
                             color=self.__colors[self.color],
                             markersize=10,
                             markeredgewidth=4,
                             marker='+')
            elif kwargs['line'] == True:
                # line plotting
                self.ax.plot(self.x,self.y,
                             linewidth=5,
                             color=self.__colors[self.color])
            else:
                # Unsupported error
                raise ValueError('Only bool supported for values of {}.'.format('line'))
        else:
            # Default is line plotting
            self.ax.plot(self.x,self.y,
                         linewidth=5,
                         color=self.__colors[self.color])
        
        # Set xlims and ylims
        self.ax.set_xlim(self.xlims)
        self.ax.set_ylim(self.ylims)
        
        # Pause and show required for correct pseudo-animation
        plt.pause(1e-6)
        plt.show()
    def wipe(self):
        '''Clear the figure.'''
        plt.clf()
        self._wait = True
    def open(self):
        '''(Re)open the graph.'''
        plt.ion()
    def close(self):
        '''Close the graph.'''
        plt.ioff()
        plt.close()
        self._wait = True
