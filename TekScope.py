#!/usr/bin/python
import numpy
import matplotlib.pyplot as plot
 
import instrument
 
""" Program to plot the Y-T data from selected channels."""
 
# Add command line options:
from optparse import OptionParser

ch1 = 0
ch2 = 0
ref1 = 0
ref1 = 0

def read_data():
	""" Function for reading data and parsing binary into numpy array """
	test.write("CURV?")
	rawdata = test.read(9000)

	# First few bytes are characters to specify the length of the transmission. Need to strip these off:
	# we'll assume a 5000-byte transmission so the string would be "#45000" and we therefor strip 6 bytes.
	return numpy.frombuffer(rawdata[6:-1], 'i2')
	

# Initialize our scope
test = instrument.TekScope1000("/dev/usbtmc0")
 
# Stop data acquisition
test.write("ACQ:STATE STOP")
 
# Set data width to 2 for better resolution
test.write("DATA:WIDTH 2")

# Set data format to binary, zero is center-frame and big endian
test.write("DATA:ENCD SRI")

#TODO: replace with automatic selection using command:
# SELECT? returns SELECT:CH1 0;CH2 1;MATH 1;REFA 0;REFB 1

# Grab the data from channel 1

test.write("DATA:SOURCE CH1")
ch1data = read_data()

test.write("DATA:SOURCE CH2")
ch2data = read_data() 


# Get the voltage scale
test.write("CH1:SCALE?")
voltscale1 = float(test.read(20))
 
# And the voltage offset
test.write("CH1:POSITION?")
voltoffset1 = float(test.read(20))

ch1data = ((ch1data/65535.0 * 10) - voltoffset1) * voltscale1

# Get the voltage scale
test.write("CH2:SCALE?")
voltscale2 = float(test.read(20))
 
# And the voltage offset
test.write("CH2:POSITION?")
voltoffset2 = float(test.read(20))

ch2data = ((ch2data/65535.0 * 10) - voltoffset2) * voltscale2

 
# Get the timescale
test.write("HORIZONTAL:MAIN:SCALE?")
timescale = float(test.read(20))
 
# Get the timescale offset
test.write("HORIZONTAL:MAIN:POSITION?")
timeoffset = float(test.read(20))

# Get the length of the horizontal record
test.write("HORIZONTAL:RECORDLENGTH?")
time_size = int(test.read(30))
 
# Now, generate a time axis.  The scope display range is 0-600, with 300 being
# time zero.
#time = numpy.arange(-300.0/50*timescale, 300.0/50*timescale, timescale/50.0)
#time = numpy.arange(time_size)

#time = time / time_size * timescale * 10
time = numpy.arange(0,timescale*10,timescale*10/time_size)
 
# Start data acquisition again, and put the scope back in local mode
test.write("ACQ:STATE RUN")
test.write("UNLOCK ALL")

# Plot the data
plot.subplot(2,1,1)
plot.plot(time,ch1data)
plot.subplot(2,1,2)
plot.plot(time,ch2data)
plot.title("Oscilloscope Channel 1&2")
plot.ylabel("Voltage (V)")
plot.xlabel("Time (S)")
#plot.xlim(time[0], time[599]
plot.show()

# TODO add file save to this script
