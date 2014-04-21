# -*- coding: utf-8 -*-
#
#   med : manual editing in pipeline
#   Copyright (C) 2014 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from tempfile import mkstemp
from shutil import copyfileobj
import os
import sys
import subprocess


def main():
    editor = os.environ.get('VISUAL') or os.environ.get('EDITOR') or 'editor'

    fd, tmp_path = mkstemp()
    f = os.fdopen(fd, 'w')
    try:
        copyfileobj(sys.stdin, f)
        f.close()
        with file('/dev/tty', 'r+', 0) as tty:
            p = subprocess.Popen([editor, tmp_path], stdin=tty, stdout=tty)
            p.wait()
            if p.returncode < 0:
                raise SystemExit(p.returncode)
        with file(tmp_path) as f:
            copyfileobj(f, sys.stdout)
    finally:
        os.unlink(tmp_path)
