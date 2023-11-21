# def add_documents()
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from models.models import Item, SearchResult

from es import EsModule

# def
app = FastAPI()
es = EsModule()

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
def get_main():
    return es.get_random_contents_by_20()


# TODO 2. 메인 - 추천글 10개
@app.get("/recom", response_model=list[Item])
def get_recommended_contents ():
    return []


# 3. 서브 - 인덱스로 글 정보 가져오기
@app.get("/sub", response_model=Item)
def get_sub(index: int):
    return es.get_content_by_index(index)


# TODO 4. 서브 - 유사한 글 5개 리스팅
@app.get("/similar", response_model=list[Item])
def get_similar_contents(index: int):
    return []


# 5. 검색 결과 화면
@app.get("/search", response_model=SearchResult)
def get_search_result(query: str, page: int = 1):
    return es.search_content_by_keyword(query, page)
