from pathlib import Path
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile


BASE_LIB_URL = 'https://github.com/fubark/cyber/releases/download/latest/'
ZIP_URL = 'https://github.com/fubark/cyber/archive/refs/tags/latest.zip'


lib_urls = [
    'libcyber.so',
    # 'libcyber.so',
    'libcyber.dylib',
    'libcyber-arm64.dylib',
    'cyber.dll',
]


dst_dir = Path('cyber/lib')


r = urlopen(ZIP_URL)
myzip = ZipFile(BytesIO(r.read()))
with open(dst_dir / 'cyber.h', 'wb') as f:
    f.write(myzip.open('cyber-latest/src/cyber.h').read())


for path in lib_urls:
    url = BASE_LIB_URL + path
    r = urlopen(url)

    with open(dst_dir / path, 'wb') as f:
        f.write(r.read())
