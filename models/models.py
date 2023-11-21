from pydantic import BaseModel
from datetime import date

class Item(BaseModel):
    item_idx: int = None
    author: str = None
    created_at: str = None
    title: str = None
    contents: str = None
    replies: list[str] = []
    similar_items: list['Item'] = []

class SearchResult(BaseModel):
    total: int
    max_page: int
    current_page: int
    search_keyword: str
    result_list: list[Item]
