import pytest
from dataclasses import FrozenInstanceError

from week01.decorators   import TOOLS,count_calls,retry,slow_square
from week01.functions  import add_item,build_connection_string,describe,make_multiplier,total
from week01.models import  BankAccount,ExperimentRun,Money,SavingsAccount,SmsGateway,broadcast


def test_keyword_only_parameter_must_be_named():
    assert describe("Raghu", years=13) =="Raghu (engineer , 13 yrs)"
    with pytest.raises(TypeError):
        describe("Raghu","architect",13)

def test_args_and_kwargs():
    assert total(1, 2 , 3.5)=="6.50 USD"
    assert build_connection_string("s","d",Encrypt="True") =="Server=s;Database=d;Encrypt=True;"

def test_no_shared_mutable_default():
    assert add_item("a") ==["a"]
    assert add_item("b") == ["b"]

def test_closure_captures_factor():
    assert make_multiplier(3)(4) == 12

def test_bank_account_rules():
    acct = BankAccount("Raghu",100)
    acct.deposit(100)
    assert acct.balance == 200
    with pytest.raises(ValueError):
        acct.withdraw(1_000)
    with pytest.raises(AttributeError):
        acct.balance=0

def test_subclass_override_and_super():
    saving=SavingsAccount("Raghu",5_000)
    with pytest.raises(ValueError,match="limited"):
        saving.withdraw(2_000)
    saving.withdraw(500)
    assert saving.balance == 4_500

def test_protlcal_accepts_unrelated_class():
    assert broadcast(SmsGateway(), ["1"], "hi" ==["sms to 1: hi"] )

def test_money_is_a_value_object():
    assert Money(10)  == Money(10.0, "USD")
    assert Money(10) + Money(5)  == Money (15)
    with pytest.raises(FrozenInstanceError):
        Money(10).amount =20
    with pytest.raises(ValueError):
        Money(-1)

def test_experiment_runs_not_to_share_list():
    a , b = ExperimentRun(name="a") ,ExperimentRun(name="b")
    a.tags.append("x")
    assert b.tags  == []

def test_decorators_preserve_metadata_add_resgister():
    assert slow_square.__name__ == "slow_square" 
    assert "slow_square" in TOOLS

def test_count_calls():
    @count_calls
    def noop():
        return None

    noop()
    noop()
    assert noop.calls == 2

def test_retry_gives_up_after_n_aatempts():
    attempts = [] 

    @retry(times=2, delay=0)
    def always_fails():
        attempts.append(1)
        raise RuntimeError("boom")
    
    with pytest.raises(RuntimeError):
        always_fails()
        assert len(attempts) ==2

