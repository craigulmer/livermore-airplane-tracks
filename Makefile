

ROOT := $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))


R2C=$(ROOT)/raw2csv/raw2csv

all: $(ROOT)/data/csv

# Build Raw2Csv tool that builds tracks from the files
$(R2C):
	cd raw2csv && go build

# Unpack
$(ROOT)/data/raw:
	cd $(ROOT)/data && tar -xf $(ROOT)/data/raw.tar.bz

unpack: $(ROOT)/data/raw

#$(ROOT)/data/csv:
#	mkdir $@

$(ROOT)/data/csv: $(ROOT)/data/raw
	mkdir $@; \
	cd $(ROOT)/data/raw; \
	for i in *.txt; do \
		csv=$${i%.txt}.csv; \
		echo Converting data/raw/$$i to data/csv/$$csv; \
		$(R2C) --file=$$i > ../csv/$$csv; \
	done

# Convert all raw text files to csv files mapnik can use
csv: $(R2C) $(ROOT)/data/csv 


# Make a file that contains every point (lon lat hexid)
$(ROOT)/data/all_points.txt:
	@grep "^3" $(ROOT)/data/raw/* | awk '{print $$4 " " $$3 " " $$2}' > $@

$(ROOT)/data/all_ids_type1.txt:
	@grep "^1" $(ROOT)/data/raw/* | awk '{print $$2}' | sort | uniq > $@

$(ROOT)/data/all_ids_type3.txt:
	@grep "^3" $(ROOT)/data/raw/* | awk '{print $$2}' | sort | uniq > $@


stat_num_points: $(ROOT)/data/all_points.txt
	@x=`wc -l $<`; \
	echo "Number Points: $${x% *}"

stat_num_planes1: $(ROOT)/data/all_ids_type1.txt
	@x=`wc -l $<`; \
	echo "Number Planes in type 1 messages: $${x% *}"

stat_num_planes3: $(ROOT)/data/all_ids_type3.txt
	@x=`wc -l $<`; \
	echo "Number Planes in type 3 messages: $${x% *}"


stats: stat_num_points stat_num_planes1 stat_num_planes3

all_data: \
	$(ROOT)/data/all_points.txt    \
	$(ROOT)/data/all_ids_type1.txt \
	$(ROOT)/data/all_ids_type3.txt \
	csv

clean:
	cd $(ROOT)/raw2csv && go clean
	rm -f $(ROOT)/data/*.txt


clean_all:
	rm -f -R $(ROOT)/data/csv 
	rm -f -R $(ROOT)/data/raw

help:
	@echo "make all_data : generate all data (CSV, points, stats)"
	@echo "     make csv : convert data to CSV format that Mapnik can use"
	@echo "make stats    : generate some simple statistics from the raw data"
