# coding:utf-8

from pyes.es import ES
from pyes.query import *
from pyes.filters import *
from werkzeug.local import LocalProxy
from flask import current_app

import settings


_logger = LocalProxy(lambda: current_app.logger)


def _get_conn(*args, **kwargs):
    _conn = ES(settings.es_hosts, *args, **kwargs)
    _conn.default_indices = settings.es_index
    return _conn


class ESClient(object):
    _connection = None

    def __init__(self, *args, **kwargs):
        self._connection = _get_conn(timeout=settings.es_timeout)

    def get_suggestion(self, input_text, size=10):
        suggestions = self._connection.suggest(settings.es_index, input_text, 'suggest_field', type='completion',
                                               size=size)
        return [item[2] for item in suggestions]

    def search_artifact(self, keyword, start=0, size=10):
        if keyword:
            keyword_reverse = keyword[::-1]
            artifact_name_filter = PrefixFilter("name", keyword)
            artifact_name_reverse_filter = PrefixFilter("name.reverse", keyword_reverse)
            artifact_terms_filter = PrefixFilter("terms", keyword)
            artifact_terms_reverse_filter = PrefixFilter("terms.reverse", keyword_reverse)
            topic_name_filter = HasParentFilter("topic", PrefixFilter("name", keyword))
            topic_name_reverse_filter = HasParentFilter("topic", PrefixFilter("name.reverse", keyword_reverse))
            topic_terms_filter = HasParentFilter("topic", PrefixFilter("terms", keyword))
            topic_terms_reverse_filter = HasParentFilter("topic", PrefixFilter("terms.reverse", keyword_reverse))
            filters = [
                artifact_name_filter,
                artifact_name_reverse_filter,
                artifact_terms_filter,
                artifact_terms_reverse_filter,
                topic_name_filter,
                topic_name_reverse_filter,
                topic_terms_filter,
                topic_terms_reverse_filter
            ]
            _query = FilteredQuery(MatchAllQuery(), ORFilter(filters, _cache=True))
        else:
            _query = MatchAllQuery()

        _search = Search(query=_query, fields=['id'], start=start, size=size, sort=[{'created_at': {'order': 'desc'}}])
        _result_set = self._connection.search(_search, doc_types='artifact')
        return _result_set.total, [doc['id'][0] for doc in _result_set]

    def search_user(self, keyword, start=0, size=10):
        if keyword:
            fullname_match = PrefixFilter("fullname", keyword)
            fullname_reverse_match = PrefixFilter("fullname.reverse", keyword[::-1])
            _query = FilteredQuery(MatchAllQuery(), ORFilter([fullname_match, fullname_reverse_match], _cache=True))
        else:
            _query = MatchAllQuery()
        _search = Search(query=_query, fields=['id'], start=start, size=size,
                         sort=[{'registered_at': {'order': 'desc'}}])
        _result_set = self._connection.search(_search, doc_types='user')
        return _result_set.total, [doc['id'][0] for doc in _result_set]

    def list_firstpage_artifact(self, start=0, size=10):
        honor_count_filter = RawFilter(dict(range={"honor_count": {"gt": 0}}))
        _search = Search(query=FilteredQuery(MatchAllQuery(), honor_count_filter), fields=['id'],
                         start=start, size=size, sort=[{'created_at': {'order': 'desc'}}])
        _result_set = self._connection.search(_search, doc_types='artifact')
        return _result_set.total, [doc['id'][0] for doc in _result_set]

    def search_topic(self, keyword, user_id=None, status=-1, start=0, size=10):
        topic_id_filter = RawFilter(dict(range={"id": {"gt": 0}}))
        filters = []
        if keyword:
            topic_name_match = PrefixFilter("name", keyword)
            terms_match = PrefixFilter("terms",keyword)
            filters.append(ORFilter([topic_name_match, terms_match]))

        if user_id:
            filters.append(TermFilter("user_id", user_id))
        elif status != -1:
            filters.append(TermFilter("status", status))

        if filters:
            filters.append(topic_id_filter)
            _query = FilteredQuery(MatchAllQuery(), ANDFilter(filters))
        else:
            _query = FilteredQuery(MatchAllQuery(), topic_id_filter)

        _search = Search(query=_query, fields=['id'], start=start, size=size,
                         sort=[{'created_at': {'order': 'desc'}}])
        _result_set = self._connection.search(_search, doc_types='topic')
        return _result_set.total, [doc['id'][0] for doc in _result_set]


    def search_artifact_by(self, artifact_name=None, term=None, start=0, size=10):
        if term:
            terms_match = PrefixFilter("terms", term)
            terms_reverse_match = PrefixFilter("terms.reverse", term[::-1])
            _query = FilteredQuery(MatchAllQuery(), ORFilter([terms_match, terms_reverse_match]))
        elif artifact_name:
            artifact_name_match = PrefixFilter("name", artifact_name)
            artifact_name_reverse_match = PrefixFilter("name.reverse", artifact_name[::-1])
            _query = FilteredQuery(MatchAllQuery(), ORFilter([artifact_name_match, artifact_name_reverse_match]))
        else:
            _query = MatchAllQuery()

        _search = Search(query=_query, fields=['id'], start=start, size=size,
                         sort=[{'created_at': {'order': 'desc'}}])
        _result_set = self._connection.search(_search, doc_types='artifact')
        return _result_set.total, [doc['id'][0] for doc in _result_set]

    def search_comment(self, user_name=None, artifact_name=None, content=None, start=0, size=10):
        if user_name:
            user_name_match = PrefixFilter("user_name", user_name)
            user_name_reverse_match = PrefixFilter("user_name.reverse", user_name[::-1])
            _query = FilteredQuery(MatchAllQuery(), ORFilter([user_name_match, user_name_reverse_match], _cache=True))
        elif artifact_name:
            artifact_name_filter = PrefixFilter("artifact_name", artifact_name)
            artifact_name_reverse_filter = PrefixFilter("artifact_name.reverse", artifact_name[::-1])
            _query = FilteredQuery(MatchAllQuery(),
                                   ORFilter([artifact_name_filter, artifact_name_reverse_filter], _cache=True))

        elif content:
            content_filter = QueryFilter(QueryStringQuery(content, search_fields="content"))
            _query = FilteredQuery(MatchAllQuery(), content_filter)
        else:
            _query = MatchAllQuery()
        _search = Search(query=_query, fields=['id'], start=start, size=size,
                         sort=[{'commented_at': {'order': 'desc'}}])
        _result_set = self._connection.search(_search, doc_types='comment')
        return _result_set.total, [doc['id'][0] for doc in _result_set]


    def index_doc(self, doc_type, doc_id, doc, **kwargs):
        parent = kwargs.pop('parent_id', None)
        try:
            self._connection.index(doc, settings.es_index, doc_type,id=doc_id ,parent=parent)
        except Exception, e:
            _logger.exception(e)


    def delete_doc(self, doc_type, doc_id):
        try:
            self._connection.delete(settings.es_index, doc_type, doc_id)
        except Exception, e:
            _logger.exception(e)


es_client = ESClient()

