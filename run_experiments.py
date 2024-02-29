import pickle
import glob
import os
import time

from src.experiment import run_experiment, run_sleep

from datetime import datetime
from random import shuffle



editors = ["subl", 'gedit']
template_files = ["lorem_ipsum.txt", "python_code_template_2.txt", "python_code_template.txt"]
target_files = ['notes.txt', 'python_code.py', "python_code.py"]
window_sizes = ['fullscreen', '600x400']


sample_size = 30

def run_full_experiment():
    timestamp = str(datetime.now().strftime("%d%m%Y%H%M%S"))

    current_dir = os.path.dirname(os.path.realpath(__file__))
    results_path = os.path.join(current_dir, 'results', timestamp)

    os.mkdir(results_path)

    # Warmup
    run_experiment("subl", template="lorem_ipsum.txt", target_file='notes.txt', window_size='fullscreen')
    run_experiment("gedit", template="lorem_ipsum.txt", target_file='notes.txt', window_size='fullscreen')

    time.sleep(5)

    for i in range(sample_size):
        experiment_parameters = []
        for editor in editors:
            for j, template in enumerate(template_files):
                for window_size in window_sizes:
                    store_file = generate_file_name(editor, template, window_size, i)
                    store_path = os.path.join(results_path, store_file)
                    experiment_parameters.append((editor, template, target_files[j], window_size, store_path))
        shuffle(experiment_parameters)

        for editor, template, target_file, window_size, store_path in experiment_parameters:

            run_experiment(editor, template=template, target_file=target_file, window_size=window_size, store_path=store_path)
            time.sleep(5)
        run_sleep(os.path.join(results_path, "sleep_" + str(i + 1)))

def generate_file_name(editor, template, window_size, i):
    return editor + '_' + template.split('.')[0] + '_' + window_size + '_' + str(i + 1) + '.pkl'

def process_results():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    list_of_results = glob.glob(os.path.join(current_dir, 'results', '*'))
    latest_results = max(list_of_results, key=os.path.getctime)

    results_dict = {}

    for i in range(sample_size):
        for editor in editors:
            for template in template_files:
                for window_size in window_sizes:

                    file = os.path.join(latest_results, generate_file_name(editor, template, window_size, i))
                    
                    with open(file, 'rb') as f:
                        energibridge_output = pickle.load(f)

                    key = editor + ', ' + window_size + ', ' + template
                    
                    energy_delta, time_delta = process_energibrdige_output(energibridge_output)
                    if key not in results_dict:
                        results_dict[key] = []
                    results_dict[key].append(round(energy_delta / time_delta, 5))
    
        # TODO: fix duplicate code
        file = os.path.join(latest_results, "sleep_" + str(i + 1))
                        
        with open(file, 'rb') as f:
            energibridge_output = pickle.load(f)

        key = "sleep"
        
        energy_delta, time_delta = process_energibrdige_output(energibridge_output)
        if key not in results_dict:
            results_dict[key] = []
        results_dict[key].append(round(energy_delta / time_delta, 5))

    for key, value in results_dict.items():
        print(key + ": " + str(value))

                    

    

def process_energibrdige_output(energibridge_output):
    energibridge_output = compute_total_energy(energibridge_output)

    energy_delta = energibridge_output['TOTAL_ENERGY (J)'][-1] - energibridge_output['TOTAL_ENERGY (J)'][0]
    time_delta = int(energibridge_output['Time'][-1]) - int(energibridge_output['Time'][0])

    return energy_delta, time_delta / 1000
    

# Computes the total energy use by adding the energy use of all cores.
def compute_total_energy(energibridge_output, n_cores = 4):
    energibridge_output["TOTAL_ENERGY (J)"] = []

    n_measurements = len(energibridge_output['Delta'])
    
    for i in range(n_measurements):
        energibridge_output["TOTAL_ENERGY (J)"].append(0)
        for core in range(1, n_cores):
            energibridge_output["TOTAL_ENERGY (J)"][i] += float(energibridge_output["CORE" + str(core) + "_ENERGY (J)"][i])

    return energibridge_output



if __name__ == '__main__':
    run_full_experiment()
    process_results()