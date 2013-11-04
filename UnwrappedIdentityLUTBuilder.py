#Authored by Greg Cotten
#Available under the MIT license

import numpy
import Image
import os

def Rescale0to1NumpyArrayToBitdepth(data, bitdepth):
	if(bitdepth == numpy.uint8):
		return (data * (2**8-1)).astype(numpy.uint8)
	# elif(bitdepth == numpy.uint16):
	# 	return (data * (2**16-1)).astype(numpy.uint16)
	# elif(bitdepth == numpy.uint32):
	# 	return (data * (2**32-1)).astype(numpy.uint32)
	# elif(bitdepth == numpy.float16):
	# 	return data.astype(numpy.float16)
	# elif(bitdepth == numpy.float32):
	# 	return data.astype(numpy.float32)
	raise NameError("Invalid bitdepth")

def MakeUnwrappedIdentityLUTAtBitdepth(cubeSize, bitdepth):
	return Rescale0to1NumpyArrayToBitdepth(MakeUnwrappedIdentityLUT(cubeSize), bitdepth)

#def returns x,y rgb data scaled 0 to 1
def MakeUnwrappedIdentityLUT(cubeSize):
	data = NumpyImageArrayOfSize(cubeSize*cubeSize, cubeSize)
	for y in xrange(data.shape[0]):
		for x in xrange(data.shape[1]):
			redIndex = (x%cubeSize)
			greenIndex = y
			blueIndex = (x/cubeSize)
			red = RemapTo01(redIndex, cubeSize)
			green = RemapTo01(greenIndex, cubeSize)
			blue = RemapTo01(blueIndex, cubeSize)
			data[y, x] = [red, green, blue]

	return data

def MakeIndentityLUT(cubeSize):
	identity = numpy.zeros((cubeSize, cubeSize, cubeSize), float)
	for x in xrange(identity.shape[0]):
		for y in xrange(identity.shape[1]):
			for z in xrange(identity.shape[2]:
				identity[x, y, z] = RemapTo01(x, cubeSize), RemapTo01(y, cubeSize), RemapTo01(z, cubeSize)
	return identity

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
	cubeSize = 16
	bitdepth = numpy.uint8 #uint8 only supported at the moment
	fileType = "tiff"
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
