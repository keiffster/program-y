"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.braintree import BraintreeStore


class FileBraintreeStore(FileStore, BraintreeStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)
        BraintreeStore.__init__(self)

    def _get_storage_path(self):
        return self.storage_engine.configuration.braintree_storage.file

    def get_storage(self):
        return self.storage_engine.configuration.braintree_storage

    def _save(self, client_context, pattern_graph):

        braintree_fullpath = self.storage_engine.configuration.braintree_storage.file
        YLogger.info(self, "Saving braintree to %s", braintree_fullpath)

        braintree_dirpath = self._get_dir_from_path(braintree_fullpath)
        self._ensure_dir_exists(braintree_dirpath)

        fileformat = self.storage_engine.configuration.braintree_storage.format
        encoding = self.storage_engine.configuration.braintree_storage.encoding

        if fileformat == FileStore.TEXT_FORMAT:
            with open(braintree_fullpath, "w+", encoding=encoding) as dump_file:
                pattern_graph.dump(output_func=dump_file.write, eol="\n")

        elif fileformat == FileStore.XML_FORMAT:
            braintree = '<?xml version="1.0" encoding="%s"?>\n' % encoding
            braintree += '<aiml>\n'
            braintree += pattern_graph.root.to_xml(client_context)
            braintree += '</aiml>\n'
            with open(braintree_fullpath, "w+", encoding=encoding) as dump_file:
                dump_file.write(braintree)

        else:
            YLogger.error(client_context, "Unknown braintree content type [%s]", fileformat)

    def save_braintree(self, client_context, pattern_graph):

        try:
            self._save(client_context, pattern_graph)

        except Exception as exc:
            YLogger.exception_nostack(client_context, "Failed to save Braintree", exc)
