from programy.parser.template.nodes.select import NotQuery
from programy.parser.template.nodes.select import Query
from programy.parser.template.nodes.select import QueryBase
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class MockQuery(Query):

    def __init__(self, subj, pred, obj, results):
        Query.__init__(self, subj, pred, obj)
        self._results = results

    def _get_matched_tuples(self, client_context, subj, pred, obj):
        return self._results


class MockNotQuery(NotQuery):

    def __init__(self, subj, pred, obj, results):
        NotQuery.__init__(self, subj, pred, obj)
        self._results = results

    def _get_unmatched_tuples(self, client_context, subj, pred, obj):
        return self._results


class TemplateSelectQueryTests(ParserTestsBaseClass):

    def test_querybase(self):

        query = QueryBase(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"))

        self.assertEqual("subj", query.subj.word)
        self.assertEqual("pred", query.pred.word)
        self.assertEqual("obj", query.obj.word)

        self.assertEqual("<subj>subj</subj><pred>pred</pred><obj>obj</obj>", query.to_xml(self._client_context))

        self.assertEqual([], query.execute(self._client_context), [])

    def test_query(self):

        query = Query(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"))

        self.assertEqual("q", query.get_xml_type())

        self.assertEqual("subj", query.subj.word)
        self.assertEqual("pred", query.pred.word)
        self.assertEqual("obj", query.obj.word)

        self.assertEqual("<q><subj>subj</subj><pred>pred</pred><obj>obj</obj></q>", query.to_xml(self._client_context))

        self.assertEqual([], query.execute(self._client_context), [])

    def test_query_no_tuples(self):
        query = MockQuery(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"), [])
        self.assertEqual([], query.execute(self._client_context, "?a ?b"))

    def test_query_one_tuple(self):
        query = MockQuery(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"), [['a', 'b', 'c']])
        self.assertEqual([[['subj', 'a'], ['pred', 'b'], ['obj', 'c']]], query.execute(self._client_context))

    def test_query_multi_tuple(self):
        query = MockQuery(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"), [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']])
        self.assertEqual([[['subj', 'a'], ['pred', 'b'], ['obj', 'c']], [['subj', 'd'], ['pred', 'e'], ['obj', 'f']], [['subj', 'g'], ['pred', 'h'], ['obj', 'i']]], query.execute(self._client_context))

    def test_notquery(self):

        query = NotQuery(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"))

        self.assertEquals("notq", query.get_xml_type())

        self.assertEqual("subj", query.subj.word)
        self.assertEqual("pred", query.pred.word)
        self.assertEqual("obj", query.obj.word)

        self.assertEqual("<notq><subj>subj</subj><pred>pred</pred><obj>obj</obj></notq>", query.to_xml(self._client_context))

        self.assertEqual([], query.execute(self._client_context), [])

    def test_notquery_no_tuples(self):
        query = MockNotQuery(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"), [])
        self.assertEqual([], query.execute(self._client_context, "?a ?b"))

    def test_notquery_one_tuple(self):
        query = MockNotQuery(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"), [['a', 'b', 'c']])
        self.assertEqual([[['subj', 'a'], ['pred', 'b'], ['obj', 'c']]], query.execute(self._client_context))

    def test_notquery_multi_tuple(self):
        query = MockNotQuery(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"), [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']])
        self.assertEqual([[['subj', 'a'], ['pred', 'b'], ['obj', 'c']], [['subj', 'd'], ['pred', 'e'], ['obj', 'f']], [['subj', 'g'], ['pred', 'h'], ['obj', 'i']]], query.execute(self._client_context))

