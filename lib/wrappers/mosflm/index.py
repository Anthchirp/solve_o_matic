import os
import sys

if not os.environ.has_key('XIA2CORE_ROOT'):
    raise RuntimeError, 'XIA2CORE_ROOT not defined'

sys.path.append(os.path.join(os.environ['XIA2CORE_ROOT'],
                             'Python'))

from Driver.DriverFactory import DriverFactory

def Mosflm_index(DriverType = None):

    DriverInstance = DriverFactory.Driver(DriverType)

    class Mosflm_indexWrapper(DriverInstance.__class__):

        def __init__(self):
            # generic things
            DriverInstance.__class__.__init__(self)
            self.set_executable('ipmosflm')

            self._template = None
            self._directory = None
            self._images = []
            
            self._cell = None
            self._spacegroup = None
            self._mosaic = None

            self._matrix = None
            
            return

        def set_template(self, template):
            self._template = template
            return

        def set_directory(self, directory):
            self._directory = directory
            return

        def add_image(self, image):
            self._images.append(image)
            return

        def set_spacegroup(self, spacegroup):
            self._spacegroup = spacegroup
            return

        def get_spacegroup(self):
            return self._spacegroup

        def get_cell(self):
            return self._cell

        def get_mosaic(self):
            return self._mosaic

        def get_matrix(self):
            return self._matrix

        def index(self):
            assert(self._template != None)
            assert(self._directory != None)
            assert(self._images != [])

            self.start()
            self.input('newmat mosflm_index.mat')
            self.input('template %s' % self._template)
            self.input('directory %s' % self._directory)
            if self._spacegroup:
                self.input('symmetry %s' % self._spacegroup)
            for image in self._images:
                self.input('autoindex dps refine image %d' % image)
            self.input('mosaic estimate')
            self.input('go')
            self.close_wait()

            # now pull out the output...

            for record in self.get_all_output():
                if 'Final cell' in record and 'after refinement' in record:
                    self._cell = tuple(map(float, record.split()[-6:]))
                if 'Refining solution #' in record:
                    self._spacegroup = record.split()[5]
                if 'The mosaicity has been estimated as' in record:
                    self._mosaic = float(record.split()[7])

            self._matrix = os.path.join(self.get_working_directory(),
                                        'mosflm_index.mat')

            return
            
            
    return Mosflm_indexWrapper()


if __name__ == '__main__':

    mi = Mosflm_index()

    mi.set_template('thaumatin_ssad_1_####.img')
    mi.set_directory('/data2/gw56/dls/dna/nt1956-6/thaumatin_ssad')
    for image in [1, 45, 90]:
        mi.add_image(image)
    mi.index()
                     
    print 'Unit cell: %.3f %.3f %.3f %.3f %.3f %.3f' % mi.get_cell()
    print 'Spacegroup: %s' % mi.get_spacegroup()
    print 'Mosaic: %.2f' % mi.get_mosaic()
    