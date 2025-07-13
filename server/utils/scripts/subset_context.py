# server/utils/subset_context.py
_BASEDATA = "server/utils/dataset"
_BASEHIST = "C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils"
_HIST  = "C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/histogramas"

_DEFAULT_DATASET = f"{_BASEDATA}/spotify_songs.csv"
_DEFAULT_HIST    = f"{_BASEHIST }/histogramas_acusticos.json"

_current_N: int | None = None          # ← 10, 100, 500…  o None para

def switch_subset(n: int | None):
    """Pasa a usar el subconjunto 'n'. Usa None para restaurar el dataset completo."""
    global _current_N
    _current_N = n

def dataset_path()  -> str:
    if _current_N is None:
        return _DEFAULT_DATASET
    return f"{_BASEDATA}/spotify_songs_{_current_N}.csv"

def histogram_path() -> str:
    if _current_N is None:
        return _DEFAULT_HIST
    return f"{_HIST}/hists_{_current_N}.json"
