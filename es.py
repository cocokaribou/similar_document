from elasticsearch import Elasticsearch
from config import HOST, PORT, USER, PW, INDEX

from math import ceil

PAGING_OFFSET = 10

class EsModule:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.es = Elasticsearch(
            hosts=[{'host': HOST, 'port': PORT, 'scheme': "https"}],
            request_timeout=300, max_retries=10, retry_on_timeout=True,
            basic_auth=(USER, PW)
        )

    # 인덱스의 전체 레코드 개수 가져오기
    def get_total_count(self):
        result = self.es.count(index=INDEX)
        return result['count']


    # 인덱스의 매핑 가져오기
    def get_mappings(self):
        result = self.es.indices.get_mapping(index=INDEX)
        return result


    # 글 20개 랜덤하게 가져오기
    def get_random_contents_by_20(self):
        query_dsl = {
            "function_score": {
                "query": {"match_all": {}},
                "functions": [
                    {"random_score": {}}
                ],
                "score_mode": "sum"
            }
        }

        result = self.es.search(index=INDEX, query=query_dsl, size=20)

        result_list = []
        for hit in result['hits']['hits']:
            source = hit['_source']
            result_map = {
                "item_idx": source['item_idx'],
                "title": source['subject'],
                "author": source['author_nick'],
                "created_at": source['created_at']
            }
            result_list.append(result_map)

        return result_list


    # 글 번호로 글 내용 가져오기
    def get_content_by_index(self, index: int):
        query_dsl = {
            "term": {
                "item_idx": index
            }
        }
        result = self.es.search(index=INDEX, query=query_dsl)

        # 존재하지 않는 글
        if not result['took']:
            return {}

        source = result['hits']['hits'][0]['_source']

        return {
            "item_idx": source.get('item_idx'),
            "author": source.get('author_nick'),
            "title": source.get('subject'),
            "contents": source.get('contents'),
            "replies": source.get('replies', []),
            "created_at": source.get('created_at'),
        }


    # 여러개 글 한꺼번에 가져오기
    def get_contents_by_index_list(self, indexes: list[int]):
        query_dsl = {
            "terms": {
                "item_idx": indexes
            }
        }
        result = self.es.search(index=INDEX, query=query_dsl)

        # 존재하지 않는 글
        if not result['took']:
            return {}

        matching_documents = result['hits']['hits']

        # TODO 입력된 인덱스 순서대로 출력
        return [{
            "item_idx": doc['_source']['item_idx'], 
            "author": doc['_source']['author_nick'],
            "title" : doc['_source']['subject'],
            "contents": doc['_source']['contents']
            } for doc in matching_documents]
    

    # 유사한 글 가져오기
    def get_similar_contents(self, index: int):
        return {}
        
    # 글 벡터 가져오기
    def get_vector_by_index(self, index: int):
        print(f"what! {index}")
        query_dsl = {
            "term": {
                "item_idx": index
            }
        }
        result = self.es.search(index=INDEX, query=query_dsl)

        # 존재하지 않는 글
        if not result['took']:
            return {}

        source = result['hits']['hits'][0]['_source']['d2v_vector']

        return source

    # 벡터로 cos_similarity 검색하기
    def cos_similarity(self, vector):
        return {}


    # 키워드 검색결과 가져오기, 10개씩 paging
    def search_content_by_keyword(self, keyword: str, page: int):
        start = 0
        if page != 1:
            start = (page - 1) * PAGING_OFFSET

        search_query = {
            "from": start,
            "size": PAGING_OFFSET,
            "query": {
                "term": {
                    "contents": keyword
                }
            },
            "sort": [
                {
                    "item_idx": {
                        "order": "desc"
                    }
                }
            ]
        }

        result = self.es.search(index=INDEX, body=search_query)

        total = result['hits']['total']['value']
        max_page = 1
        if total > 10:
            max_page = ceil(total / 10)

        result_list = []
        for hit in result['hits']['hits']:
            result_map = {
                "item_idx": hit['_source']['item_idx'],
                "title": hit['_source']['subject'],
            }
            result_list.append(result_map)

        return {
            "total": total,
            "max_page": max_page,
            "current_page": page,
            "search_keyword": keyword,
            "result_list": result_list
        }

es = EsModule()