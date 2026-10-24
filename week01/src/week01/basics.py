"""Day 2: five everyday C# utilities rewritten in idiomatic Python."""
import re
from collections import Counter
from datetime import date, timedelta


#1 string helper --c# static strign slugify (string title )
def slugify(titile:str) ->str:
    """Hello world 2026' -> 'hello-world-2026'. """
    words=re.findall(r"[a-z0-9]+",titile.lower())
    return "-".join(words)

# 2. Parsing -- C#: int.TryParse(text, out var value) ? value : null
def try_parse_int(text:str | None) ->int | None:
    """Return the int or None when the text is not whole number."""
    if not text:
        return None

    # 3. Date helper -- C#: count weekdays between two DateTimes
def business_day_between (start:date ,end :date) -> int :
    """weekdays from start (inclusive) to end (Exclusive). """
    total_days=(end - start).days
    return sum(
        1
        for offset in range(total_days)
        if(start+timedelta(days=offset)).weekday() < 5
    )

# 4. LINQ -- C#: items.Chunk(size).ToList()

def chunk(items:list,size:int)->list[list]:
    """[1,2,3,4,5],2 -> [[1.2],[3,4],[5]]."""
    if size<1:
        raise ValueError(f"size must be >=1, got {size}")
    return [items[i:i+size] for i in range (0,len(items),size)]

# 5. LINQ -- C#: words.GroupBy(w => w).OrderByDescending(g => g.Count()).Take(n)

def top_words(text:str ,n:int=3) ->list[tuple[str,int]]:
    """Most frequent words ,case -insensitive ,as (word,count)  pairs"""
    words=re.findall(r"[a-z']+",text.lower())
    return Counter(words).most_common(n)

if __name__ == "__main__":
    print(f"{slugify('Day 2: Python Syntax vs C#!')=}")
    print(f"{try_parse_int(' 42 ')=}, {try_parse_int('4.2')=}")
    print(f"{business_day_between(date(2026, 10, 19), date(2026, 10, 26))=}")
    print(f"{chunk(list(range(7)), 3)=}")
    print(f"{top_words('the cat and the hat and the bat')=}")