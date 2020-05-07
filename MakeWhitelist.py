import sys

## filters out cbc that do not match whitelist. In particualr, requires everything from start to end to match
##assumes all are sorted lexigraphically!
def filter_cbc(cbc,white,start,end):
	poss=[barcode[start:end] for barcode in cbc]
	poss.sort()
	cur_white=0
	cur_cbc=0
	ret=[]
	while cur_white<len(white) and cur_cbc<len(cbc):
		if poss[cur_cbc]==white[cur_white]:
			ret.append(cbc[cur_cbc])
			cur_cbc=cur_cbc+1
			continue;
		if poss[cur_cbc]<white[cur_white]:
			cur_cbc=cur_cbc+1;
			continue;
		cur_white=cur_white+1
	
	return(ret)

	


##useful function
def readInList(filename):
	fil=open(filename)
	lst=fil.readlines()
	lst=[l.strip() for l in lst]
	return(lst)



if __name__=="__main__":
	print("Let make the whitelist!")
	args=sys.argv
	infile=args[1]
	outfile=args[2]
	whitefile="/stanley/levin_dr/ssimmons/SciFi/Kallisto/UpdatedPipeline/Code/Lists/comb.cbc.txt"
	barfile="/stanley/levin_dr/ssimmons/SciFi/Kallisto/UpdatedPipeline/Code/Lists/737K-cratac-v1.txt"
	cbc=readInList(infile)
	white_comb=readInList(whitefile)
	white_10x=readInList(barfile)

	print(len(cbc))
	print(len(white_comb))
	print(len(white_10x))
	print("Sort Inputted lists")
	cbc.sort()
	white_comb.sort()
	white_10x.sort()

	print("First, filter out based off of combinatorial barcodes")
	cbc=filter_cbc(cbc,white_comb,0,13)

	print("Next, filter out based off of 10x barcodes")
	cbc=filter_cbc(cbc,white_10x,13,29)

	print("Finally, save!")
	fil=open(outfile,"w")
	for c in cbc:
		fil.write(c+"\n")
	print("Done!")

	fil.close()

