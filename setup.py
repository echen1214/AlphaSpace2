from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='alphaspace',
      version='2.0',
      description='Protein topographical mapping tool',
      url='http://github.com/lenhsherr/alphaspace',
      author='Haotian Li',
      author_email='hl2368@nyu.edu',
      license='MIT',
      packages=['alphaspace'],
      package_data={'Examples': ['*'], },
      scripts=['bin/alphaspace2'],
      include_package_data=True,
      zip_safe=False,

      install_requires=['mdtraj',
                        'cython',
                        'configargparser',
                        'scipy',
                        ]

      )
