import os
from dotenv import load_dotenv
from pathlib import Path

dir: Path = Path(__file__).resolve().parent.parent


dotenv_path = Path(f'{dir}/variables_entorno.env')
load_dotenv(dotenv_path=dotenv_path)

client = os.getenv('SPOTIPY_CLIENT_ID')
secret = os.getenv('SECRET_ID')
url_direct = os.getenv('URL_DIRECT')


def pritnEnvironment():
    print(f'El id del client es: {client}')
    print(f'El id del secret es: {secret}')
    print(f'La url direct es: {url_direct}')


if __name__ == '__main__':
    pritnEnvironment()
