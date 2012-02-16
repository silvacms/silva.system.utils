
import logging

from Products.SilvaExternalSources.interfaces import ICodeSource
from Products.SilvaDocument.interfaces import IDocument
from silva.core.services.utils import walk_silva_tree
from silva.system.utils.script import NEED_SILVA_SESSION

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

    def find_existing_sources(self, root):
        logger.info("Finding sources in '%s'." % (
                '/'.join(root.getPhysicalPath())))
        sources = 0
        for content in walk_silva_tree(root):
            if ICodeSource.providedBy(content):
                logger.warn("Found source '%s'." % (
                        '/'.join(content.getPhysicalPath())))
                sources += 1
        logger.info('Found %d sources.' % sources)

    def find_document_sources(self, root, identifier):
        logger.info("Finding documents with source '%s' in '%s'." % (
                identifier,
                '/'.join(root.getPhysicalPath())))
        documents = 0
        for content in walk_silva_tree(root):
            if not IDocument.providedBy(content):
                continue
            documents += 1
            self.inspect_document(content.get_viewable(), identifier)
            self.inspect_document(content.get_editable(), identifier)
        logger.info('Verified %d documents.' % documents)

    def inspect_document(self, version, identifier):
        if version is not None:
            root = version.content.documentElement
            for node in root.getElementsByTagName('source'):
                if node.attributes['id'].nodeValue == identifier:
                    logger.warn("Document version '%s' uses source '%s'." % (
                            '/'.join(version.getPhysicalPath()),
                            identifier))

    def run(self, root, options):
        if options.folder:
            root = root.restrictedTraverse(options.folder)

        if not options.identifier:
            self.find_existing_sources(root)
        else:
            self.find_document_sources(root, options.identifier)

