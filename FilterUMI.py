import sys


if __name__=="__main__":
	outfile=sys.argv[1]
	num=5
	if len(sys.argv)>2:
		num=int(sys.argv[2])
	sys.stderr.write("Iterate over input!\n")
	line=sys.stdin.readline()

	cur_cbc=""
	cur_umi=""
	cur_class=""
	count=0
	I=0
	while len(line)>1:
		cur=line
		I=I+1
		if I % 100000 == 0:
			sys.stderr.write(str(I)+"\n")
		line=sys.stdin.readline()

		##gets the new cbc/umi/class
		cur_cbc=cur.split("\t")[0]	
		cur_umi=cur.split("\t")[1]
		cur_class=cur.split("\t")[2]
		count=int(cur.split("\t")[3])
		##if same as last read, continue

		##else, if changed and >1 read match write the output
		if count>num:
			toSave=cur_cbc+"\t"+cur_class+"\n"
			#toSave=cur_cbc+"\t"+cur_umi+"\t"+cur_class+"\t1\n"
			print(toSave)
			#sys.stdin.write(toSave)

		#update to new cbc/umi/class/count values


