from candidature_auto import charger_entreprises, generer_email, normaliser, rediger_message

FORMATS = charger_entreprises()


def test_normaliser():
    assert normaliser("  Hélène ") == "helene"
    assert normaliser("Le Gall") == "legall"


def test_format_prenom_nom():
    assert generer_email("Marie", "Dupont", "AXA", FORMATS) == "marie.dupont@axa.com"


def test_casse_et_accents():
    assert generer_email("Éric", "Lefèvre", "  axa ", FORMATS) == "eric.lefevre@axa.com"


def test_format_initiale():
    entreprise, fmt = next((e, f) for e, f in FORMATS.items() if "{p}" in f)
    adresse = generer_email("Marie", "Dupont", entreprise, FORMATS)
    assert "{" not in adresse and adresse.startswith("m")


def test_entreprise_inconnue():
    assert generer_email("Marie", "Dupont", "Entreprise Fictive", FORMATS) is None


def test_message():
    objet, corps = rediger_message("Madame", "dupont", "AXA")
    assert objet == "Data et IA chez AXA : 15 minutes d'échange ?"
    assert corps.startswith("Bonjour Madame Dupont,")
    assert "ce que fait AXA" in corps
