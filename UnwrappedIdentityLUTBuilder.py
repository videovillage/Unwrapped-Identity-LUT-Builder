#Authored by Greg Cotten
#Available under the MIT license

import numpy
from PIL import Image
import os

def Rescale0to1NumpyArrayToBitdepth(data, bitdepth):
	if(bitdepth == numpy.uint8):
		return (data * (2**8-1)).astype(numpy.uint8)
	# elif(bitdepth == numpy.uint16):
	# 	return (data * (2**16-1)).astype(numpy.uint16)
	# elif(bitdepth == numpy.uint32):
	#  	return (data * (2**32-1)).astype(numpy.uint32)
	# elif(bitdepth == numpy.float16):
	# 	return data.astype(numpy.float16)
	# elif(bitdepth == numpy.float32):
	# 	return data.astype(numpy.float32)
	raise NameError("Invalid bitdepth")

def MakeUnwrappedIdentityLUTAtBitdepth(cubeSize, bitdepth):
	return Rescale0to1NumpyArrayToBitdepth(MakeUnwrappedIdentityLUT(cubeSize), bitdepth)

def MakeIndentityLUT(cubeSize):
	identity = numpy.zeros((cubeSize, cubeSize, cubeSize), object)
	for r in xrange(identity.shape[0]):
		for g in xrange(identity.shape[1]):
			for b in xrange(identity.shape[2]):
				identity[r, g, b] = [RemapTo01(r, cubeSize), RemapTo01(g, cubeSize), RemapTo01(b, cubeSize)]
	return identity

#def returns x,y rgb data scaled 0 to 1
def MakeUnwrappedIdentityLUT(cubeSize):
	data = NumpyImageArrayOfSize(cubeSize*cubeSize, cubeSize)
	identity = MakeIndentityLUT(cubeSize)
	for y in xrange(data.shape[0]):
		for x in xrange(data.shape[1]):
			redIndex = (x%cubeSize)
			greenIndex = y
			blueIndex = (x/cubeSize)
			data[y, x] = [identity[redIndex, greenIndex, blueIndex][0], identity[redIndex, greenIndex, blueIndex][1], identity[redIndex, greenIndex, blueIndex][2]]

	return data



def RemapTo01(val, cubeSize):
	return (float(val)/float(cubeSize-1))

def RemapToInt(val, bits):
	return int(val*bits)
			
#bitdepth: np.uint8, np.float32
def NumpyImageArrayOfSize(width, height):
	return numpy.zeros( (height, width, 3), float)

def PrintNumpyArray(data):
	for y in xrange(data.shape[0]):
		for x in xrange(data.shape[1]):
			print x, y, data[y,x]


def main():
	#parameters
	cubeSize = 32
	bitdepth = numpy.uint8 #uint8 only supported at the moment due to PIL being terrible
	fileType = "png"
	destinationFolder = os.path.dirname(os.path.abspath(__file__))+"/" #os.path.expanduser("~")+"/Desktop/"
	filename = "identityLUT_"+str(cubeSize)+"x"+str(cubeSize)+"."+fileType

	#make unwrapped lut as a numpy array only uint8 supported at this time
	data = MakeUnwrappedIdentityLUTAtBitdepth(cubeSize, bitdepth)
	
	#copy numpy array into PIL image
	img = Image.fromarray(data)

	#save image
	img.save(destinationFolder + filename, fileType)

if __name__ == '__main__':
	main()    
