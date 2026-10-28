import pytest

from app.utils.logger import AZUL, NARANJA, RESET, ROJO, VERDE, AppLogger


@pytest.mark.parametrize(
    "metodo, nivel, color",
    [
        ("ok", "OK", VERDE),
        ("info", "INFO", AZUL),
        ("warning", "WARNING", NARANJA),
        ("error", "ERROR", ROJO),
    ],
)
def test_cada_metodo_imprime_nivel_color_y_mensaje(capsys, metodo, nivel, color):
    log = AppLogger("test")

    getattr(log, metodo)("hola")

    salida = capsys.readouterr().out
    assert salida.startswith(color)
    assert f"[{nivel}] test: hola" in salida
    assert salida.strip().endswith(RESET)
