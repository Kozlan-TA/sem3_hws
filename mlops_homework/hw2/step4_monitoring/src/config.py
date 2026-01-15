import yaml

def load_config(filepath):
    try:
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f'Ошибка загрузки config\'а: {e}')