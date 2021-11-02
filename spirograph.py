import sys, random, argparse
import numpy as np 
import math 
import turtle  
import random 
from PIL import Image 
from datetime import datetime 
from math import gcd 


class Spiro:

	def __init__(self, xc, yc, col, R, r, l):


		#Creates turtle object
		self.t = turtle.Turtle()
		self.t.shape('turtle')
		self.step = 5  #Sets step in degrees 
		self.drawingComplete = False 

		self.setparams(xc, yc, col, R, r, l)

		self.restart() #Initializes drawing 



	#Setting Parameters
	def setparams(self, xc, yc, col, R, r, l):
		self.xc = xc
		self.yc = yc
		self.R = int(R)
		self.r = int(r)
		self.l = l 
		self.col = col 

		#Reduction of r/R with GCD
		gcdVal = gcd(self.r, self.R)
		self.nRot = self.r//gcdVal
		self.k  = r/float(R) #Gets ratio of radii 
		self.t.color(*col)
		self.a =  0  #Stores current angle



	def restart(self):
		self.drawingComplete = False
		self.t.showturtle()

		self.t.up() #Going to first point 
		R, k, l = self.R, self.k, self.l 
		a = 0.0

		#Computing x and y coordinates, and starting pnt.
		x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
		y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
		self.t.setpos(self.xc + x, self.yc + y)
		self.t.down()



	#Drawing lines
	def draw(self):
		R, k, l = self.R, self.k, self.self
		for i in range(0, 360*self.nRot + 1, self.step):
			a = math.radians(i)
			x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
			y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
			self.t.setpos(self.xc + x, self.sc + y)

			#Drawing is completed, hide cursor 
		self.t.hideturtle()
		

	#Creates Animation 
	def update(self):
		#Skip steps if done 
		if self.drawingComplete:
			return 

		#Sets and increments angle
		self.a += self.step 
		R, k, l = self.R, self.k, self.l 
		a = math.radians(self.a)
		x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
		y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
		self.t.setpos(self.xc + x, self.yc + y)
		#Sets flag if drawing is complete
		if self.a >= 360*self.nRot:
			self.drawingComplete = True 
			self.t.hideturtle()



#Animating Spirographs 
class SpiroAnimator:

	#Constructor
	def __init__(self, N):
		self.deltaT = 10  #Timer value in milliseconds 
		self.width = turtle.window_width()
		self.height = turtle.window_height()
		#Create spiro objects 
		self.spiros = []
		for i in range(N):
			rparams = self.genRandomParams() #Generate random parameters
			spiro = Spiro(*rparams) #Sets spiro parameters 
			self.spiros.append(spiro)
		turtle.ontimer(self.update, self.deltaT)


	def genRandomParams(self):
		width, height = self.width, self.height 
		R = random.randint(50, min(width, height)//2)
		r = random.randint(10, 9*R//10)
		l = random.uniform (0.1, 0.9)
		xc = random.randint(-width//2, width//2)
		yc = random.randint(-height//2, width//2)
		
		col = (random.random(),
			random.random(),
			random.random())
		return(xc, yc, col, R, r, l)


	#Restart method for SpiralAnimator 
	def restart(self):
		for spiro in self.spiros:
			spiro.clear()
			rparams = self.genRandomParams() #Generating random parameters 
			spiro.setparams(*rparams)
			spiro.restart 

	#Update method for SpiralAnimator 
	def update(self):
		nComplete = 0 
		for spiro in self.spiros: #Updates and Counts completed spiros 
			spiro.update()
			if spiro.drawingComplete:
				nComplete += 1 
		#If all spiros completed
		if nComplete == len(self.spiros):
			self.restart()	
		turtle.ontimer(self.update, self.deltaT)

	#Toggles turtle curser on and off 
	def toggleTurtles(self):
		for spiro in self.spiros:
			if spiro.t.invisible():
				spiro.t.hideturtle()
			else:
				spiro.t.showturtle()


#Saves drawings as PNG 
def saveDrawing():
	turtle.hideturtle()
	#Generate unique names for files 
	dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
	fileName = 'spiro-' + dateStr
	print("Saving drawing to %s.eps/png" % fileName)
	canvas = turtle.getcanvas() #Get tkinter canvas
	#Saves as postcript img 
	canvas.postscript(file = fileName + '.eps')

	#Pillow module to convert image file to PNG 
	img = Image.open(fileName + '.eps')
	img.save(fileName + '.png', '.png')
	turtle.showturtle()



def main():
	print("genrating your spirograph...")
	
	
	descStr = """This program draws Spirographs. When no arguments, 
	program draws random Spirographs"""
			  
		

	#Create parser 
	parser = argparse.ArgumentParser(description = descStr)
	#Adding expected arguments
	parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
	help="The three arguments in sparams: R, r, l.")
	args = parser.parse_args()

	#Window setup 
	turtle.setup(width=0.8)
	turtle.shape('turtle')
	turtle.title("Spirographs!!!")

	#Add key handler to save drawings 
	turtle.onkey(saveDrawing, "s")
	turtle.listen()
	turtle.hideturtle()

	#Check for arguments and draw Spirograph 
	if args.sparams:
		params = [float(x) for x in args.sparams] 
		#Draw with parameters 
		col = (0.0,0.0,0.0)
		spiro = Spiro(0, 0, col, *params)
		spiro.draw()
	else:
		spiroAnim = SpiroAnimator(18) #This number is the argument
		turtle.onkey(spiroAnim.toggleTurtles, "t")
		#Key handler to resart animation 
		turtle.onkey(spiroAnim.restart, "space")

	turtle.mainloop()

if __name__ == '__main__':
	main()
