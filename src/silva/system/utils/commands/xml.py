# -*- coding: utf-8 -*-
# Copyright (c) 2013  Infrae. All rights reserved.
# See also LICENSE.txt

from silva.core.interfaces import IContainer
from silva.core.xml import ZipImporter
from silva.system.utils.script import NEED_SILVA_SESSION
from zope.publisher.browser import TestRequest

import logging

logger = logging.getLogger('silva.system')


class XmlImportCommand(object):

    flags = NEED_SILVA_SESSION

    def get_options(self, factory):
        parser = factory('xml_import',
            help="Import from silva xml (ZIP) file.")
        parser.add_argument(
            'file', help='Silva XML file to import')
        parser.add_argument(
            'paths', nargs=1,
            help='path to Silva sites to work on, ex: /silvaroot')
        parser.add_argument(
            'target',
            help='path in Silva where to import to, ex: /silvaroot/folder',
            default='/')
        parser.add_argument(
            '--replace',
            help="replace content if it already exists.",
            action='store_true',
            default=False)
        parser.set_defaults(plugin=self)

    def run(self, root, options):
        try:
            import_root = root.restrictedTraverse(options.target)
        except KeyError as e:
            logger.error('invalid target path : %s %s',
                         options.target, e.args[0])
            exit(1)

        if not IContainer.providedBy(import_root):
            logger.error('invalid import base, not a container.')
            exit(1)

        with open(options.file, 'r') as input_archive:
            importer = ZipImporter(
                import_root, TestRequest(),
                {'replace': options.replace})
            importer.importStream(input_archive)
