#! /bin/bash

#$ -cwd
#$ -q broad
#$ -P regevlab
#$ -l h_vmem=50g
#$ -e count.chi.err
#$ -o count.chi.out
#$ -l h_rt=8:00:00
#$ -l os=RedHat7

#$ -t 1-2

source /broad/software/scripts/useuse


use .python-3.6.0


export PATH=$PATH:/home/unix/ssimmons/.local/bin/:/home/unix/ssimmons/.local/lib/python3.6/site-packages/kb_python/bins/linux/bustools:/home/unix/ssimmons/.local/lib/python3.6/site-packages/kb_python/bins/linux/kallisto

#SEEDFILE=fastq.txt
SEEDFILE=../../Results_Mar14/fastq.txt
#SGE_TASK_ID=1

R1=$(awk "NR==$SGE_TASK_ID" $SEEDFILE | awk '{print $1}') #read 1
R2=$(awk "NR==$SGE_TASK_ID" $SEEDFILE | awk '{print $2}')
R3=$(awk "NR==$SGE_TASK_ID" $SEEDFILE | awk '{print $3}') #read 3


R1=../$R1
R2=../$R2
R3=../$R3
echo $R1

outdir=$(awk "NR==$SGE_TASK_ID" $SEEDFILE | awk '{print $4}')

outdir=${outdir}_Chi

echo $outdir

mkdir $outdir

index=/stanley/levin_dr/ssimmons/SciFi/Kallisto/transcriptome.idx
t2g=/stanley/levin_dr/ssimmons/SciFi/Kallisto/transcripts_to_genes.txt

echo First Run Kallisto!
kallisto bus -i $index -x 0,8,21,2,0,16:0,0,8:1,0,0 -o $outdir $R1 $R3 $R2

echo Next, create white list
echo Extract Counts!
bustools text -p $outdir/output.bus | awk '{print $1}' | sort | uniq -c | sort > $outdir/read.counts.txt 
echo Make list!
python MakeWhiteListSimple.py $outdir/read.counts.txt $outdir/whitelist.txt


echo Correct the CBC!
bustools correct -o $outdir/corrected.bus -w $outdir/whitelist.txt $outdir/output.bus


echo Got bus file! Next sort busfile:
bustools sort -o $outdir/corrected.sorted.bus $outdir/corrected.bus


echo Filter out CBC/UMI/class pairs that only have one read supporting them and create count matrix for equaivalence classes
bustools text -p $outdir/corrected.sorted.bus | python ChimeraFilter.py  $outdir/tpt.txt | sort | uniq -c | sed 1d > $outdir/umi.counts.txt
#cp $outdir/corrected.sorted.bus $outdir/filt.bus

echo Go from equivalance classes to genes, and done!!
#TO IMPLEMENT
python Split.EC.py $outdir/matrix.ec $outdir/equiv.to.trans.txt
python GetResults.py $outdir/umi.counts.txt $t2g $outdir/equiv.to.trans.txt $outdir/transcripts.txt $outdir/count.genes.txt



#echo Create count matrix!
#bustools count -o $outdir/counts -g $t2g -e $outdir/matrix.ec -t $outdir/transcripts.txt --genecounts $outdir/filt.bus





#kb count -i  $index -g $t2g -x 0,8,21,2,0,16:0,0,8:1,0,0 -o $outdir --filter bustools $R1 $R3 $R2
