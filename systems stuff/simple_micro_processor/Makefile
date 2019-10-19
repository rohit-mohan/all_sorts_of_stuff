FLAGS=
INFILE=
OUTFILE=$(INFILE:.v=)
DUMPFILE=$(INFILE:.v=.dmp)


$(OUTFILE) : $(INFILE)
	iverilog $(INFILE) -o $(OUTFILE) $(FLAGS)

clean :
	rm -f $(DUMPFILE) $(OUTFILE)


