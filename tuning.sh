VECTORDIR=tuning_vectors
RESULTDIR=tuning_result
DATADIR=/media/ke/Data/Experiment_Vectors_Results_Dec25-Jan/w2v/vectors
CBDIR=../CB-SGwithPP

mkdir -p "${VECTORDIR}"
mkdir -p "${RESULTDIR}"

for i in `seq 100 50 100`
do
  sed -i "1d" "${DATADIR}"/t9_s${i}w8ns25_cbow.bin.txt

  python retrofit.py -i "${DATADIR}"/t9_s${i}w8ns25_cbow.bin.txt -l lexicons/ppdb2.pkl -n 10 -o "${VECTORDIR}"/fuzzyretro_cbow_t9_s${i}w8ns25.vec

  python "${CBDIR}"/compute-wordsim.py "${VECTORDIR}"/fuzzyretro_cbow_t9_s${i}w8ns25.vec "${CBDIR}"/SimLex-999.csv > "${RESULTDIR}"/999_retro_cbow_t9_s${i}w8ns25.txt

done
