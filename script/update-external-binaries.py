#!/usr/bin/env python

import errno
import sys
import os

from lib.config import get_target_arch, get_platform_key
from lib.util import add_exec_bit, download, extract_zip, rm_rf, \
                     safe_mkdir, tempdir

VERSION = 'v1.4.0'
SOURCE_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
FRAMEWORKS_URL = 'http://github.com/electron/electron-frameworks/releases' \
                 '/download/' + VERSION


def main():
  os.chdir(SOURCE_ROOT)
  version_file = os.path.join(SOURCE_ROOT, 'external_binaries', '.version')

  if (is_updated(version_file, VERSION)):
    return

  rm_rf('external_binaries')
  safe_mkdir('external_binaries')

  if sys.platform == 'darwin':
    download_and_unzip('Mantle')
    download_and_unzip('ReactiveCocoa')
    download_and_unzip('Squirrel')
  elif sys.platform in ['cygwin', 'win32']:
    download_and_unzip('directxsdk-' + get_target_arch())

  download_and_unzip('sccache-'+get_platform_key()+'-'+get_target_arch())
  # https://bugs.python.org/issue15795
  add_exec_bit('external_binaries/sccache')

  with open(version_file, 'w') as f:
    f.write(VERSION)


def is_updated(version_file, version):
  existing_version = ''
  try:
    with open(version_file, 'r') as f:
      existing_version = f.readline().strip()
  except IOError as e:
    if e.errno != errno.ENOENT:
      raise
  return existing_version == version


def download_and_unzip(framework):
  zip_path = download_framework(framework)
  if zip_path:
    extract_zip(zip_path, 'external_binaries')


def download_framework(framework):
  filename = framework + '.zip'
  url = FRAMEWORKS_URL + '/' + filename
  download_dir = tempdir(prefix='electron-')
  path = os.path.join(download_dir, filename)

  download('Download ' + framework, url, path)
  return path


if __name__ == '__main__':
  sys.exit(main())
