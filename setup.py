from distutils.core import setup
# from distutils.command.install import INSTALL_SCHEMES

# for scheme in INSTALL_SCHEMES.values():
#     scheme['data'] = scheme['purelib']

setup(
    name='springboard-capstone',
    version='1.0.0',
    description='All-inclusive repo of steps for data collection, cleaning, model training, and a web app for utilizing the model for the keywording project I did for my Springboard Capstone.',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    url='https://github.com/mwiederrecht/Springboard-Capstone',
    author='Melissa Wiederrecht',
    author_email='mwiederrecht@gmail.com',
    license='UNLICENCED',
    packages=['app'],
    install_requires=[
        'pypandoc>=1.5',
        'watermark>=1.8.1',
        'pandas>=1.2.0',
        'pytest>=4.3.1',
        'pytest-runner>=4.4',
        'starlette==0.14.2',
        'tensorflow>=2.4.1',
        'pillow>=8.1.2',
        'uvicorn==0.13.4',
        'keras==2.4.3',
        'python-multipart==0.0.5',
        'numpy==1.19.5',
        'gevent==20.6.2',
        'h5py==2.10.0',
        'aiofiles==0.5.0',
        'aiohttp==3.6.2',
        'asyncio==3.4.3',
        'scrapy==2.1.0',
        'fire==0.4.0',
        'requests==2.23.0',
        'scikit_learn>=0.24.1'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
