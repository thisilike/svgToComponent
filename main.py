from os import walk, makedirs
from shutil import rmtree
from tqdm import tqdm
try:
    from yaml import Loader, load
except:
    raise Exception('yaml not installed. you can install it with: "pip install pyyaml".')

def load_config():
    try:
        with open('config.yml', 'r', encoding='utf-8') as config_file:
            config = load(config_file, Loader=Loader)
    except:
        config = dict()
    set_defaults(config)
    return config

def set_defaults(config):
    settings_name = 'inputFolderPath'
    default_setting = './input'
    if config.get(settings_name) is None:
        print('"', settings_name + '" not set in config, default to "', default_setting, '"')
        config['settings_name'] = default_setting
    print('config loaded: ', settings_name,' = "', config.get(settings_name), '"')
    
    settings_name = 'outputFolderPath'
    default_setting = './output'
    if config.get(settings_name) is None:
        print('"', settings_name + '" not set in config, default to "', default_setting, '"')
        config['settings_name'] = default_setting
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
    config = load_config()
    
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