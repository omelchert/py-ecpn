P=../numExp01_small_systems
T_EQ=5e5

for N in 8 16 32 64;
do 
  echo $N
  python3 main_postprocessing.py $P/data_N${N}/ $T_EQ > res_N${N}.dat
done
