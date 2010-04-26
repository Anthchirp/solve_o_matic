import os
import sys

if not os.environ.has_key('XIA2CORE_ROOT'):
    raise RuntimeError, 'XIA2CORE_ROOT not defined'

sys.path.append(os.path.join(os.environ['XIA2CORE_ROOT'],
                             'Python'))

from Driver.DriverFactory import DriverFactory
from Decorators.DecoratorFactory import DecoratorFactory

# N.B. this does *not* inherit from the CCP4 Driver enhancements - as hklin
# &c. behave differently. May want to change this decision and retain the
# overloading of set_hklin etc. though if loggraph parsing proves to be useful.

example_script = '''
  phaser << eof
  mode mr_auto
  hklin f.mtz
  labin F=F SIGF=SIGF
  ensemble model pdb 2VHK.pdb identity 100
  composition protein mw 25600 num 1
  search ensemble model num 1
  root mr
  eof'''

def Phaser(DriverType = None):

    DriverInstance = DriverFactory.Driver(DriverType)

    class PhaserWrapper(DriverInstance.__class__):

        def __init__(self):

            self.set_executable('phaser')

            self._hklin = None
            self._hklout = None
            self._xyzin = None
            self._xyzout = None

            # FIXME code around this for cases where the identity is 100%
            # - i.e. copy the sequence from the input pdb file

            self._sequence = None

            self._mode = 'MR'

            return

        def set_sequence(self, sequence):
            self._sequence = sequence
            return

        def get_sequence(self):
            return self._sequence

        def set_hklin(self, hklin):
            self._hklin = hklin
            return
        
        def get_hklin(self):
            return self._hklin

        def set_hklout(self, hklout):
            self._hklout = hklout
            return
        
        def get_hklout(self):
            return self._hklout

        def set_xyzin(self, xyzin):
            self._xyzin = xyzin
            return
        
        def get_xyzin(self):
            return self._xyzin

        def set_xyzout(self, xyzout):
            self._xyzout = xyzout
            return
        
        def get_xyzout(self):
            return self._xyzout

    return PhaserWrapper()

if __name__ == '__main__':
    # run a test...
