import os
import sys
import pickle 
import time
import subprocess
import psutil
from datetime import datetime

def run_experiment(editor_name, template, target_file, window_size, store_path=None):

    editor_process = open_editor(editor_name, target_file)

    time.sleep(1)

    set_window_size(window_size)
    
    command = generate_pretender_command(template)
    
    energibridge_output = execute_energibridge(command)

    close_editor(editor_process)

    if store_path == None:
        return
    
    with open(store_path, 'wb') as f:
        pickle.dump(energibridge_output, f)

def run_sleep(store_path):
    
    command = "sleep 10"
    
    energibridge_output = execute_energibridge(command)

    with open(store_path, 'wb') as f:
        pickle.dump(energibridge_output, f)

def close_editor(editor_process):
    editor_process.terminate()

    # For some reason, sublime text does not terminate with the other command
    for proc in psutil.process_iter():
        if proc.name() == 'sublime_text':
            proc.kill()

# Generate a command that executes the script that pretends to be a human typing
def generate_pretender_command(template):
    python_executable = sys.executable

    current_dir = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(current_dir, '..', 'templates', template)
    pretender_path = os.path.join(current_dir, 'human_pretender.py')

    return python_executable + ' ' + pretender_path + ' ' + template_path


def open_editor(editor_name, target_file):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_path = os.path.join(current_dir, '..', 'target_files', target_file)

    editor_process = subprocess.Popen([editor_name, target_path])

    return editor_process


def set_window_size(window_size):
    window_id = int(subprocess.run(['xdotool', 'search', '--name', 'target_files'], capture_output = True).stdout)
    if window_size == 'fullscreen':
        subprocess.run(['wmctrl', '-i', '-r', str(window_id), '-b' 'toggle,fullscreen'])
    else:
        width = window_size.split('x')[0]
        height = window_size.split('x')[1]
        subprocess.run(['xdotool', 'windowsize', str(window_id), width, height])
    

# Execute command (wrapped in energibridge) and parse output into dict
def execute_energibridge(command):
    cmd = "energibridge --summary " + command
    lines = list(os.popen(cmd))

    energibridge_output = {}

    keys = lines[0].strip().split(',')

    for key in keys:
        energibridge_output[key] = []

    for line in lines[1:]:
        for index, value in enumerate(line.strip().split(',')):
            energibridge_output[keys[index]].append(value)

    return energibridge_output

