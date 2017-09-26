# Assignment1_python
Requires gmpy and mpi4py python packages
Sharcnet commands:
	Find best dev node:
		pdsh -w orc-dev[2-4] free | grep 'buffers\/' | awk '{print $1,$NF}' | sort -n -r -k 2
		pdsh -w orc-dev[2-4] uptime | awk '{print $1,$NF}' | sort -n -k 2
	Load python 3.4.2:
		module load python/intel/3.4.2
	Submit the jobs:
		Serial queue: sqsub -r 120m -o output_1.log -q serial python3 assignment1.py 1000000000
		Parallel queue: sqsub -r 60m -o output_2.log -q mpi -n 2 python3 assignment1.py 1000000000

Results:
	For 1,000,000,000: Gap 282 for numbers 436273009 and 436273291
	For 1,000,000,000,000: Gap 540 for numbers 738832927927 and 738832928467

Benchmark for 1,000,000,000 (full data in Benchmark.xlsx):
	Serial: 3059 seconds (51 minutes)
	2 CPUs: 1413 seconds (23.5 minutes)
	3 CPUs: 953 seconds  (15.9 minutes)
	4 CPUs: 712 seconds  (11.9 minutes)
	5 CPUs: 388 seconds  (6.5 minutes)
	6 CPUs: 324 seconds  (5.4 minutes)
	7 CPUs: 259 secodns  (4.3 minutes)
	8 CPUs: 230 seconds  (3.8 minutes)