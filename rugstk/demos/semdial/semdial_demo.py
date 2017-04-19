#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Visualization of LUX results.
Adapted from ZetCode Tkinter tkColorChooser tutorial
(author: Jan Bodnar, website: www.zetcode.com)
"""

from Tkinter import Tk, Frame, Button, Text, Label, StringVar, BOTH, SUNKEN, NORMAL, END, DISABLED, Entry
import tkColorChooser
from rugstk import LUX
import colorsys
from math import sin, cos, atan2, pi


class Example(Frame):

    output_lines = 10
    # make debug false when you are actually going to demo this to an audience
    debug = 1
        
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.hsv_color = colorsys.rgb_to_hsv(0.0, 0.0, 1.0)
        self.hex_color = '#0000ff'
        # Added second copy of the above two fields for second color
        # For debugging, want an initial 
        if self.debug :
            self.hsv_colorTwo = colorsys.rgb_to_hsv(0.0, 0.50, 0.625)
            self.hex_colorTwo = '#0088aa'
        else:
            self.hsv_colorTwo = colorsys.rgb_to_hsv(1.0, 0.0, 0.0)
            self.hex_colorTwo = '#ff0000'
        
        self.parent = parent  
	print "Loading model..."      
        self.lux = LUX()
        self.initUI()

    def update_output(self):
        (h, s, v) = self.hsv_color
        self.cv.set('Color {:.2f} {:.2f} {:.2f} (hsv)'.format(h, s, v))
        
    #tjm Added second update_output method for when second color is chosen 
    def update_outputTwo(self):
        (h, s, v) = self.hsv_colorTwo
        self.cvTwo.set('Color {:.2f} {:.2f} {:.2f} (hsv)'.format(h, s, v))
       
    def initUI(self):

        row_height = 220
        start_height = 30
        left_column = 30
        sq_size = 180
        color_column = left_column
        assoc_column = color_column + sq_size + 30
        dist_column = assoc_column + 220
        
        y_label = 5
        self.parent.title("Interactive LUX visualization")      
        self.pack(fill=BOTH, expand=1)
        
        self.frame = Frame(self, border=1, relief=SUNKEN, width=sq_size, height=sq_size)
        self.frame.place(x=color_column, y=start_height)
        self.frame.config(bg=self.hex_color)
        self.frame.bind("<Button-1>", self.onChooseClick)

        #tjm Added second color display window
        self.frameTwo = Frame(self, border=1, relief=SUNKEN, width=sq_size, height=sq_size)
        self.frameTwo.place(x=color_column, y=start_height+row_height)
        self.frameTwo.config(bg=self.hex_colorTwo)
        self.frameTwo.bind("<Button-1>", self.onChooseTwoClick)
        
        #tjm First string field to display the H, S, and V values
        self.cv = StringVar()
        self.info = Label(self, textvariable=self.cv)
        self.info.place(x=color_column, y=y_label)
        
        #tjm second string field to display H, S, and V values
        self.cvTwo = StringVar()
        self.infoTwo = Label(self, textvariable=self.cvTwo)
        self.infoTwo.place(x=color_column, y=y_label+row_height)
        
        #tjm label for associated color terms field
        self.cvThree = StringVar()
        self.infoThree = Label(self, textvariable=self.cvThree)
        self.infoThree.place(x=assoc_column, y=y_label)

        #tjm label for distinguishing color terms field
        self.cvFour = StringVar()
        self.infoFour = Label(self, textvariable=self.cvFour)
        self.infoFour.place(x=dist_column, y=y_label)      
                
        #tjm instruction text for color term assignment prediction function
        self.cvFive =  StringVar()
        self.infoFive = Label(self, textvariable=self.cvFive)
        self.infoFive.place(x=left_column, y=y_label+2*row_height)

        self.display = Text(self, border=1, 
            relief=SUNKEN, width=25, height=self.output_lines)
        self.display.place(x=assoc_column, y=start_height)
        self.display.tag_configure('undistinguished', foreground='dark salmon')
        
        #tjm Added second text window to display color labels
        self.displayTwo = Text(self, border=1, 
            relief=SUNKEN, width=25, height=self.output_lines)
        self.displayTwo.place(x=assoc_column, y=start_height+row_height)
        self.displayTwo.tag_configure('undistinguished', foreground='dark salmon')
        
        #tjm Text field that displays distinction color term for top color
        self.distLabel = Text(self, border=1, 
            relief=SUNKEN, width=25, height=self.output_lines)
        self.distLabel.place(x=dist_column, y=start_height)
        
        #tjm Text field that shows distinction color term for bottom color
        self.distLabelTwo = Text(self, border=1, 
            relief=SUNKEN, width=25, height=self.output_lines)
        self.distLabelTwo.place(x=dist_column, y=start_height+row_height)
        
        #tjm added Entry widget for user to supply a color term
        self.e = Entry(self, bd = 5)
        self.e.bind("<Return>", lambda(event):self.onChooseAssign(self.e.get()))
        self.e.place(x = assoc_column, y=y_label+2*row_height)
        
        #tjm added text window to display result
        self.assignmentResult = Text(self, border = 1,
            relief=SUNKEN, width = 25, height = 2)
        self.assignmentResult.place(x = dist_column, y = y_label+2*row_height)
        
        self.cvThree.set('Associated Color Terms')
        self.cvFour.set('Differentiating Color Terms')
        self.cvFive.set('Test color term to interpret')

        self.update_output()
        self.update_outputTwo()
        self.distAndDisplay()
        
    def distAndDisplay(self):
        hueResultList = self.distinguish(1)
        hueResultListTwo = self.distinguish(2)
        #tjm displays top N choices and confidence ratings in the distLabel text field
        desc = [ '{:<17} {:.3f}\n'.format(hueResultList[i][0], hueResultList[i][1]) for i in range(self.output_lines) ]
        self.distLabel.config(state=NORMAL)
        self.distLabel.delete(1.0, END)
        self.distLabel.insert(END, ''.join(desc))
        self.distLabel.config(state=DISABLED)
        descs = [hueResultList[i][0] for i in range(self.output_lines)]
        
        descTwo = [ '{:<17} {:.3f}\n'.format(hueResultListTwo[i][0], hueResultListTwo[i][1]) for i in range(self.output_lines) ]
        self.distLabelTwo.config(state=NORMAL)
        self.distLabelTwo.delete(1.0, END)
        self.distLabelTwo.insert(END, ''.join(descTwo))
        self.distLabelTwo.config(state=DISABLED)
        descsTwo = [hueResultListTwo[i][0] for i in range(self.output_lines)]

        #tjm the "items" field holds the probability for each color term being used to describe hsv_color
        (h, s, v) = self.hsv_color
        items = self.lux.full_posterior((h * 360, s * 100, v * 100))
        desc = [ '{:<17} {:.3f}\n'.format(items[i][0], items[i][1]) for i in range(self.output_lines) ]

        #tjm displays the HSV values
        self.display.config(state=NORMAL)
        self.display.delete(1.0, END)
        self.display.insert(END, ''.join(desc))
        for i in range(self.output_lines) :
            if items[i][0] not in descs :
                self.display.tag_add('undistinguished', str(i+1) + ".0", str(i+1) + ".23")
        self.display.config(state=DISABLED)    

        #tjm the "itemsTwo" field holds the probability for each color term being used to describe hsc_colorTwo
        (h, s, v) = self.hsv_colorTwo
        itemsTwo = self.lux.full_posterior((h * 360, s * 100, v * 100))
        descTwo = [ '{:<17} {:.3f}\n'.format(itemsTwo[i][0], itemsTwo[i][1]) for i in range(self.output_lines) ]
        self.displayTwo.config(state=NORMAL)
        self.displayTwo.delete(1.0, END)
        self.displayTwo.insert(END, ''.join(descTwo))
        for i in range(self.output_lines) :
            if itemsTwo[i][0] not in descsTwo :
                self.displayTwo.tag_add('undistinguished', str(i+1) + ".0", str(i+1) + ".23")
        self.displayTwo.config(state=DISABLED)    

        self.onChooseAssign(self.e.get())

    def onChoose(self):
      
        news = tkColorChooser.askcolor()
        if news and news[0]:
            ((red,green,blue), hx) = news
            self.hex_color = hx
            self.hsv_color = colorsys.rgb_to_hsv(red/255.0, green/255.0, blue/255.0)
            self.frame.config(bg=hx)
            self.update_output()
            self.distAndDisplay()
            
    #tjm Added second onChoose function for when the second button is clicked
    def onChooseTwo(self):
      
        news = tkColorChooser.askcolor()
        if news and news[0]:
            ((red,green,blue), hx) = news
            self.hex_colorTwo = hx
            self.hsv_colorTwo = colorsys.rgb_to_hsv(red/255.0, green/255.0, blue/255.0)
            self.frameTwo.config(bg=hx)
            self.update_outputTwo()
            self.distAndDisplay()
            
    def onChooseClick(self, event) :
        self.onChoose()

    def onChooseTwoClick(self, event) :
        self.onChooseTwo()
        
    def onChooseAssign(self, colorTerm):
        node = self.lux.all.get(colorTerm)
        if node:
            scoreTop = self.score(node, self.hsv_color, self.hsv_colorTwo)
            scoreNumberTop = scoreTop[1]
            scoreBottom= self.score(node, self.hsv_colorTwo, self.hsv_color)
            scoreNumberBottom = scoreBottom[1]
            totalScoreTop = (scoreNumberTop/(scoreNumberTop+scoreNumberBottom))
            if totalScoreTop > 0.5:
                winner = '{:<17} {:.3f}\n{:<14} {:.6f}'.format('top color!', totalScoreTop, colorTerm, scoreNumberTop)
            else:
                if totalScoreTop < 0.5:
                    winner = '{:<17} {:.3f}\n{:<14} {:.6f}'.format('bottom color!', (1.0 - totalScoreTop),  colorTerm, scoreNumberBottom)
                else:
                    winner = 'Could describe either.\n{:<14f} {:.6f}'.format(colorTerm, scoreNumberTop)
        elif colorTerm :
            winner = 'Unknown term: ' +  colorTerm 
        else :
            winner = ''
            
        self.assignmentResult.config(state=NORMAL)
        self.assignmentResult.delete(1.0, END)
        self.assignmentResult.insert(END, winner)
        self.assignmentResult.config(state=DISABLED)  
    
    def score(self, currentNode, hsvY, hsvZ):
        (hY, sY, vY) = hsvY
        (hZ, sZ, vZ) = hsvZ
        
        hY *= 360
        sY *= 100
        vY *= 100
        hZ *= 360
        sZ *= 100
        vZ *= 100
        
        muHLow = currentNode.dim_models[0].params[0]
        muHHigh = currentNode.dim_models[0].params[3]
        muSLow = currentNode.dim_models[1].params[0]
        muSHigh = currentNode.dim_models[1].params[3]
        muVLow = currentNode.dim_models[2].params[0]
        muVHigh = currentNode.dim_models[2].params[3]
        # mds changed to hY and hZ - never use the unscaled values
        phiHY = currentNode.dim_models[0].phi(hY)
        phiHZ = currentNode.dim_models[0].phi(hZ)
        phiSY = currentNode.dim_models[1].phi(sY)
        phiSZ = currentNode.dim_models[1].phi(sZ)
        phiVY = currentNode.dim_models[2].phi(vY)
        phiVZ = currentNode.dim_models[2].phi(vZ)
 
        # mds added: need to handle hue adjust
        if currentNode.dim_models[0].adjust :
                adjust = True; 
                nhY = atan2(sin(hY*pi/180),cos(hY*pi/180))*180/pi
                nhZ = atan2(sin(hZ*pi/180),cos(hZ*pi/180))*180/pi
        else :
                adjust = False;
                nhY = hY;
                nhZ = hZ;
                
        """
        ([product over opposite dimensions d] phi_d(y) ) *  <== termA
        ([product over other dimensions d] phi_d(y) - <== termB
        [product over all dimensions d] phi_d(z)) <== termC
        """
        termA = 1.0
        termB = 1.0
        termC = phiHZ * phiSZ * phiVZ
        oppSideCase = 0
        #tjm determine which case and calculate appropriate y-but-not-z value
            
        #tjm opposite sides case for hue
        if ((nhY < muHLow) & (muHHigh < nhZ)) | ((nhZ < muHLow) & (muHHigh < nhY)):
            termA *= phiHY
            oppSideCase += 1
        else:
            termB *= phiHY
        #tjm opposite sides case for saturation
        if ((sY < muSLow) & (muSHigh < sZ)) | ((sZ < muSLow) & (muSHigh < sY)):
            termA *= phiSY   
            oppSideCase += 1
        else:
            termB *= phiSY
        #tjm opposite sides case for value
        if ((vY < muVLow) & (muVHigh < vZ)) | ((vZ < muVLow) & (muVHigh < vY)):
                termA *= phiVY 
                oppSideCase +=1
        else:
            termB *= phiVY   
            
        score = termA * (termB - termC)
        if score < 0:
            score = 0
        #mds weight words by availability
        score *= currentNode.availability
        
        return [currentNode.name, score, termA, termB, termC, oppSideCase, adjust, nhY, nhZ, muHLow, muHHigh]
    
    #tjm Method to select color term that describes one color but not the other
    def distinguish(self, choice):        
        
        """tjm process:
        1) go through all color terms
            1a) see if it's an acceptable case
            1b) calculate y-but-not-z-confidence
            1c) store color term name and y-but-not-z-confidence in list
        2) return sorted list
        3) print out top 5 values for sanity check 
        """
        
        #tjm list of color terms and associated y-but-not-z confidence
        hueResults = []
        
        #tjm determine if you're picking a term to describe top color or bottom color
        if choice == 1:
            #tjm loop over all color terms
            for currentNodeChoice in self.lux.all.values(): 
                #mds enable comprehensive debugging reports
                hueResults.append(self.score(currentNodeChoice, self.hsv_color, self.hsv_colorTwo))
        else:
            for currentNodeChoice in self.lux.all.values(): 
                #mds enable comprehensive debugging reports
                hueResults.append(self.score(currentNodeChoice, self.hsv_colorTwo, self.hsv_color))

        total = sum(r[1] for r in hueResults)
        for r in hueResults :
            r[1] /= total
            
        return sorted(hueResults, key = lambda hueResults:hueResults[1], reverse=True)
        

    
def main():
  
    root = Tk()
    ex = Example(root)
    #tjm Doubled vertical height to make room for second color chooser
    #tjm Added 100 to vertical height to make room for distinction readout  
    #tjm added 60 to vertical height for color term assignment function
    #tjm added 50 to vertical height for color term assignment results
    root.geometry("680x500+300+300")
    root.mainloop()  
    


if __name__ == '__main__':
    main()  
    
    
