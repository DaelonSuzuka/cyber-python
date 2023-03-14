from pathlib import Path
from urllib.request import urlopen


BASE_URL = 'https://github.com/DaelonSuzuka/cyber/releases/download/latest/'


lib_urls = [
    'libcyber.so',
    # 'libcyber.so',
    'libcyber.dylib',
    'libcyber-arm64.dylib',
    'cyber.dll',
]


dst_dir = Path('cyber/lib')


for path in lib_urls:
    url = BASE_URL + path
    r = urlopen(url)
    
    with open(dst_dir / path, 'wb') as f:
        f.write(r.read())
