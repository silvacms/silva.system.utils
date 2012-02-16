
import logging

from Products.SilvaDocument.interfaces import IDocument
from Products.SilvaExternalSources.interfaces import ICodeSource
from silva.core.interfaces import ISilvaObject, IContainer
from silva.system.utils.script import NEED_SILVA_SESSION

logger = logging.getLogger('silva.system')


THRESHOLD = 1000

def walk_silva_tree(content, requires=ISilvaObject):
    """A generator to lazily get all the Silva object from a content /
    container.
    """
    count = 0
    if requires.providedBy(content):
        # Version are indexed by the versioned content itself
        yield content
    if IContainer.providedBy(content):
        for child in content.objectValues():
            for content in walk_silva_tree(child):
                count += 1
                yield content
                if count > THRESHOLD:
                    # Review ZODB cache
                    content._p_jar.cacheGC()
                    count = 0


class FindSourcesCommand(object):
    """Find documents that use code sources.
    """
    flags = NEED_SILVA_SESSION

    def get_options(self, factory):
        parser = factory(
            'find_sources',
            help='find code sources')
        parser.add_argument(
            "-u", "--username",
            help="username to login in order to convert files")
        parser.add_argument(
            "-i", "--identifier",
            help="find document that uses that source")
        parser.add_argument(
            "-f", "--folder",
            help="folder to restrict the search to")
        parser.add_argument(
            "paths", nargs="+",
            help="path to Silva sites to work on")
        parser.set_defaults(plugin=self)

    def find_existing_sources(self, root):
        logger.info("Finding sources in '%s'." % (
                '/'.join(root.getPhysicalPath())))
        sources = 0
        for source in walk_silva_tree(root, requires=ICodeSource):
            logger.warn("Found source '%s'." % (
                    '/'.join(source.getPhysicalPath())))
            sources += 1
        logger.info('Found %d sources.' % sources)

    def find_document_sources(self, root, identifier):
        logger.info("Finding documents with source '%s' in '%s'." % (
                identifier,
                '/'.join(root.getPhysicalPath())))
        documents = 0
        for document in walk_silva_tree(root, requires=IDocument):
            documents += 1
            self.inspect_document(document.get_viewable(), identifier)
            self.inspect_document(document.get_editable(), identifier)
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
