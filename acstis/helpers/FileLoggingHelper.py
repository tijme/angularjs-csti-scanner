# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2017 Tijme Gommers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import colorlog

class FileLoggingHelper:
    """The FileLoggingHelper enables logging messages to a file.

    Attributes:
        __phantomjs_driver (str): The cached path to the executable PhantomJS driver.

    """

    __filename = None

    @staticmethod
    def set_file(filename=None):
        """Set the filename to log messages to.

        Args:
            filename (str): The filename (including absolute or relative path) to log to.

        Note:
            If the log filename already exists it will be appended with a number. So output.log
            could become `output.log.1` or `output.log.2`.

        """

        if not filename:
            return

        filename_backup = filename
        filename_append = 0
        filename_changed = False
        filename_error = False

        while os.path.isfile(filename) and not filename_error:
            filename_changed = True
            filename_append += 1
            filename = filename_backup + "." + str(filename_append)

            if filename_append == sys.maxsize:
                filename_error = True

        if filename_error:
            colorlog.getLogger().error("The output log file already exists and therefore no logs will be written.")
            return

        if filename_changed:
            colorlog.getLogger().warning("The output log filename was changed to `" + filename + "` since `" + filename_backup + "` already exists.")

        FileLoggingHelper.__filename = filename

    @staticmethod
    def log(message):
        """Write the given message to the initialized log file.

        Args:
            message (str): The message to write to the log file.

        """

        with open(FileLoggingHelper.__filename, "a") as log:
            log.write(message + "\n")
