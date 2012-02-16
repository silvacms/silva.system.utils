
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

    def run(self, root, options):
        if not options.identifier:
            fail(u"Please provide a source identifier.")
        logger.info('Finding documents')

        if options.folder:
            root = root.restrictedTraverse(options.folder)

        for count, content in enumerate(walk_silva_tree(root)):
            if not IDocument.providedBy(content):
                continue
            version = content.get_viewable()
            if version is not None:
                for node in version.content.documentElement.childNodes:
                    if node.nodeName == 'source':
                        if node.attr.id == options.identifier:
                            logger.error('Document %s uses source %s' % (
                                    '/'.join(content.getPhysicalPath()),
                                    options.identifier))
