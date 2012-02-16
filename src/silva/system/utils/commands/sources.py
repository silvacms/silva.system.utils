
import logging

from silva.system.utils.script import NEED_SILVA_SESSION, fail
from silva.core.services.utils import walk_silva_tree
from Products.SilvaDocument.interfaces import IDocument

logger = logging.getLogger('silva.system')


class FindSourcesCommand(object):
    """Find documents that use code sources.
    """
    flags = NEED_SILVA_SESSION

    def get_options(self, factory):
        parser = factory(
            'find_sources',
            help='find documents that uses a source')
        parser.add_argument(
            "-u", "--username",
            help="username to login in order to convert files")
        parser.add_argument(
            "-i", "--identifier",
            help="source identifier to look for")
        parser.add_argument(
            "-f", "--folder",
            help="sub folder to look for")
        parser.add_argument(
            "paths", nargs="+",
            help="path to Silva sites to work on")
        parser.set_defaults(plugin=self)

    def inspect(self, version, identifier):
        if version is not None:
            root = version.content.documentElement
            for node in root.getElementsByTagName('source'):
                if node.attributes['id'].nodeValue == identifier:
                    logger.warn("Document '%s' uses source '%s'." % (
                            '/'.join(version.getPhysicalPath()),
                            identifier))

    def run(self, root, options):
        if not options.identifier:
            fail(u"Please provide a source identifier.")
        if options.folder:
            root = root.restrictedTraverse(options.folder)

        logger.info("Finding documents with source '%s' in '%s'." % (
                options.identifier,
                '/'.join(root.getPhysicalPath())))

        documents = 0
        for content in walk_silva_tree(root):
            if not IDocument.providedBy(content):
                continue
            documents += 1
            self.inspect(content.get_viewable(), options.identifier)
            self.inspect(content.get_editable(), options.identifier)
        logger.info('Verified %d documents.' % documents)
