import pytest

from app.especificacion import evaluar, validar_limites


@pytest.mark.parametrize(
    "valor,minimo,maximo,esperado",
    [
        (7.0, 6.5, 8.5, True),
        (6.5, 6.5, 8.5, True),  # límite inclusivo
        (8.6, 6.5, 8.5, False),
        (6.4, 6.5, 8.5, False),
        (3.0, None, 5.0, True),  # solo máximo
        (9.0, None, 5.0, False),
        (1.0, 2.0, None, False),  # solo mínimo
        (10.0, None, None, True),
    ],
)
def test_evaluar(valor, minimo, maximo, esperado):
    assert evaluar(valor, minimo, maximo) is esperado


def test_limites_invertidos():
    with pytest.raises(ValueError):
        validar_limites(10, 5)
