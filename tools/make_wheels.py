from pathlib import Path
from zipfile import ZipFile

# wheel platform tag: platform dynamic lib
PLATFORMS = {
    'win_amd64': 'cyber/lib/cyber.dll',
    'macosx_10_9_x86_64': 'cyber/lib/libcyber-arm64.dylib',
    'macosx_11_0_arm64': 'cyber/lib/libcyber.dylib',
    'manylinux_2_12_x86_64.manylinux2010_x86_64.musllinux_1_1_x86_64': 'cyber/lib/libcyber.so',
}

uni_wheels = Path('dist').glob('*py3-none-any.whl')

for uni_wheel_name in uni_wheels:
    for platform, lib in PLATFORMS.items():
        platform_wheel_name = uni_wheel_name.as_posix().replace('any', platform)

        zin = ZipFile(uni_wheel_name, 'r')
        zout = ZipFile(platform_wheel_name, 'w')

        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if item.filename.startswith('cyber/lib/'):
                if item.filename == lib:
                    zout.writestr(item, buffer)
            else:
                zout.writestr(item, buffer)

        zout.close()
        zin.close()
