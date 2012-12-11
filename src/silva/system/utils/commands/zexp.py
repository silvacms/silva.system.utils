
from silva.system.utils.script import NEED_ZOPE_SESSION, NEED_SILVA_SESSION
from silva.core.interfaces import IContainer

import logging

logger = logging.getLogger('silva.system')

def file_opener(gzip=False):
    file_open = open
    if gzip:
        import gzip
        file_open = gzip.open
    return file_open


class ExportZEXPCommand(object):

    flags = NEED_ZOPE_SESSION

    def get_options(self, factory):
        parser = factory(
            'zexp_export',
            help='export a content into a ZEXP')
        # parser.add_argument('--gzip', action='store_true',
        #     help='Use gzip compression.')
        parser.add_argument('path', help='path to export')
        parser.add_argument('outfile', help='path to the ouput zip file')
        parser.set_defaults(plugin=self)

    def run(self, root, options):
        path = options.path
        try:
            content = root.restrictedTraverse(path)
            connection = content._p_jar
            with open(options.outfile, 'wb') as f:
                connection.exportFile(content._p_oid, f)
        except KeyError:
            logger.error('Invalid path')
            exit(1)


class ImportZEXPCommand(object):
    flags = NEED_SILVA_SESSION

    def get_options(self, factory):
        parser = factory(
            'zexp_import',
            help='import a ZEXP file')
        # parser.add_argument('--gzip', action='store_true',
        #     help='Input is a gzip file')
        parser.add_argument(
            'file', help='ZEXP file to import')
        parser.add_argument(
            'paths', nargs=1,
            help='path to Silva sites to work on')
        parser.add_argument(
            'target',
            help='path in Silva where to import the ZEXP',
            default='/')
        parser.set_defaults(plugin=self)

    def run(self, root, options):
        path = options.target
        if not path.startswith('/'):
            path = '/' + path
        container_path, content_id = path.rsplit('/', 1)
        try:
            import_root = root.restrictedTraverse(container_path)
        except KeyError:
            logger.error('Invalid path')
            exit(1)

        if not IContainer.providedBy(import_root):
            logger.error('Import root is not a container')
            exit(2)

        with open(options.file, 'rb') as f:
            logger.info('Importing...')
            content = import_root._p_jar.importFile(f)
            logger.info('Inserting content at %s...',
                        "/".join(import_root.getPhysicalPath()) + path)
            import_root._setObject(content_id, content)
            content.id = content_id
