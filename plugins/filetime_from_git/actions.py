# -*- coding: utf-8 -*-
import base64
import hashlib
import logging
import os

from pelican.utils import strftime

from .registration import content_git_object_init
from .utils import datetime_from_timestamp
from .utils import string_to_bool


logger = logging.getLogger(__name__)


@content_git_object_init.connect
def filetime_from_git(content, git_content):
    '''
    Update modification and creation times from git
    '''
    if not content.settings['GIT_FILETIME_FROM_GIT']:
        # Disabled for everything
        return

    if not string_to_bool(content.metadata.get('gittime', 'yes')):
        # Disable for this content
        return

    file_exist = True
    path = content.source_path
    try:
        fs_creation_time = datetime_from_timestamp(os.stat(path).st_ctime, content)
        fs_modified_time = datetime_from_timestamp(os.stat(path).st_mtime, content)
    except FileNotFoundError:
        logger.warn(path + " is not exist")
        file_exist = False
        fs_creation_time = datetime_from_timestamp(None, content)
        fs_modified_time = datetime_from_timestamp(None, content)

    # 1. file is not managed by git
    #    date: fs time
    # 2. file is staged, but has no commits
    #    date: fs time
    # 3. file is managed, and clean
    #    date: first commit time, update: last commit time or None
    # 4. file is managed, but dirty
    #    date: first commit time, update: fs time
    if git_content.is_managed_by_git():
        if git_content.is_committed():
            content.date = git_content.get_oldest_commit_date()

            if git_content.is_modified():
                if content.settings['GIT_WARN_MODIFIED']:
                    logger.warn(path + " is modified without commited")
                content.modified = fs_modified_time
            else:
                content.modified = git_content.get_newest_commit_date()
        else:
            # File isn't committed
            if content.settings['GIT_WARN_NOT_COMMITED']:
                logger.warn(path + " is not committed")
            content.date = fs_creation_time
    else:
        # file is not managed by git
        if file_exist and content.settings['GIT_WARN_NOT_MANAGED']:
            logger.warn(path + " is not managed by git")
        content.date = fs_creation_time

    # Clean up content attributes
    if not hasattr(content, 'modified'):
        content.modified = content.date

    if hasattr(content, 'date'):
        content.locale_date = strftime(content.date, content.date_format)

    if hasattr(content, 'modified'):
        content.locale_modified = strftime(
            content.modified, content.date_format)


@content_git_object_init.connect
def git_sha_metadata(content, git_content):
    '''
    Add sha metadata to content
    '''
    if not content.settings['GIT_SHA_METADATA']:
        return

    if not git_content.is_committed():
        return

    content.metadata['gitsha_newest'] = str(git_content.get_newest_commit())
    content.metadata['gitsha_oldest'] = str(git_content.get_oldest_commit())


def update_hash_from_str(hsh, str_input):
    """
    Convert a str to object supporting buffer API and update a hash with it.
    """
    byte_input = str(str_input).encode("UTF-8")
    hsh.update(byte_input)


@content_git_object_init.connect
def git_permalink(content, git_content):
    '''
    Add git based permalink id to content metadata
    '''
    if not content.settings['GIT_GENERATE_PERMALINK']:
        return

    if not string_to_bool(content.metadata.get('git_permalink', 'yes')):
        # Disable for this content
        return

    if not git_content.is_committed():
        return

    permalink_hash = hashlib.sha1()
    update_hash_from_str(permalink_hash, git_content.get_oldest_commit())
    update_hash_from_str(permalink_hash, git_content.get_oldest_filename())
    git_permalink_id_raw = base64.urlsafe_b64encode(permalink_hash.digest())
    git_permalink_id = git_permalink_id_raw.decode("UTF-8")
    permalink_id_metadata_key = content.settings['PERMALINK_ID_METADATA_KEY']

    if permalink_id_metadata_key in content.metadata:
        content.metadata[permalink_id_metadata_key] = (
            ','.join((
                content.metadata[permalink_id_metadata_key], git_permalink_id))
        )
    else:
        content.metadata[permalink_id_metadata_key] = git_permalink_id
