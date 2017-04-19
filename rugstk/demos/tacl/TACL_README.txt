"A Bayesian Approach to Grounded Color Semantics"
ANONYMOUS 

DIRECTIONS FOR THE DEMO 

The demo file allows you to explore our model, the development data, and the gaussian model. 

The standard scientific computing python stack is required to run this. This includes: matplotlib, scipy, and numpy. 

NOTE: some computer may load slower than others when committing actions in this demo file.  This is mostly due to plotting libraries.  

Directions:

0.  run "python demo.py"  --- If you have the required dependencies, it will run. If you don't, please check into Anaconda, Enthought's Canopy, or other python bundles for scientific computing. 

1. Select a color on the left. The posterior for LUX is shown below as a vertical list of color labels and their corresponding probability.  

2. You may double click on any of the color labels to see three things: (1) the LUX model for that color label, (2) the Guassian model for that color label, and (3) the development data for that color label.  

Additional Points:

1. The Probe X (The chosen color value) will also be shown in relation to these three things. 

2. You may also single click on a color label and click the "Show Details".

3.  The development data is shown as the binomial data from which our model was fit.  Of course, this means that the shape of the histograms is different than what the Gaussian was learned on.  We show the sampling rate using a gradient.  The histograms are shaded with a gradient from light grey to dark grey.  The light grey represents a less sample area and dark grey the higher sampled area.    

4.  This folder contains the LUX file in lux.xml

5.  To use LUX, please see lux.py and demo.py.

6. In LUX xml, each child of the root node is a color label.  Each color label has as children the three dimensions.  Finally, in each dimension is the 6 parameters with standard deviations.
There are two accompanying python files (lux.py and demo.py) that detail how to parse and use the model.

NOTE: The model expects datum on the support set of (0,360) for HUE, (0,100) for Saturation, and (0,100) for Value
Some of the labels have had their Hues Adjusted. Hue is a circle.  Some distributions (such as RED) straddle the 0/360 point.
To convert, we used the atan2 function which converts to (-180,180).  However, each model is built to accept the support set (0,360) and convert to the atan2 adjusted support set. 
