#This file is an example run file that outputs the folder-files for splash page in a standard python-flask structure. To run it, all you need to do is cd into output_src/ and type "flask run"

from EasyFlask import source_build


if __name__ == '__main__':
    file_in = 'splash_page.yamlish'
    output_dir = 'output_src/'
    source_build.full_build(file_in=file_in, output_dir=output_dir)