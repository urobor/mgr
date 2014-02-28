import glob
import os
import ConfigParser

script_dir = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(script_dir, 'config', 'autocascader.ini'))
to_root = config.get('paths', 'script_to_root')

# Objects
objects_mark_dir = os.path.join(script_dir, to_root,
                                config.get('paths', 'objects_mark_dir'))
sol_path = os.path.join(objects_mark_dir, 'solaris.txt')
fro_path = os.path.join(objects_mark_dir, 'front.txt')
bac_path = os.path.join(objects_mark_dir, 'background.txt')
sol = open(sol_path, 'w')
fro = open(fro_path, 'w')
bac = open(bac_path, 'w')
for i, id_path in enumerate(glob.glob(os.path.join(objects_mark_dir, '*'))):
        
    if(id_path.endswith("txt")):
        continue
    print os.path.basename(id_path)
    for j, type_path in enumerate(glob.glob(os.path.join(id_path, '*'))):
        num = 0
        f = open(type_path, 'r')
        for k, line in enumerate(f):
            if(type_path.endswith('solaris.txt')):
                sol.write(line)
            if(type_path.endswith('front.txt')):
                fro.write(line)
            if(type_path.endswith('background.txt')):
                bac.write(line)
        f.close()
fro.close()
bac.close()
sol.close()