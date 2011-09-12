# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from silva.system.utils.script import NEED_ZOPE_SESSION
from silva.core.interfaces import IRoot
import logging

logger = logging.getLogger('silva.system')


class ListingCommand(object):
    flags = NEED_ZOPE_SESSION

    def get_options(self, factory):
        parser = factory(
            'list',
            help="list all site in the database")
        parser.set_defaults(plugin=self)

    def run(self, root, options):
        logger.info('Listing silva sites')
        for content in root.objectValues():
            if IRoot.providedBy(content):
                logger.info('%s (version %s)' % (
                        '/'.join(content.getPhysicalPath()),
                        content.get_silva_content_version()))
