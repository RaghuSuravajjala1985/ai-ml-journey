from datetime import date
import pytest
from week01.basics import business_day_between,chunk,slugify,top_words,try_parse_int

@pytest.mark.parametrize(
    ("title","expected"),
    [
        ("Hello World!" ,"hello-world"),
        ("Day 2: python vs C# ","day-2-python-vs-c"),
        ("","")
    ],
)
def test_slugify(title,expected):
    assert slugify(title)== expected

def test_try_parse_int():
    assert try_parse_int('42') == 42
    assert try_parse_int(" -7 ") == -7
    assert try_parse_int("4.2") is None
    assert try_parse_int("") is None
    assert try_parse_int(None) is None 

def test_business_days_full_week():
    assert business_day_between(date(2026,10,19), date(2026,10,26)) == 5

def test_business_days_weekends_only():
    assert business_day_between(date(2026,10,24), date(2026,10,26)) == 0

def test_chunk():
    assert chunk([1,2,3,4,5],2) == [[1,2],[3,4],[5]]
    assert chunk([],3) == []

def test_top_words():
    assert top_words("The cat and THE hat and the bat",2) ==[("the",3),("and",2)]



