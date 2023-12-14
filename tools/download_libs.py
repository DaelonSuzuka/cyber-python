from pathlib import Path
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile


VERSION = '0.3'

BASE_LIB_URL = f'https://github.com/fubark/cyber/releases/download/{VERSION}/'
ZIP_URL = f'https://github.com/fubark/cyber/archive/refs/tags/{VERSION}.zip'


lib_urls = [
    'libcyber-linux-x64.a',
    'libcyber-macos-arm64.a',
    'libcyber-macos-x64.a',
    'libcyber-windows-x64.lib',
]


dst_dir = Path('cyber/lib')


r = urlopen(ZIP_URL)
myzip = ZipFile(BytesIO(r.read()))
with open(dst_dir / 'cyber.h', 'wb') as f:
    f.write(myzip.open(f'cyber-{VERSION}/src/include/cyber.h').read())


for path in lib_urls:
    url = BASE_LIB_URL + path
    r = urlopen(url)

    with open(dst_dir / path, 'wb') as f:
        f.write(r.read())
