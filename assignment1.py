import numpy
import sys
import datetime
import gmpy
from gmpy import mpz
from mpi4py import MPI
from math import floor
from gap_struct import gap_struct

def numbers_gap_cmp(p1,p2,gap):
	new_gap = gap_struct(p1,p2)
	if (new_gap>gap):
		return new_gap
	else:
		return gap

def Main():
	#Get process size and rank
	comm = MPI.COMM_WORLD
	size = comm.Get_size()
	rank = comm.Get_rank()

	#Get the top boundary from the user
	if (len(sys.argv)<2 or not sys.argv[1].isdigit()):
			print("Please supply the program with the number of items")
			exit(1)
	n_input = int(sys.argv[1])

	n = int(floor(n_input/6)) 
	
	#find size of objects for p (np)
	if rank<(n%size):
		np = int(floor(n/size) + 1)
	else:
		np = int(floor(n/size))

	#find start location for p (i start,p)
	i_start = mpz(rank*floor(n/size) + min(rank,n%size))
	
	#Top boundary for current process values is the start value + size
	end_index = i_start+np

	#Barrier to measure start time before the loop
	comm.Barrier()

	#Initalizing values. process 0 is initalized with 2 and 3 as first prime numbers
	if (rank == 0):
		first_prime = mpz(2)
		second_prime = mpz(3)
		max_gap = gap_struct(first_prime,second_prime)
		wt = MPI.Wtime()
		#print("Starting at {}".format(datetime.datetime.now()))
	else:
		first_prime = None
		second_prime = None
		max_gap = gap_struct(mpz(0),mpz(1))

	second_last_prime = None
	last_prime = None
	index = i_start
	switch_iteration = True
	perc_index = 1
	#Initalize the current number to test with start value in order to pass the while condition
	curr_number = 5 + 6*i_start	

	#Loop as long as the current number is not bigger then the local upper limit and the program upper limit
	while (curr_number<=n_input and index<end_index):
		#Print percentage
		#if (index>=(i_start+perc_index*(end_index-i_start)/100)):
		#	print("{} : Processor {} is {}% done".format(datetime.datetime.now(),rank,perc_index))
		#	perc_index +=1
		#Is the current number a prime?
		if gmpy.is_prime(curr_number):
			#If it's the first prime encountered set it as the second prime (the first will be updated from neighbor)
			if (second_prime == None):
				second_prime = curr_number
			else:
				#If the current local last prime is empty, compare with the first prime encountered, else with the last
				if(second_last_prime == None):
					max_gap = numbers_gap_cmp(second_prime,curr_number,max_gap)
				else:
					max_gap = numbers_gap_cmp(second_last_prime,curr_number,max_gap)
				second_last_prime = curr_number
                #The loop iterates only over multiplications of 6 once for 5 and once for 7
		if (switch_iteration):
			curr_number = 7 + 6*index
			switch_iteration = False
			index+=1
		else:
			curr_number = 5 + 6*index
			switch_iteration = True
				
	# Send first and last values to neighbor
	if (rank>0):
		comm.send(second_prime,dest=(rank-1),tag=1)
	if (rank<size-1):
		comm.send(second_last_prime,dest=rank+1,tag=2)

	#Receive values from neighbors
	if (rank>0):
		first_prime = comm.recv(source=(rank-1),tag=2)
		if (first_prime == None):
			print("Process {} received Null as prime from left neighbor".format(rank))
		else:
			max_gap = numbers_gap_cmp(first_prime,second_prime,max_gap)
	if (rank<size-1):
		last_prime = comm.recv(source=rank+1,tag=1)
		if (last_prime == None):
			print("Process {} received Null as prime from right neighbor".format(rank))
		else:
			max_gap = numbers_gap_cmp(second_last_prime,last_prime,max_gap)
	
	#Send maximum gaps to master process 0
	if (rank>0):
		comm.send(max_gap,dest=0,tag=3)
	else:
		#Calculate max from all processes
		for p in range(1,size):
			p_max = comm.recv(source=p,tag=3)
			if (p_max>max_gap):
				max_gap = p_max
		#Print the maximum gap from all processes
		print(max_gap)
		#Print the total time the program took
		print("Total time to compute: {:2f} seconds".format(MPI.Wtime() - wt))
		#print("Done in {}".format(datetime.datetime.now()))
	
Main()


