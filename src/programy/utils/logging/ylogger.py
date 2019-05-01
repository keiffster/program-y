"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import logging
import traceback


class YLoggerSnapshot(object):

    def __init__(self, criticals=0, fatals=0, errors=0, exceptions=0, warnings=0, infos=0, debugs=0):
        self._criticals = criticals
        self._fatals = fatals
        self._errors = errors
        self._exceptions = exceptions
        self._warnings = warnings
        self._infos = infos
        self._debugs = debugs

    def __str__(self):
        return "Critical(%d) Fatal(%d) Error(%d) Exception(%d) Warning(%d) Info(%d), Debug(%d)" % (
            self._criticals, self._fatals, self._errors, self._exceptions, self._warnings, self._infos, self._debugs
        )

    def to_json(self):
        return {
                "criticals":    self._criticals,
                "fatals":       self._fatals,
                "errors":       self._errors,
                "exceptions":   self._exceptions,
                "warnings":     self._warnings,
                "infos":        self._infos,
                "debugs":       self._debugs
        }


class YLogger(object):

    CRITICALS = 0
    FATALS = 0
    ERRORS = 0
    EXCEPTIONS = 0
    WARNINGS = 0
    INFOS = 0
    DEBUGS = 0

    @staticmethod
    def snapshot():
        return YLoggerSnapshot(YLogger.CRITICALS,
                               YLogger.FATALS,
                               YLogger.ERRORS,
                               YLogger.EXCEPTIONS,
                               YLogger.WARNINGS,
                               YLogger.INFOS,
                               YLogger.DEBUGS)

    @staticmethod
    def reset_snapshot():
        YLogger.CRITICALS = 0
        YLogger.FATALS = 0
        YLogger.ERRORS = 0
        YLogger.EXCEPTIONS = 0
        YLogger.WARNINGS = 0
        YLogger.INFOS = 0
        YLogger.DEBUGS = 0

    @staticmethod
    def format_message(caller, message):
        if caller is not None:
            if hasattr(caller, "ylogger_type"):
                log_type = caller.ylogger_type()
                if log_type == 'client':
                    return "[%s] - %s" % (caller.id, message)
                elif log_type == 'bot':
                    return "[%s] [%s] - %s" % (caller.client.id if caller.client is not None else "",
                                               caller.id, message)
                elif log_type == 'brain':
                    clientid = ""
                    botid = ""
                    if caller.bot is not None:
                        if caller.bot.client is not None:
                            clientid = caller.bot.client.id
                        botid = caller.bot.id
                    return "[%s] [%s] [%s] - %s" % (clientid, botid, caller.id, message)
                elif log_type == 'context':
                    return "[%s] [%s] [%s] [%s] - %s" % (caller.client.id if caller.client is not None else "",
                                                         caller.bot.id if caller.bot is not None else "",
                                                         caller.brain.id if caller.brain is not None else "",
                                                         caller.userid, message)
        return message

    @staticmethod
    def critical(caller, message, *args, **kwargs):
        YLogger.CRITICALS += 1
        if logging.getLogger().isEnabledFor(logging.CRITICAL):
            logging.critical(YLogger.format_message(caller, message), *args, **kwargs)

    @staticmethod
    def fatal(caller, message, *args, **kwargs):
        YLogger.FATALS += 1
        if logging.getLogger().isEnabledFor(logging.FATAL):
            logging.fatal(YLogger.format_message(caller, message), *args, **kwargs)

    @staticmethod
    def error(caller, message, *args, **kwargs):
        YLogger.ERRORS += 1
        if logging.getLogger().isEnabledFor(logging.ERROR):
            logging.error(YLogger.format_message(caller, message), *args, **kwargs)

    @staticmethod
    def exception_nostack(caller, message, exception, *args, **kwargs):
        YLogger.EXCEPTIONS += 1
        if logging.getLogger().isEnabledFor(logging.ERROR):
            excep_msg = "%s [%s]"%(message, str(exception))
            logging.error(YLogger.format_message(caller, excep_msg), *args, **kwargs)

    @staticmethod
    def exception(caller, message, exception, *args, **kwargs):
        YLogger.EXCEPTIONS += 1
        if logging.getLogger().isEnabledFor(logging.ERROR):
            excep_msg = "%s [%s]"%(message, str(exception))
            logging.error(YLogger.format_message(caller, excep_msg), *args, **kwargs)
            tb_lines = [line.rstrip('\n') for line in
                        traceback.format_exception(exception.__class__, exception, exception.__traceback__)]
            for line in tb_lines:
                logging.exception(YLogger.format_message(caller, line))

    @staticmethod
    def warning(caller, message, *args, **kwargs):
        YLogger.WARNINGS += 1
        if logging.getLogger().isEnabledFor(logging.WARNING):
            logging.warning(YLogger.format_message(caller, message), *args, **kwargs)

    @staticmethod
    def info(caller, message, *args, **kwargs):
        YLogger.INFOS += 1
        if logging.getLogger().isEnabledFor(logging.INFO):
            logging.info(YLogger.format_message(caller, message), *args, **kwargs)

    @staticmethod
    def debug(caller, message, *args, **kwargs):
        YLogger.DEBUGS += 1
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(YLogger.format_message(caller, message), *args, **kwargs)


