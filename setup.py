from distutils.core import setup
setup(
  name='netjson-robustness-analyser',
  packages=['netjson-robustness-analyser'],
  version='0.1',
  description='A library to perform some robustness analysis on '
          'NetJSON-defined graphs',
  author='Leonardo Maccari',
  author_email='maccari@disi.unitn.it',
  url='https://github.com/netCommonsEU/netjson-robustness-analyser',
  download_url='https://github.com/netCommonsEU/netjson-robustness-analyser/'
               'archive/0.1.tar.gz',
  keywords=['NetJSON', 'graph analysis', 'robustness'],
  install_requirements='networkx',
  classifiers=[],
)
