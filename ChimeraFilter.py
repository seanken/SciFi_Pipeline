import sys


if __name__=="__main__":
	outfile=sys.argv[1]
	fil=open(outfile,"w")
	sys.stderr.write("Iterate over input!\n")
	line=sys.stdin.readline()

	cur_cbc=""
	cur_umi=""
	cur_class=""
	counts=[]
	equiv=[]
	count=0
	I=0
	while len(line)>1:
		cur=line
		I=I+1
		if I % 100000 == 0:
			sys.stderr.write(str(I)+"\n")
		line=sys.stdin.readline()

		##gets the new cbc/umi/class
		new_cbc=cur.split("\t")[0]	
		new_umi=cur.split("\t")[1]
		new_class=cur.split("\t")[2]
		count=int(cur.split("\t")[3])
		##if same as last read, continue
		if new_cbc==cur_cbc and new_umi==cur_umi:
			counts.append(count)
			equiv.append(new_class)
			continue;
		tot=sum(counts)
		TPT=[coun/tot for coun in counts]
		for i in range(0,len(TPT)):
			fil.write(str(TPT[i])+"\n")
			if TPT[i]<.25:
				continue;
			toSave=cur_cbc+"\t"+equiv[i]+"\n"
			print(toSave)
		equiv=[]
		counts=[]
		cur_umi=new_umi
		cur_cbc=new_cbc

	

		tot=sum(counts)
		TPT=[coun/tot for coun in counts]
		for i in range(0,len(TPT)):
			if TPT[i]<.1:
				continue;
			toSave=cur_cbc+"\t"+equiv[i]+"\n"
			print(toSave)
		cur_umi=new_umi
	fil.close()
