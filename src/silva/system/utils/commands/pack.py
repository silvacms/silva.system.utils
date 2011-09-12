# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from silva.system.utils.script import NEED_ZOPE_RUNNING, fail
import time
import logging

logger = logging.getLogger('silva.system')


class PackCommand(object):
    flags = NEED_ZOPE_RUNNING

    def get_options(self, factory):
        parser = factory(
            'pack',
            help="pack a root database")
        parser.add_argument(
            "--days", type=int, default=3,
            help="number of days to keep")
        parser.set_defaults(plugin=self)

    def run(self, db, options):
        if options.days < 0:
            fail("Cannot pack in the future.")
        logger.info('Packing root database ...')
        db.pack(time.time()-options.days*86400)


