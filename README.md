# livermore-airplane-tracks

Some Raw ADS-B data collected in Livermore, CA and some tools to inspect/plot the data

For more info, see my bog entries about this project: 

http://craigulmer.com/index.pl?id=flight_data_from_the_data_logger

http://craigulmer.com/index.pl?id=examining_bad_flight_data_from_the_logger


## Data
The data in this repo was captured by me using an RTL-SDR and the dump1090 program. I live in Livermore, CA and ran the dumper every day during February 2015 (though not at night). I certify that I collected this data myself at home, and that anyone can use it as they wish.

The data is packed in single bzip'd tar file. Once unpacked you get a text file dump for each day of the month. There are two types of messages embedded in the data. The first column identifies the message type. Type 1 is a chrip message that associates the hex ID for the plane with a callsign (often the tailfin). Type 3 identifies the position for a particular plane at a particular time. The lines in the file are odered as they were captured by the SDR. The date stamps are what the the planes reported themselves (and thus may be out of order)..

## Converting to Tracks
I wrote a program to convert the raw data into tracks that programs like Mapnik can use. The program is written in Go and just joins all the points for a particular plane together into a WKT string.

## Plotting the Data
A few pylab plotters are included. These tools were used to investigate some of the bad points I was noticing.

## Use the Makefile
The makefile in this project should help you build and process all the data in this project. It can unpack the raw data, build the go file, and do some simple stats on the data. Try: make all_data.

