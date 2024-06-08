
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
       verilog_generator(decimals_coefficients, decimals_sp, decimals_coefficients1, decimals_sp1, combo)
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


decimals_coefficients = [-1.38969368784555e-05,1.00180303809062,-0.0346608520878083,
                        0.138380195244790,0.992171770706222,-0.103546222855846,
                        0.274991166192216,0.963216482665988,-0.171082833823530,
                        0.407967791923376,0.914729985941142,-0.236326691900638,
                        0.535365318905679,0.846302570913861,-0.298262142616927,
                        0.655035998865252,0.757209333609685,-0.355753099203657,
                        0.764528313635175,0.646105287552906,-0.407444261026624,
                        0.860760383691764,0.510388681417401,-0.451557531933264,
                        0.939389638802240,0.344010121212614,-0.485304779411492,
                        0.992138485152333,0.125247741018008,-0.498812356378983]

decimals_sp = [0.00	,0.138839721679688,	0.278594970703125,	0.420242309570313,
              0.564956665039063,	0.714248657226563,	0.870330810546875	,1.03678894042969,	1.22088623046875,	1.44532775878906]
decimals_coefficients1 = [1.38997265948326e-05,0.999045605652702,
                        0.0756404684767055,0.994976082273178,
                        0.122710132067811,0.991055904557702,
                        0.138407993264794,0.987540094576632,
                        0.175582338713714,0.981293525636010,
                        0.208957888381137,0.974477718170707,
                        0.239648173936725,0.967176845344251,
                        0.268270394711140,0.960846139577210
                        ]

decimals_sp1 = [0.00,0.0756988525390625	,0.123016357421875, 0.138839721679688	,0.176483154296875,	0.210494995117188,	0.241989135742188,	0.271591186523438]



# range_start = 10
# range_end = 20
# comb_set_no = 3


#----------------------------------------------------------------------------------------------#






# combinations = generate_combinations_func(range_start, range_end, comb_set_no)
# combinations_list = list(combinations)


############################################################################################################################






# PSO parameters
max_iterations = 100
num_particles = 50


past_combo=[]


csv_file = open(f'./csvfiles/values_fitness.csv', 'w')
csv_writer = csv.writer(csv_file)




csv_writer.writerow([f'Combo','fitness','power','delay','area', 'mae'])




num_dimensions = 5    # No of elements in a combination






c1 = 2.0  # Cognitive coefficient
c2 = 2.0  # Social coefficient
w = 0.7   # Inertia weight


# Define bounds for each dimension
min_bound = 7
max_bound = 15


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
target_error = 0.0000139

# PSO optimization loop
for iteration in range(max_iterations):
   print("\n\n\nIteration Number : ",iteration+1)
   particle_num=0
   for particle in particles:
       print("\n    Particle Number : ",particle_num+1)
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

       particle_num = particle_num+1


csv_writer.writerow([])
csv_writer.writerow([])
csv_writer.writerow(["Optimal Solution : ", global_best_position, "Optimal Fitness : ", global_best_fitness])


# Print the results
print("\n\n\n Optimal Solution:", global_best_position)
print("Optimal Fitness:", global_best_fitness)
