VECTORDIR=tuning_vectors
RESULTDIR=tuning_result
DATADIR=/media/ke/新加卷/w2v_vectors
CBDIR=../CB-SGwithPP

mkdir -p "${VECTORDIR}"
mkdir -p "${RESULTDIR}"

for i in `seq 100 50 800`
do
  sed -i "1d" "${DATADIR}"/t9_s${i}w8ns25_cbow.bin.txt

  python retrofit.py -i "${DATADIR}"/t9_s${i}w8ns25_cbow.bin.txt -l lexicons/ppdb-xl.txt -n 10 -o "${VECTORDIR}"/retro_cbow_t9_s${i}w8ns25.vec

  python "${CBDIR}"/compute-wordsim.py "${VECTORDIR}"/retro_cbow_t9_s${i}w8ns25.vec "${CBDIR}"/SimLex999.csv > "${RESULTDIR}"/999_retro_cbow_t9_s${i}w8ns25.txt

  python "${CBDIR}"/compute-wordsim.py "${VECTORDIR}"/retro_cbow_t9_s${i}w8ns25.vec "${CBDIR}"/WS353.csv > "${RESULTDIR}"/353_retro_cbow_t9_s${i}w8ns25.txt

  python "../glove/eval/python"/evaluate.py --vocab_file=../SNetSG_ts/vocab_text9.txt --vectors_file="${VECTORDIR}"/retro_cbow_t9_s${i}w8ns25.vec > "${RESULTDIR}"/qw_retro_cbow_t9_s${i}w8ns25.txt
done
