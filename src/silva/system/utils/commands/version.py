# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from silva.core.services.utils import walk_silva_tree
from silva.core.interfaces import IVersionedContent
from silva.system.utils.script import fail, NEED_SILVA_RUNNING
import transaction
import logging

logger = logging.getLogger('silva.system')


def purge_old_versions(root, keep):
    count = 0
    for count, content in enumerate(walk_silva_tree(root)):
        if not IVersionedContent.providedBy(content):
            continue
        versions = content._previous_versions
        if not versions:
            continue
        if count and count % 500 == 0:
            # Commit now and when
            transaction.commit()

        removable_versions = versions[:-keep]
        content._previous_versions = versions[-keep:]

        contained_ids = content.objectIds()
        removable_version_ids = set([
            str(version[0]) for version in removable_versions
            if version[0] in contained_ids])

        content.manage_delObjects(list(removable_version_ids))


class CleanupVersionCommand(object):
    """Clean old Silva versions.
    """
    flags = NEED_SILVA_RUNNING

    def get_options(self, factory):
        parser = factory(
            'version',
            help="clean old version of versioned content")
        parser.add_argument(
            "--keep", type=int, default=1,
            help="number of previous version to keep")
        parser.add_argument(
            "paths", nargs="+",
            help="path to Silva sites to work on")
        parser.set_defaults(plugin=self)

    def run(self, root, options):
        if options.keep < 1:
            fail("You need to keep at least one version")
        logger.info('Removing old versions')
        purge_old_versions(root, options.keep)
        transaction.commit()

