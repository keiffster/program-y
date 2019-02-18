"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from programy.utils.logging.ylogger import YLogger

from programy.extensions.base import Extension

class HotReloadAdminExtension(Extension):

    @staticmethod
    def reload_aimls(client_context):
        YLogger.debug(client_context, "Hot reloading all AIML files")
        client_context.brain.reload_aimls()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_denormal(client_context):
        YLogger.debug(client_context, "Hot reloading Denormal")
        client_context.brain._load_denormals()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_normal(client_context):
        YLogger.debug(client_context, "Hot reloading Normal")
        client_context.brain._load_normals()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_gender(client_context):
        YLogger.debug(client_context, "Hot reloading Gender")
        client_context.brain._load_genders()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_person(client_context):
        YLogger.debug(client_context, "Hot reloading Person")
        client_context.brain._load_persons()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_person2(client_context):
        YLogger.debug(client_context, "Hot reloading Person2")
        client_context.brain._load_person2s()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_properties(client_context):
        YLogger.debug(client_context, "Hot reloading Properties")
        client_context.brain._load_properties()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_defaults(client_context):
        YLogger.debug(client_context, "Hot reloading Defaults")
        client_context.brain._load_default_variables()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_regex(client_context):
        YLogger.debug(client_context, "Hot reloading Regex")
        client_context.brain.load_regex_templates()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_patterns(client_context):
        YLogger.debug(client_context, "Hot reloading Pattern Nodes")
        client_context.brain.aiml_parser.pattern_parser._pattern_factory.load(client_context.client.storage_factory)
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_templates(client_context):
        YLogger.debug(client_context, "Hot reloading Template Nodes")
        client_context.brain.aiml_parser.template_parser._template_factory.load(client_context.client.storage_factory)
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_maps(client_context):
        YLogger.debug(client_context, "Hot reloading Maps")
        client_context.brain._load_maps()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_map(client_context, mapname):
        YLogger.debug(client_context, "Hot reloading Map [%s]", mapname)
        client_context.brain.reload_map(mapname)
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_sets(client_context):
        YLogger.debug(client_context, "Hot reloading Sets")
        client_context.brain._load_sets()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_set(client_context, setname):
        YLogger.debug(client_context, "Hot reloading Set [%s]", setname)
        client_context.brain.reload_set(setname)
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_rdfs(client_context):
        YLogger.debug(client_context, "Hot reloading Rdfs")
        client_context.brain._load_rdfs()
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_rdf(client_context, rdfname):
        YLogger.debug(client_context, "Hot reloading RDF [%s]", rdfname)
        client_context.brain.reload_rdf(rdfname)
        return 'HOTRELOAD OK'

    @staticmethod
    def reload_all(client_context):
        YLogger.debug(client_context, "Hot reloading all")
        HotReloadAdminExtension.reload_aimls(client_context)
        HotReloadAdminExtension.reload_denormal(client_context)
        HotReloadAdminExtension.reload_normal(client_context)
        HotReloadAdminExtension.reload_gender(client_context)
        HotReloadAdminExtension.reload_person(client_context)
        HotReloadAdminExtension.reload_person2(client_context)
        HotReloadAdminExtension.reload_properties(client_context)
        HotReloadAdminExtension.reload_defaults(client_context)
        HotReloadAdminExtension.reload_regex(client_context)
        HotReloadAdminExtension.reload_patterns(client_context)
        HotReloadAdminExtension.reload_templates(client_context)
        HotReloadAdminExtension.reload_sets(client_context)
        HotReloadAdminExtension.reload_maps(client_context)
        HotReloadAdminExtension.reload_rdfs(client_context)
        return "HOTRELOAD OK"

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(client_context, "Hot Reload Admin - [%s]", data)

        try:
            commands = HotReloadAdminExtension.split_into_commands(data)

            if commands[0] == 'RELOAD':
                entity = commands[1]

                if entity in ['AIML', 'DENORMAL', 'NORMAL', 'GENDER', 'PERSON', 'PERSON2', 'PROPERTIES', 'DEFAULTS', 'REGEX', 'PATTERNS', 'TEMPLATES', 'SET', 'MAP', 'RDF']:

                    if entity == 'DENORMAL':
                        return HotReloadAdminExtension.reload_denormal(client_context)

                    elif entity == 'NORMAL':
                        return HotReloadAdminExtension.reload_normal(client_context)

                    elif entity == 'GENDER':
                        return HotReloadAdminExtension.reload_gender(client_context)

                    elif entity == 'PERSON':
                        return HotReloadAdminExtension.reload_person(client_context)

                    elif entity == 'PERSON2':
                        return HotReloadAdminExtension.reload_person2(client_context)

                    elif entity == 'PROPERTIES':
                        return HotReloadAdminExtension.reload_properties(client_context)

                    elif entity == 'DEFAULTS':
                        return HotReloadAdminExtension.reload_defaults(client_context)

                    elif entity == 'REGEX':
                        return HotReloadAdminExtension.reload_regex(client_context)

                    elif entity == 'PATTERNS':
                        return HotReloadAdminExtension.reload_patterns(client_context)

                    elif entity == 'TEMPLATES':
                        return HotReloadAdminExtension.reload_templates(client_context)

                    elif entity == 'AIML':
                        if len(commands) == 3:
                            aimlname = commands[2]
                            return HotReloadAdminExtension.reload_aiml(client_context, aimlname)
                        else:
                            raise Exception ("Missing AIML name")

                    elif entity == 'SET':
                        if len(commands) == 3:
                            setname = commands[2]
                            return HotReloadAdminExtension.reload_set(client_context, setname)
                        else:
                            raise Exception ("Missing Set name")

                    elif entity == 'MAP':
                        if len(commands) == 3:
                            mapname = commands[2]
                            return HotReloadAdminExtension.reload_map(client_context, mapname)
                        else:
                            raise Exception ("Missing Map name")

                    elif entity == 'RDF':
                        if len(commands) == 3:
                            rdfname = commands[2]
                            return HotReloadAdminExtension.reload_rdf(client_context, rdfname)
                        else:
                            raise Exception ("Missing RDF name")

                elif entity == 'ALL':

                    if len(commands) == 3:
                        entities = commands[2]
                        if entities == 'AIML':
                            return HotReloadAdminExtension.reload_aimls(client_context)

                        elif entities == 'MAPS':
                            return HotReloadAdminExtension.reload_maps(client_context)

                        elif entities == 'SETS':
                            return HotReloadAdminExtension.reload_sets(client_context)

                        elif entities == 'RDFS':
                            return HotReloadAdminExtension.reload_rdfs(client_context)
                    else:
                        return HotReloadAdminExtension.reload_all(client_context)

                else:
                    raise Exception ("Unknonw reload entity [%s]"%entity)

            elif commands[0] == 'COMMANDS':
                return "RELOAD [DENORMAL|NORMAL|GENDER|PERSON|PERSON2|PROPERTIES|DEFAULTS|REGEX|PATTERNS|TEMPLATES] | [SET|MAP|RDF] NAME | ALL [AIML|MAPS|SETS|RDFS]"

            else:
                raise Exception ("Unknonw reload command [%s]"%commands[0])

        except Exception as e:
            YLogger.exception(client_context, "Failed to execute hot reload extension", e)

        return "Hot Reload Admin Error"