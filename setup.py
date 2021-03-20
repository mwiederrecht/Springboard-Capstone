from distutils.core import setup


def readme():
    """Import the README.md Markdown file and try to convert it to RST format."""
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError):
        with open('README.md') as readme_file:
            return readme_file.read()


setup(
    name='springboard-capstone',
    version='1.0.0',
    description='All-inclusive repo of steps for data collection, cleaning, model training, and a web app for utilizing the model for the keywording project I did for my Springboard Capstone.',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    url='https://github.com/mwiederrecht/springboard-capstone',
    author='Melissa Wiederrecht',
    author_email='mwiederrecht@gmail.com',
    license='UNLICENCED',
    packages=['app'],
    install_requires=[
        'pypandoc>=1.4',
        'watermark>=1.8.1',
        'pandas>=0.24.2',
        'pytest>=4.3.1',
        'pytest-runner>=4.4',
        'starlette==0.13.6',
        'tensorflow>=2.3.1',
        'pillow>=7.2',
        'uvicorn==0.11.7',
        'keras==2.4.3',
        'python-multipart==0.0.5',
        'numpy==1.18.0',
        'gevent==20.6.2',
        'h5py==2.10.0',
        'aiofiles==0.5.0',
        'aiohttp==3.6.2',
        'asyncio==3.4.3',
        'scrapy==2.1.0',
        'fire==0.4.0'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
