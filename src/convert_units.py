from unidecode import unidecode #remove non ascii characters

_PINCEE_PAR_UNITE = {
    "pincee": 1.0,
    "soufle": 1.4286,
    "nuage": 1.4286 * 5,
    "poignee": 1.4286 * 5 * 3,
    "once": 1.4286 * 5 * 3 * 2,
}



def _normalize(text: str) -> str:
    return unidecode(text.strip().lower())


def convert_to_pincee(quantity: float, unit: str) -> float:
    normalized_unit = _normalize(unit)

    if normalized_unit not in _PINCEE_PAR_UNITE:
        supported_units = ", ".join(_PINCEE_PAR_UNITE)
        raise ValueError(
            f"Unite inconnue : {unit!r}. Unites acceptees : {supported_units}."
        )

    return quantity * _PINCEE_PAR_UNITE[normalized_unit]