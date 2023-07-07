#This is mainly for UI if ran directly, and supplies functions for argparse if ran in the command line

from .road_map import full_road_map

def full_build(file_in, output_dir):
    full_road_map(file_in, output_dir)

def user_interaction():
    intro = '''\
Welcome to EasyFlask!
If you're just getting started, and don't have a config file made, feel free to skip entering a file path to display the splash page.

If you're looking to create your own website, know that the directory can exist, or not, and this will create, then write to it.
    '''
    print(intro)
    output_dir = input("Directory to build in: ")
    file_in = input('Path to yamlish file: ')

    return file_in, output_dir

if __name__ == '__main__':
    file_in, output_dir = user_interaction()
    
    full_build(file_in, output_dir)


