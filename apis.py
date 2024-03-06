# def add_documents()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Item, SearchResult

from es import es

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return "Welcome to FastAPI!"


@app.get("/total")
def get_total_count():
    return {"total": es.get_total_count()}


# 1. 메인 - 랜덤글 20개
@app.get("/main", response_model=list[Item])
async def get_main():
    return es.get_random_contents_by_20()


# # TODO 2. 메인 - 추천글 10개 factorization machine
# @app.get("/recom", response_model=list[Item])
# async def get_recommended_contents ():
#     return []


# 3. 서브 - 인덱스로 글 정보 가져오기
@app.get("/sub", response_model=Item)
async def get_sub(index: int):
    return es.get_content_by_index(index)


# 4. 서브 - 유사한 글 5개 리스팅
@app.get("/similar")
async def get_similar_contents(index: int):
    return es.get_similar_contents(index)


# 5. 검색 결과 화면
@app.get("/search", response_model=SearchResult)
async def get_search_result(query: str, page: int = 1):
    return es.search_content_by_keyword(query, page)

@app.get("/test")
async def get_test(index: int):
    # return es.get_contents_by_index_list([541956, 359414, 60727, 326673, 31458, 26148, 11629, 10412])
    # return es.get_mappings()
    return es.get_vector_by_index(index)

@app.get("/all")
async def get_all_docs():
    return len(es.get_preprocessed_contents())