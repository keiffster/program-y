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
from programy.utils.logging.ylogger import YLogger
import os
import os.path
import xml.etree.ElementTree as ET

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.learnf import LearnfStore

from programy.utils.logging.ylogger import YLogger



class FileLearnfStore(FileStore, LearnfStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    @staticmethod
    def create_learnf_path(client_context, learnf_dir):
        return "%s%s%s.aiml"%(learnf_dir, os.sep, client_context.userid)

    @staticmethod
    def create_learnf_file_if_missing(learnf_path):

        if os.path.isfile(learnf_path) is False:
            try:
                YLogger.debug(None, "Creating new learnf file [%s]", learnf_path)

                with open(learnf_path, "w+", encoding="utf-8") as file:
                    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    file.write('<aiml>\n')
                    file.write('</aiml>\n')
                    file.close()

            except Exception as excep:
                YLogger.exception_nostack(None, "Error Writing learnf to %s", excep, learnf_path)

    @staticmethod
    def write_node_to_learnf_file(client_context, node, learnf_path):

        YLogger.debug(client_context, "Writing learnf to %s", learnf_path)

        try:
            tree = ET.parse(learnf_path)
        except Exception:
            # Assume invalid aiml file, so remove it and start again with a fresh copy
            os.remove(learnf_path)
            FileLearnfStore.create_learnf_file_if_missing(learnf_path)
            tree = ET.parse(learnf_path)

        root = tree.getroot()

        # Only add a new node if it doesn't already exist
        if FileLearnfStore.node_already_exists(root, node) is False:
            root.append(node)
            tree.write(learnf_path, method="xml")

    @staticmethod
    def node_already_exists(root, node):

        new_pattern = node.find('pattern')
        if new_pattern is None:
            return False

        new_pattern_str = ET.tostring(new_pattern)

        for category in root:
            current_pattern = category.find('pattern')
            if current_pattern is not None:
                current_pattern_str = ET.tostring(current_pattern)
                if current_pattern_str == new_pattern_str:
                    return True

        return False

    def _get_storage_path(self):
        if len(self.storage_engine.configuration.learnf_storage.dirs) > 1:
            YLogger.warning(self, "Learnf Storage has multiple folders specified, using first only")

        return self.storage_engine.configuration.learnf_storage.dirs[0]

    def create_category_xml_node(self, client_context, category)   :
        # Add our new element
        child = ET.Element("category")
        child.append(category.pattern)
        child.append(category.topic)
        child.append(category.that)
        xml_category = category.template.xml_tree(client_context)
        child.append(xml_category)
        return child

    def save_learnf(self, client_context, category):
        try:
            xml_node = self.create_category_xml_node(client_context, category)

            learnf_path = self._get_storage_path()
            self._ensure_dir_exists(learnf_path)

            learnf_fullpath = self.create_learnf_path(client_context, learnf_path)

            self.create_learnf_file_if_missing(learnf_fullpath)

            self.write_node_to_learnf_file(client_context, xml_node, learnf_fullpath)

        except Exception as exc:
            YLogger.exception_nostack(client_context, "Failed to save learnf", exc)
