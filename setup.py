from distutils.core import setup

setup(name='color-describer',
      version='0.1',
      description='',
      author='',
      author_email='',
      url='https://github.com/stanfordnlp/color-describer',
      packages=['stanza', 'tensorflow'],
      # package_dir = {'': ''},
      py_modules=['colordesc', 'colorutils', 'speaker', 'vectorizers'],
      # data_files=[('rugstk', ['rugstk/example.py'])]
      # package_data={'': ['stanza', 'tensorflow', 'thirdparty/*', 'rugstk/*']}
)
