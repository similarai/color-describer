"""
Lexicon of Uncertain Color Standards
Written by XXXXXXXXXXXXXXXXXXXXXXX

This is a demo script for the LUX release.  
There is an accompanying XML file.  This script opens it and offers basic functionality
"""

from scipy.stats import gamma as gam_dist
from math import sin, cos, atan2, pi
import xml.etree.ElementTree as ET
import os
import scipy.special as scispec


class LUX:
    def __init__(self, filename=None):
        """
        Input: full path filename to lux.csv
        Function: Parse lux.xml and make available several probability functions:
            1) predict(datum): predicts most likely label; return [label,probability]
            2) posterior_likelihood(datum,label): Returns P(datum|label)
            3) full_posterior(datum): returns all labels ordered by decreasing posterior likelihood
            
        Please look at demo.py which accompanies this file for functionality demonstration. 
        """
	if not filename: filename = os.path.dirname(os.path.abspath(__file__))+"/lux.xml"
        tree = ET.parse(filename)
        root = tree.getroot()

        self.all = {child.get("name"):color_label(child) for child in root}
        
        
    def full_posterior(self, datum):
        probabilities = [[dist.name,dist(datum)] for dist in self.all.values()]
        total = sum([x[1] for x in probabilities])
        return sorted([[name,prob/total] for name,prob in probabilities], key=lambda x:x[1], reverse=True)
        #return sorted([[name,prob] for name,prob in probabilities], key=lambda x:x[1], reverse=True)
        
        
    def predict(self, datum):
        #NOTE: This returns the unnormalized posterior likelihood 
        probabilities = [[dist.name,dist(datum)] for dist in self.all.values()]
        sorted_probabilities = sorted(probabilities, key=lambda x: x[1], reverse=True)
        return sorted_probabilities[0]
    
    def posterior_likelihood(self, datum, label):
        probabilities = [dist(datum) for dist in self.all.values()]
        if label not in self.all.keys(): raise OutOfVocabularyException("Label '%s' was not in the lexicon" % label)
        return self.all[label](datum)/sum(probabilities)
    
    def eval_shortcut(self, datum, label):
        probabilities = {dist.name:dist(datum) for dist in self.all.values()}
        if label not in self.all.keys(): raise OutOfVocabularyException("Label '%s' was not in the lexicon" % label)
        total = sum(probabilities.values())
        posterior = sorted([[name,prob/total] for name,prob in probabilities.items()], key=lambda x:x[1], reverse=True)
        label_prob = probabilities[label]/total 
        return posterior,label_prob
    
    def get_phi(self, datum,label):
        return self.all[label].phi(datum)
    
    def get_params(self, label):
        return [x.params for x in self.all[label].dim_models]
    
    def get_adj(self, label):
        return self.all[label].dim_models[0].adjust
    
    def get_avail(self,label):
        return self.all[label].availability
    
    def getColor(self, name):
        try:
            return self.all[name]
        except KeyError:
            raise OutOfVocabularyException("Color not found, was looking for %s" % name)
    
class color_label:
    def __init__(self,label_node):
        """
        The all-dimension model for each color label
        """
        name = label_node.get("name"); availability = float(label_node.get("availability")); hue_adjust = eval(label_node.get("hue_adjust"))
        
        self.name = name; self.availability = availability
        self.dim_models = [single_dim(child) for child in label_node]
        self.dim_models[0].adjust = hue_adjust
        self.hue_adjust = hue_adjust

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def __call__(self, *args):
        return self.phi(args[0])*self.availability
    
    def phi(self,x):
        return self.dim_models[0].phi(x[0])*self.dim_models[1].phi(x[1])*self.dim_models[2].phi(x[2]) 
    
    def broadness(self):
        broad = lambda x: (x.params[3] + x.params[5]) - (x.params[0] - x.params[2])
        return broad(self.dim_models[0]) / 360 , broad(self.dim_models[1]) / 100 , broad(self.dim_models[2]) / 100

class single_dim:
    """
    The single dimension for each color label
    """
    def __init__(self, dim_node):
        def get_node(name):
            for child in dim_node:
                if child.tag==name:
                    return child
        paramdict = {child.tag:child for child in dim_node}
        paramnames =["mulower","shapelower","scalelower","muupper","shapeupper","scaleupper"]
        self.params = [float(paramdict[paramname].get("value")) for paramname in paramnames]
        self.adjust=False
        self._set_params()
    
    def _swap(self,params):
        self.params = params
        self._set_params()
    
    def _set_params(self):
        mu1,sh1,sc1,mu2,sh2,sc2 = self.params
        self.region = lambda x: (2 if x>mu2 else 1) if x>=mu1 else 0
        self.f= [lambda x: scispec.gdtrc((1.0/sc1),sh1,abs(x-mu1)),
                 lambda x: 1,
                 lambda x: scispec.gdtrc((1.0/sc2),sh2,abs(x-mu2))]

    
    def phi(self, x):
        if self.adjust: x = atan2(sin(x*pi/180),cos(x*pi/180))*180/pi
        return self.f[self.region(x)](x)

class OutOfVocabularyException(Exception):
    pass
