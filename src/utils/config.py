import json

def load_config(file_path='../configs/config.json'):
#def load_config(file_path='../configs/config.json'):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def get_config_section(section_name):
    config = load_config()
    return config.get(section_name, {})

def get_vehicle_config():
    return get_config_section('VEHICLE')

def get_display_config():
    return get_config_section('DISPLAY')







