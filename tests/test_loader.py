import pytest
from mnp.ingestion.loader import load_endes

# Definimos las variantes globalmente para inyectarlas en todos los tests
MODULE_VARIANTS = [
    1629,           # Entero crudo
    "1629",         # String crudo
    "household"     # Alias limpio
]

RECORD_VARIANTS = [
    "rech1",               # Alias limpio
    "RECH1.sav",           # Mayúsculas con extensión
    "RECH1.SAV",           # Todo en mayúsculas
    "rech1_2024",          # Con sufijo de año
    "RECH1_2024.sav"       # Sufijo de año + extensión
]

@pytest.mark.parametrize("module_input", MODULE_VARIANTS)
@pytest.mark.parametrize("record_input", RECORD_VARIANTS)
def test_carga_datos_sintaxis(module_input, record_input):
    """Prueba la limpieza sintáctica (mayúsculas, extensiones) en un año fácil (2024)."""
    df = load_endes(year=2024, module=module_input, record=record_input)
    assert not df.empty, f"Fallo al cargar: {module_input} | {record_input}"
    assert df.shape == (135045, 36)

HISTORICAL_PAIRS = [
    (2000, 64, "rech1"),                        # Household en 2000
    (2024, 1635, "re516171"),                   # Fertility en 2024 (código crudo y registro sucio)
    (2012, 71, "re516171"),                     # Fertility en 2012 (código histórico antiguo)
    (None, "fertility_nuptiality", "rec51f")    # Máquina del tiempo con alias limpios
]

@pytest.mark.parametrize("year, module_input, record_input", HISTORICAL_PAIRS)
def test_carga_con_metadata_historica(year, module_input, record_input):
    """Prueba la obtención de la metadata (df, meta) enfrentando la resolución de nombres antiguos."""
    resultado = load_endes(year=year, module=module_input, record=record_input, meta=True)
    
    if year is None:
        assert isinstance(resultado, dict)
        assert 2012 in resultado
        df, meta = resultado[2012]
    else:
        df, meta = resultado

    assert not df.empty
    assert hasattr(meta, "column_labels") or hasattr(meta, "column_names_to_labels")

@pytest.mark.parametrize("year, module_input, _", HISTORICAL_PAIRS)
def test_carga_modulos_completos_historicos(year, module_input, _):
    """Prueba la carga masiva de carpetas omitiendo el record, resolviendo carpetas antiguas."""
    # Omitimos el record intencionalmente para forzar la carga de todo el módulo
    resultados = load_endes(year=year, module=module_input, meta=True)
    
    assert isinstance(resultados, dict)
    assert len(resultados) > 0
    
    if year is None:
        # Diccionario anidado: resultados[año][record] = (df, meta)
        assert 2012 in resultados
        primer_record = list(resultados[2012].keys())[0]
        assert isinstance(resultados[2012][primer_record], tuple)
    else:
        # Diccionario plano: resultados[record] = (df, meta)
        primer_registro = list(resultados.keys())[0]
        assert isinstance(resultados[primer_registro], tuple)

def test_llamada_vacia_protegida():
    """Valida que llamar a load_endes() sin parámetros lanza un error."""
    with pytest.raises(ValueError, match="Se requiere especificar un 'module'"):
        load_endes()

