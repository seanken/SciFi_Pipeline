import pandas
import sys

if __name__=="__main__":
	print("Start")
	infile=sys.argv[1]
	outfile=sys.argv[2]
	print(infile)
	print(outfile)
	dat=pandas.read_csv(infile,names=["Counts_CBC"],sep="\t")
	print(dat.head())
	dat["CBC"]=[s.strip().split(" ")[1] for s in dat["Counts_CBC"]]
	dat["Count"]=[int(s.strip().split(" ")[0]) for s in dat["Counts_CBC"]]
	tab=dat[dat["Count"]>10]
	tab=tab["CBC"]
	print(tab.head())
	tab.to_csv(outfile,sep="\t",index=False)
