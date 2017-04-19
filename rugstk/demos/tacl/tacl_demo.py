#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Visualization of LUX results.
Adapted from ZetCode Tkinter tkColorChooser tutorial
(author: Jan Bodnar, website: www.zetcode.com)
"""
import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from Tkinter import Tk,  Frame, Button, Listbox, Label, Text, BOTH, SUNKEN, NORMAL, StringVar,END,DISABLED, TOP, LEFT, BOTTOM, RIGHT, X, Y, CENTER
import tkColorChooser 
from rugstk import LUX
import colorsys 
from matplotlib.pyplot import Figure
from scipy.stats import gamma as gam_dist
from scipy.stats import norm
import numpy as np
import pickle
from matplotlib.patches import Rectangle
from math import atan2,cos
import tkFont
import operator
from math import floor
import os
global curdir
curdir = os.path.dirname(os.path.abspath(__file__))
#custom_preamble = {
#    "text.usetex": True,
#    "text.latex.preamble": [
#        r"\usepackage{amsmath}", # for the array macros
#        ],
#    }
#matplotlib.rcParams.update(custom_preamble)


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.hsv_color = colorsys.rgb_to_hsv(0.0, 0.0, 1.0)
        self.hex_color = '#0000ff'
        self.color_list = ["red","blue","green","orange","purple"]
        self.parent = parent        
        print "Loading model..."
        self.lux = LUX()
        fp = open(curdir+"/gauss_model.pkl"); self.gm = pickle.load(fp); fp.close()
        fp = open(curdir+"/memoized_binomial_data.pkl"); self.curve_data = pickle.load(fp); fp.close()
        fp = open(curdir+"/sampling_normalizer.pkl"); self.normalizer = pickle.load(fp); fp.close()
        print "Creating UI"
        self.initUI()
        self.update_output()
        self.replot()

    def update_output(self):
        (h, s, v) = self.hsv_color
        self.hsv_var.set("Hue: \t %2.1f \nSat:\t %2.1f \nValue:\t %2.1f" % (h*360,s*100,v*100))
        items = self.lux.full_posterior((h * 360, s * 100, v * 100))
        self.current_post = items
        desc = [ '{:<25} ({:.3f})\n'.format(items[i][0], items[i][1]) for i in range(25) ]
        self.display.config(state=NORMAL)
        self.display.delete(0, END)
        
        for i in range(25): self.display.insert(END, '{:<20} ({:.3f})'.format(items[i][0], items[i][1]))

        self.display.select_set(0, 0)
    
    def plot_lux_model(self, params,ax1,label,support,dim):
        cur_color='black'
        mu1,sh1,sc1,mu2,sh2,sc2 = params
        left_stach=gam_dist(sh1,scale=sc1); lbounds=left_stach.interval(0.99)
        right_stach=gam_dist(sh2,scale=sc2); rbounds=right_stach.interval(0.99)
        lx=np.linspace(mu1,-180); rx=np.linspace(mu2,360)
        s=3;
        ax1.plot(rx, [right_stach.sf(abs(y-mu2)) for y in rx],linewidth=s,c=cur_color);
        ax1.plot([1.01*mu1,0.99*mu2], [1.,1.], linewidth=s,c=cur_color)
        return ax1.plot(lx,[left_stach.sf(abs(y-mu1)) for y in lx],c=cur_color, linewidth=s);
        
    def plot_gm_model(self, params, ax, label, support):
        s=3
        x = np.linspace(support[0],support[1],360)

        return ax.plot(x,norm.pdf(x,params[0],params[1]),c='red', linewidth=s), norm.pdf([params[0]],params[0],[params[1]])[0]
        
        
    def initUI(self):
      
        self.parent.title("Interactive LUX visualization")      
        self.pack(fill=BOTH, expand=1)
         
        self.color_frame = Frame(self, border=1)
        self.color_frame.pack(side=LEFT)
        
        probe_title_var = StringVar(); probe_title_label = Label(self.color_frame, textvariable=probe_title_var, justify=CENTER,  font = "Helvetica 16 bold italic")
        probe_title_var.set("Color Probe X"); probe_title_label.pack(side=TOP)
        
        self.hsv_var = StringVar()
        self.hsv_label = Label(self.color_frame, textvariable=self.hsv_var,justify=LEFT)
        h,s,v = self.hsv_color
        self.hsv_var.set("Hue: %2.1f \nSaturation: %2.1f \nValue: %2.1f" % (h*360,s*100,v*100))
        self.hsv_label.pack(side=TOP)
        
        self.frame = Frame(self.color_frame, border=1, 
            relief=SUNKEN, width=200, height=200)

        self.frame.pack(side=TOP)
        self.frame.config(bg=self.hex_color)
        self.frame.bind("<Button-1>",self.onChoose)
                
        
        self.btn = Button(self.color_frame, text="Select Color", 
            command=self.onChoose)
        self.btn.pack(side=TOP)
       
        posterior_title_var = StringVar(); posterior_title_label = Label(self.color_frame, textvariable=posterior_title_var, justify=CENTER, font = "Helvetica 16 bold italic")
        posterior_title_var.set("\n\nLUX's Posterior"); posterior_title_label.pack(side=TOP)
        
        Label(self.color_frame, text="Double click to show details \n(Wait time dependent on computer)").pack(side=TOP)


        
        my_font = tkFont.Font(family="Courier", size=10)
        self.display = Listbox(self.color_frame, border=1, 
            relief=SUNKEN, width=30, height=25, font=my_font)
        self.display.pack(side=TOP,fill=Y,expand=1)
        self.display.bind("<Double-Button-1>",self.onSelect)
        self.display_btn = Button(self.color_frame, text="Show details", command=self.onSelect)
        self.display_btn.pack(side=TOP)
        
        self.update_output()
        
        
        
        self.fig = Figure(figsize=(10,4), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas._tkcanvas.pack(side='top', fill='both', expand=1)

    def replot(self):
        
        def gb(x,i,t):
            #t is max value, i in number of bins, x is the thing to be binned
            if x==t:
                return i-1
            elif x==0.0:
                return 0
            return int(floor(float(x)*i/t))        
        hsv_title = []
        j=self.display.curselection()[0]
        name = self.current_post[j][0]
        mult = lambda x: reduce(operator.mul, x)
        g_labels = []; lux_labels=[]; all_g_params=[]
        for i in range(3):
            
            def align_yaxis(ax1, v1, ax2, v2):
                """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
                _, y1 = ax1.transData.transform((0, v1))
                _, y2 = ax2.transData.transform((0, v2))
                inv = ax2.transData.inverted()
                _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
                miny, maxy = ax2.get_ylim()

                ax2.set_ylim(miny, maxy+dy)
                        
            subplot = self.fig.add_subplot(4,1,i+1) 
            dim_label = ["H", "S","V"][i] 
            subplot.set_ylabel(r"$P(k^{true}_{%s}|x)$" % ["H", "S","V"][i] )
            
            curve_data = self.curve_data[name][i]
            
            scale = lambda x,a=0.3,b=0.9: (b-a)*(x)+a
            p_x = lambda x: self.normalizer[i][gb(x,len(self.normalizer[i]),[360,100,100][i])]
            max_p_x = max(self.normalizer[i])
            #1 is white, 0 is black. so we want highly probable thigns to be black.. 


            if self.lux.get_adj(self.current_post[j][0]): 
                support = [[-180,180], [0,100],[0,100]][i]
                pp = lambda x,i: x-360 if i==0 and x>180 else x
                hacky_solution = [360,100,100][i]
                w = 1.5 if i==0 else 1
                
                conv = lambda x: x*support[1]/len(curve_data)
                bar_colors = ["%s" % (scale(1-p_x(conv(x))/max_p_x)) for x in range(len(curve_data))]
                bar1 = subplot.bar([pp(atan2(sin((x*hacky_solution/len(curve_data))*pi/180),cos((x*hacky_solution/len(curve_data))*pi/180))*180/pi,i) for x in range(len(curve_data))],[x/max(curve_data) for x in curve_data], label="%s data" % j,ec="black",width=w,linewidth=0,color=bar_colors)
            else: 
                support = [[0,360], [0,100],[0,100]][i]
                w = 1.5 if i==0 else 1
                conv = lambda x: x*support[1]/len(curve_data)
                bar_colors = ["%s" % (scale(1-p_x(conv(x))/max_p_x)) for x in range(len(curve_data))]
                bar1 = subplot.bar([x*support[1]/len(curve_data) for x in range(len(curve_data))],[x/max(curve_data) for x in curve_data], label="%s data" % name[0],ec="black",width=w,linewidth=0,color=bar_colors)
                pp = lambda x,*args: x
                
            point = pp(self.hsv_color[i]*[360,100,100][i],i)
            hsv_title.append(point)
            probeplot = subplot.plot([point,point], [0,1],linewidth=3,c='blue',label="Probe")

            #for j in range(5):
            lux_plot = self.plot_lux_model(self.lux.get_params(self.current_post[j][0])[i], subplot, self.current_post[j][0],support, i)
            subplot2 = subplot.twinx()
            gm_plot,gm_height = self.plot_gm_model([pp(g_param,i) for g_param in self.gm[self.current_post[j][0]][0][i]], subplot2, self.current_post[j][0], support)
            extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
            
            subplot.legend([extra], [["Hue", "Saturation", "Value"][i]],loc=2,frameon=False)
            
            
            if i==0: legend_set=lux_plot+[extra,extra,extra]+gm_plot+[extra,extra,extra]
            lux_params = self.lux.get_params(self.current_post[j][0])[i]
            g_params = [pp(g_param,i) for g_param in self.gm[self.current_post[j][0]][0][i]]
            all_g_params.append(g_params)
            
            g_labels.append(r"$\mu^{%s}=$%2.2f, $\sigma^{%s}$=%2.2f" % (dim_label, g_params[0],dim_label,g_params[1]))
            #lux_labels.append(r"$\mu^{L,%s}=$%2.2f, $E[\tau^{L,%s}]$=%2.2f, $\alpha^{L,%s}$=%2.2f, $\beta^{L,%s}$=%2.2f, $\mu^{U,%s}=$%2.2f, $E[\tau^{L,%s}]$=%2.2f, $\alpha^{U,%s}$=%2.2f, $\beta^{U,%s}$=%2.2f" % (dim_label, lux_params[0],dim_label, (lux_params[0]-lux_params[1]*lux_params[2]),dim_label,lux_params[1],dim_label, lux_params[2],dim_label,lux_params[3],dim_label,(lux_params[3]+lux_params[4]*lux_params[5]),dim_label, lux_params[4],dim_label,lux_params[5]))
            lux_labels.append(r"$\mu^{L,%s}=$%2.2f, $\alpha^{L,%s}$=%2.2f, $\beta^{L,%s}$=%2.2f, $\mu^{U,%s}=$%2.2f,  $\alpha^{U,%s}$=%2.2f, $\beta^{U,%s}$=%2.2f" % (dim_label, lux_params[0],dim_label, lux_params[1],dim_label, lux_params[2],dim_label,lux_params[3],dim_label,lux_params[4],dim_label,lux_params[5]))
            
            subplot.set_xlim(support[0],support[1])  
            subplot.set_ylim(0,1.05)
            subplot2.set_xlim(support[0],support[1])
            subplot2.set_ylabel(r"$P(x|Gaussian_{%s})$" % ["H", "S","V"][i])  
            align_yaxis(subplot, 1., subplot2, gm_height)
    
    
        leg_loc =(0.9,0.2)
    
        datum = [x*[360,100,100][i] for i,x in enumerate(self.hsv_color)];  phi_value = self.lux.get_phi(datum,self.current_post[j][0])
        #gauss_value = mult([norm.pdf(datum[i],all_g_params[i][0],all_g_params[i][1]) for i in range(3)])
        leg=self.fig.legend(probeplot+legend_set, ["Probe X"]+ [r"$\mathbf{\phi}_{%s}(X)=\mathbf{%2.5f}$; $\mathbf{\alpha}=\mathbf{%2.4f}$" % (self.current_post[j][0],phi_value,self.lux.get_avail(self.current_post[j][0]))]+lux_labels+ 
                                     [r"$Normal^{Hue}_{%s}$; $prior(%s)=%2.4f$" % (self.current_post[j][0],self.current_post[j][0], self.gm[self.current_post[j][0]][2])]+[g_labels[0]+"; "+g_labels[1]+"; "+g_labels[2]]
                                     , loc=8, handletextpad=4,labelspacing=0.1)

        
        self.fig.suptitle("%s" % name, size=30)

        print "done replotting"

    def onChoose(self, *args):
        try:
            ((red,green,blue), hx) = tkColorChooser.askcolor()
        except:
            print "I think you hit cancel"
            return
        self.hex_color = hx
        self.hsv_color = colorsys.rgb_to_hsv(red/255.0, green/255.0, blue/255.0)
        self.frame.config(bg=hx)
        self.update_output()
        self.fig.clear()
        self.replot()
        self.canvas.draw()
        
    def onSelect(self, *args):
        self.fig.clear()
        self.replot()
        self.canvas.draw()

def main():
  
    root = Tk()
    ex = Example(root)
    root.geometry("1400x950+300+50")
    root.mainloop()  


if __name__ == '__main__':
    main()  
