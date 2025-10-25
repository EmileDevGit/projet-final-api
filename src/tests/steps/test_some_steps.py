import requests
from pytest_bdd import scenarios, given, then, when, parsers

scenarios("../features/some.feature")

BASE_URL = ""

@given(parsers.parse("un contexte explicite"))
def placeholder():
    assert True

@when(parsers.parse("je fais une action spécifique"))
def action():
    pass

@then(parsers.parse("je recoit un résultat X"))
def resultat():
    assert True
