
import logging

from silva.system.utils.script import NEED_SILVA_SESSION
from silva.core.services.interfaces import IFilesService
from zope.component import getUtility
import transaction


logger = logging.getLogger('silva.system')


class ConvertFileCommand(object):
    """Call the convert file command.
    """
    flags = NEED_SILVA_SESSION

    def get_options(self, factory):
        parser = factory(
            'convert_files',
            help="convert file storage")
        parser.add_argument(
            "-u", "--username",
            help="username to login in order to convert files")
        parser.add_argument(
            "paths", nargs="+",
            help="path to Silva sites to work on")
        parser.set_defaults(plugin=self)

    def run(self, root, options):
        logger.info("Converting files.")

        service = getUtility(IFilesService)
        service.convert_storage(root)
        logger.info("Done.")
        transaction.commit()


