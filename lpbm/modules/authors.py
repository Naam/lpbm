# lpbm/modules/authors.py - Loads and manipulates authors.
# Author: Franck Michea < franck.michea@gmail.com >
# License: New BSD License (See LICENSE)

'''
Author manager, getting authors configuration in blog sources and loading all
the authors.
'''

import os
import sys

import lpbm.models.configmodel as cm_module
import lpbm.exceptions
import lpbm.logging
import lpbm.module_loader
import lpbm.tools as ltools

from lpbm.models.authors import Author

class Authors(lpbm.module_loader.ModelManagerModule):
    '''
    Author manager, getting authors configuration in blog sources and loading
    all the authors.
    '''

    # pylint: disable=C0321
    def abstract(self): return 'Loads, manipulates and renders authors.'
    def model_cls(self): return Author
    def name(self): return 'authors'
    def object_name(self): return 'author'

    def init(self):
        super().init()

    def load(self, modules, args):
        filename = ltools.join(args.exec_path, 'authors.cfg')
        self.cm = cm_module.ConfigModel(filename)

        # Now loads all authors.
        for section in self.cm.config.sections():
             self.register_object(Author, section)

    # Random module functions internal to lpbm
    def is_valid(self, authors):
        authors = ltools.split_on_comma(authors)
        ids = [o.id for o in self.objects]
        for author in authors:
            try:
                if int(author) not in ids:
                    print('Author id {} is invalid!'.format(author))
                    return False
            except ValueError:
                print('One of the ids is not a valid integer: {}'.format(author))
                return False
        return True

    # Particular functions requested on command line.
    def opt_new(self):
        '''Interactively create an author.'''
        super().opt_new(None)
