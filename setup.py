from setuptools import setup

setup(name='trends-earth-cli',
      version='1.0.3',
      description='Library to interact with trends-earth',
      author='Sergio Gordillo, Raul Requero',
      author_email='sergio.gordillo@vizzuality.com,raul.requero@vizzuality.com',
      license='MIT',
      packages=['tecli'],
      package_data={'': ['run/Dockerfile', 'skeleton/requirements.txt', 'skeleton/src/__init__.py', 'skeleton/src/main.py']},
      install_requires=[
          'fire==0.1.0',
          'PyYAML==3.12',
          'requests==2.13.0',
          'termcolor==1.1.0',
          'python-dateutil==2.6.0'
      ],
      entry_points={
          "console_scripts": [
              "trends=tecli:main"
          ]
      },
      zip_safe=False)
