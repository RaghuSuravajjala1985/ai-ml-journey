"""" Day 3- functions :parameters kinds,*args/**kwargs, closures , functions as values."""
from collections.abc import Callable

def describe(name:str ,/, role:str="engineer" ,*,years:int =0) -> str:
    """ name is positional-only ,role is noramal ,years is keywords only . """

    return f"{name} ({role} , {years} yrs)"

def total(*amounts:float ,currency:str ="USD") -> str  :
    """*amounts behaves like C# 'params double[] amounts' ."""
    return f"{sum(amounts):,.2f} {currency}"

def build_connection_string(server:str,database:str,**options:str) ->str:
    """" **options is an open-ended options bag ,like distionary<string ,string> ."""
    parts=[f"Server={server}", f"Database={database}"]
    parts+=[f"{key}={value}" for key, value in options.items()]
    return ";" .join(parts) +";"

def add_item(item :str,bucket :list[str] | None =None) -> list[str]:
    """"Correct idioms for mutable defaults : use None ,then create a new list ."""
    if bucket is None :
        bucket=[]
    bucket.append(item)
    return bucket

def make_multiplier(facator :float) -> Callable[[float],float]:
    """"returs a closure ,like returning a Func<double,double> that captures factors."""
    def multiply(x:float) -> float :
        return x*facator
   
    return multiply

def apply_all(value:float, *funcs: Callable[[float],float]) -> float:
    """"Functions are values : pass them around like delegates."""
    for func in funcs:
        value =func(value)
    return value

if __name__ == "__main__":
   print(describe("Raghu", "architect", years=13))
   print(total(19.99, 5.01, 75))
   config = {"Encrypt": "True", "Timeout": "30"}
   print(build_connection_string("sql01", "orders", **config))  # dict unpacking
   print(add_item("a"), add_item("b"))  # ['a'] ['b'] - no shared state
   double, triple = make_multiplier(2), make_multiplier(3)
   print(apply_all(5, double, triple, lambda x: x + 1))  # ((5*2)*3)+1 = 31
   names = ["Zoe", "adam", "Bob"]
   print(sorted(names, key=str.lower))  # like OrderBy(n => n.ToLower())