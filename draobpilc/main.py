#!/usr/bin/env python3

# Copyright 2015 Ivan awamper@gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import signal
import logging
import argparse

from gi.repository import Gtk
from draobpilc import get_data_path
from draobpilc import common
from draobpilc import version
from draobpilc.lib import utils
from draobpilc.application import Application

DESKTOP_FILE_PATH = os.path.join(
    os.path.expanduser('~/.local/share/applications'),
    '%s.desktop' % version.APP_NAME
)


def install_desktop_file():
    desktop_tpl = get_data_path('desktop_file.tpl')

    if os.path.exists(DESKTOP_FILE_PATH):
        print(_('File "%s" already exists.' % DESKTOP_FILE_PATH))
        return False

    with open(desktop_tpl, encoding='utf-8') as tpl_file:
        contents = tpl_file.read()
        contents = contents.replace('{APP_VERSION}', str(version.APP_VERSION))
        contents = contents.replace('{APP_NAME}', version.APP_NAME)
        contents = contents.replace('{COMMENT}', version.APP_DESCRIPTION)
        contents = contents.replace('{EXEC}', 'draobpilc')
        contents = contents.replace('{ICON}', common.ICON_PATH)

        with open(DESKTOP_FILE_PATH, 'w', encoding='utf-8') as desktop_file:
            desktop_file.write(contents)

    return True


def uninstall_desktop_file():
    if not os.path.exists(DESKTOP_FILE_PATH):
        print(_('File "%s" doesn\'t exits.' % DESKTOP_FILE_PATH))
        return False

    os.remove(DESKTOP_FILE_PATH)
    return True


def run():
    parser = argparse.ArgumentParser(description='GPaste GUI')
    parser.add_argument('-d', '--debug',
        action='store_true',
        default=False,
        dest='debug'
    )
    parser.add_argument('--install-desktop-file',
        action='store_true',
        default=False,
        dest='install_desktop_file',
        help=_('Add "Draobpilc.desktop" to "~/.local/share/applications"')
    )
    parser.add_argument('--uninstall-desktop-file',
        action='store_true',
        default=False,
        dest='uninstall_desktop_file',
        help=_('Remove "Draobpilc.desktop" from "~/.local/share/applications"')
    )
    parser.add_argument('--version',
        action='version',
        version=str(version.APP_VERSION_STRING)
    )
    args = parser.parse_args()

    msg_f = '%(asctime)s %(levelname)s\t%(filename)s:%(lineno)d \t%(message)s'
    time_f = '%H:%M:%S'

    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format=msg_f,
            datefmt=time_f
        )

        # Gtk hates "-d" switch, so lets drop it
        if '-d' in sys.argv:
            sys.argv.remove('-d')
        if '--debug' in sys.argv:
            sys.argv.remove('--debug')
    else:
        logging.basicConfig(
            level=logging.WARN,
            format=msg_f,
            datefmt=time_f
        )

    if args.install_desktop_file:
        install_desktop_file()
        sys.exit()
    if args.uninstall_desktop_file:
        uninstall_desktop_file()
        sys.exit()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)


if __name__ == '__main__':
    run()
