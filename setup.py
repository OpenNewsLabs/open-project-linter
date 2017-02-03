from distutils.core import setup

setup(
    name='Open Project Linter',
    version='0.1dev',
    packages=['openlinter'],
    license='Apache v2.0',
    description='Automatic checklist for open source project best practices.',
    author='Frances Hocutt',
    author_email='frances.hocutt+gh@gmail.com',
    entry_points={
        'console_scripts': []
    }
)
