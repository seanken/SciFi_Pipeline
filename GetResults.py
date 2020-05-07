import pandas
import sys


if __name__=="__main__":
	args=sys.argv
	print("Load Data!")
	counts=pandas.read_csv(args[1],sep="\t",names=["Count_CBC","Equiv"])
	t2g=pandas.read_csv(args[2],sep="\t",names=["Trans","Gene","GeneName"])
	equiv2t=pandas.read_csv(args[3],sep="\t",names=["Equiv","Trans_num"])
	trans=pandas.read_csv(args[4],sep="\t",names=["Trans"])
	outfile=args[5]

	print("Make Nice!")
	trans["Trans_num"]=[i for i in range(0,trans.shape[0])]
	counts["Count_CBC"]=[val.strip() for val in counts["Count_CBC"]]

	counts["Count"]=[int(val.split(" ")[0]) for val in counts["Count_CBC"]]
	counts["CBC"]=[val.split(" ")[1] for val in counts["Count_CBC"]]
	
	print(counts.head())
	print(t2g.head())
	print(equiv2t.head())
	print(trans.head())



	print("")
	print("Perform some joins")
	print("Want map from equiv to genes")
	trans=pandas.merge(trans,t2g)
	trans=pandas.merge(trans,equiv2t)
	print(trans.head())
	print("Get number of genes per equiv")
	tab=trans.groupby(by=["Equiv"]).agg({'GeneName':'nunique'}).reset_index()
	print(tab.columns)
	tab.columns=["Equiv","NumGenes"]
	print(tab.head())

	trans=pandas.merge(trans,tab)
	trans=trans.drop_duplicates("Equiv")
	print(trans.head())
	print(trans.shape)
	trans=trans[trans["NumGenes"]==1]
	print(trans.shape)
	trans=trans[["Equiv","GeneName"]]
	print(trans.head())
	print("Number")
	print(sum([i for i in counts["Count"]]))
	print(counts.shape)
	counts=pandas.merge(trans,counts,how="inner")
	print(sum([i for i in counts["Count"]]))

	print(counts.shape)

	print(counts.head())
	counts=counts[["CBC","GeneName","Count"]]
	print(counts.head())

	print("Save!")
	counts.to_csv(outfile,sep="\t")
