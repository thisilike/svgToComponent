from os import walk, makedirs
from shutil import rmtree
from tqdm import tqdm
try:
    from yaml import Loader, load
except:
    raise Exception('yaml not installed. you can install it with: "pip install pyyaml".')

def check_config(config):
    settings_name = 'inputFolderPath'
    if config.get(settings_name) is None:
        raise Exception(settings_name + ' not set in config')
    print('config loaded: ', settings_name,' = "', config.get(settings_name), '"')
    
    settings_name = 'outputFolderPath'
    if config.get(settings_name) is None:
        raise Exception(settings_name + ' not set in config')
    print('config loaded: ', settings_name,' = "', config.get(settings_name), '"')

def convert(input_path: str, config: dict):
    nf = '<template>\n'
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            nf += '\t' + line + '\n'
    nf = nf[:-1] + '</template>'
    
    output_path = input_path.replace(config.get('inputFolderPath'), config.get('outputFolderPath'), 1)
    output_path = output_path[:-4] + '.vue'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(nf)


def main():
    with open('config.yml', 'r', encoding='utf-8') as config_file:
        config = load(config_file, Loader=Loader)
    check_config(config)
    
    rmtree('./output')

    file_paths = list()
    
    for path, dirs, files in walk(config.get('inputFolderPath')):
        path = path.replace('\\', '/')
        for file in files:
            if file[-4:] == '.svg':
                file_paths.append((path, file))
            
    for path, file in tqdm(file_paths, desc='Converting:', ascii=True):
        try:
            makedirs(path.replace(config.get('inputFolderPath'), config.get('outputFolderPath'), 1))
        except:
            pass
        convert(path + '/' + file, config)
        
    print('Finished!')

if __name__ == '__main__':
    main()