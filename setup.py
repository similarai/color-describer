from distutils.core import setup

setup(name='color-describer',
      version='0.1',
      description='',
      author='',
      author_email='',
      url='https://github.com/stanfordnlp/color-describer',
      packages=['stanza', 'stanza.research', 'stanza.monitoring', 
      'tensorflow', 'tensorflow.core', 'tensorflow.core.util', 'tensorflow.core.framework',
      'models', 
      'rugstk', 'rugstk.core', 'rugstk.data', 'rugstk.data.munroecorpus'],
      package_data={'models': ['lstm_fourier_quick.p']},
      py_modules=['colordesc', 'colorutils', 'speaker', 'vectorizers', 'color_instances', 'neural', 'helpers'],
)
