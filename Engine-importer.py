import os
import re
import shutil

# find public node, if there is "alias output __out: engine;" in the next line, get public node name
def get_engine_name(filename):
    with open(filename, 'r') as f:
        for line in f:
            if re.match(r'^public node', line):
                next_line = f.readline()
                if re.match(r'^\s*alias output __out: engine;', next_line):
                    return line.split()[2]
                
# find public node, if there is "alias output __out: vehicle;" in the next line, get public node name
def get_vehicle_name(filename):
    with open(filename, 'r') as f:
        for line in f:
            if re.match(r'^public node', line):
                next_line = f.readline()
                if re.match(r'^\s*alias output __out: vehicle;', next_line):
                    return line.split()[2]

# find public node, if there is "alias output __out: transmission;" in the next line, get public node name
def get_transmission_name(filename):
    with open(filename, 'r') as f:
        for line in f:
            if re.match(r'^public node', line):
                next_line = f.readline()
                if re.match(r'^\s*alias output __out: trans;', next_line):
                    return line.split()[2]

# Create main.mr with all information gathered
def create_main_mr(filename, engine_name, vehicle_name, transmission_name):
    with open('../main.mr', 'w') as f:
        f.write('import "engine_sim.mr"\n')
        f.write('import "themes/default.mr"\n')
        f.write('import "engines/{}"\n\n'.format(filename))
        f.write('use_default_theme()\n')
        f.write('set_engine({}())\n'.format(engine_name))
        if vehicle_name:
            f.write('set_vehicle({}())\n'.format(vehicle_name))
        if transmission_name:
            f.write('set_transmission({}())\n'.format(transmission_name))

def main():
# Check if there is a "./new/" folder, if not create it, print message to put .mr file in new folder, and exit program
    if not os.path.exists('./new/'):
        os.makedirs('./new/')
        print('Please put .mr file in new folder')
        exit()

# Check if there is a .mr file in new folder, if not print message to put .mr file in new folder, and exit program
    if not os.listdir('./new/'):
        print('Please put .mr file in new folder')
        exit()

# Check if there is a .mr file in new folder, if there is, move it to current folder, get engine, vehicle, and transmission name, and create main.mr file
    for filename in os.listdir('./new/'):
        if filename.endswith('.mr'):
            shutil.move('./new/{}'.format(filename), './')
            engine_name = get_engine_name(filename)
            vehicle_name = get_vehicle_name(filename)
            transmission_name = get_transmission_name(filename)
            create_main_mr(filename, engine_name, vehicle_name, transmission_name)
            break

if __name__ == '__main__':
    main()
