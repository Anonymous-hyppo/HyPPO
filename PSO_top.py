
import random
from genus_run import *
from generate_combinations import *
from fitness import *
from verilog_generator import *
from tcl_generator_genus import *
from invoke_genus import *
from extract_ppa import *
from error_calc import *
# from xdc_generator import *
# from cleaner import *
# import os
# from timeit import default_timer as timer
import math
import csv
from tqdm import tqdm


# global csv_file


# Define the SSIM fitness function
def fitness_vivado(combo_pso,csv_writer,pastcombo):
   print(combo_pso)
   combo=[]


   for y in combo_pso:
       if y>0:
           combo.append(y)
   # print(combo)




   # if sum(combo) < no_bits :
   #     fitness = float('inf')
   # else :
           
   if combo not in pastcombo :
       pastcombo.append(combo)
       verilog_generator(decimals_coefficients, decimals_sp,combo)
       invoke_genus(combo)
       tcl_generator(combo)
       # xdc_generator(5) # Check check check
       genus_run()
       mae_calc(combo)


   obtained_mae = extract_mae(combo)
   power = extract_power_opt(combo)
   area  = extract_area_opt(combo)
   delay = extract_delay_opt(combo)


   fitness = area
   print(f"Combo = {combo} ; delay = {delay} ; Area={area} ; power = {power} ; fitness = {fitness}, error = {obtained_mae}")
   csv_writer.writerow([combo,fitness,power,delay,area, obtained_mae])
       # clean()
   return fitness, obtained_mae




#--------------------------------------------inputs--------------------------------------------#


decimals_coefficients = [ 0.004746947172222, 0.941711629577653, 0.416301883059278, 0.713966714212242, 0.642298105875394, 0.504286731180926]
decimals_sp = [0.00, 0.437500000000000, 0.757812500000000]


# range_start = 10
# range_end = 20
# comb_set_no = 3


#----------------------------------------------------------------------------------------------#






# combinations = generate_combinations_func(range_start, range_end, comb_set_no)
# combinations_list = list(combinations)


############################################################################################################################






# PSO parameters
max_iterations = 30
num_particles = 30


past_combo=[]


csv_file = open(f'./csvfiles/values_fitness.csv', 'w')
csv_writer = csv.writer(csv_file)




csv_writer.writerow([f'Combo','fitness','power','delay','area', 'mae'])




num_dimensions = 2    # No of elements in a combination






c1 = 2.0  # Cognitive coefficient
c2 = 2.0  # Social coefficient
w = 0.7   # Inertia weight


# Define bounds for each dimension
min_bound = 3
max_bound = 10


# Initialize particles
particles = [{'position': [random.randint(min_bound, max_bound) for _ in range(num_dimensions)],
             'velocity': [random.uniform(-1, 1) for _ in range(num_dimensions)],
             'best_position': None,
             'best_fitness': float('inf')}
            for _ in range(num_particles)]




global_best_position = list(particles[0]['position'])
global_best_fitness = float('inf')
mae = float('inf')


# target_error = mae_calc([11,10,9])
target_error = 0.00477


# PSO optimization loop
for iteration in range(max_iterations):
   print("\n\n\nIteration Number : ",iteration+1)
   particle_num=0
   for particle in particles:
       print("\n    Particle Number : ",particle_num+1)
       print("\n\n\nIteration Number : ",iteration+1)
       # print(f"particle value : {particle['position']}")
       # Ensure particle positions are within bounds
       particle['position'] = [min(max(p, min_bound), max_bound) for p in particle['position']]




       # Evaluate fitness using the Rosenbrock function
       fitness, mae = fitness_vivado(particle['position'],csv_writer,past_combo)
       # fitness = rosenbrock_fitness(particle['position'])


       # Update personal best
       if fitness < particle['best_fitness']:
           particle['best_fitness'] = fitness
           particle['best_position'] = particle['position']


       # Update global best
       if fitness < global_best_fitness:
           if mae <= target_error: # if fitness satisfies, the check for the error metric ------> Check if this condition can be written better
               global_best_fitness = fitness
               global_best_position = list(particle['position'])


       # Update velocity and position
       for i in range(num_dimensions):
           # print(f"best position : {particle['best_position']}")
           # print(f"particle position cognitive: {particle['position']}")
           # print(f"global best : {global_best_position}")
           cognitive = c1 * random.uniform(0, 1) * (particle['best_position'][i] - particle['position'][i])
           social = c2 * random.uniform(0, 1) * (global_best_position[i] - particle['position'][i])
           particle['velocity'][i] = w * particle['velocity'][i] + cognitive + social
           particle['position'][i] = int(round(particle['position'][i] + particle['velocity'][i]))




       
       particle_num=particle_num+1


csv_writer.writerow([])
csv_writer.writerow([])
csv_writer.writerow(["Optimal Solution : ", global_best_position, "Optimal Fitness : ", global_best_fitness])


# Print the results
print("\n\n\nOptimal Solution:", global_best_position)
print("Optimal Fitness:", global_best_fitness)
