"""Candidature Auto : envoyer une candidature spontanée en quelques secondes.

On saisit le prénom, le nom et l'entreprise d'un recruteur. Le script déduit
son adresse mail à partir du format utilisé par l'entreprise
(ex. {prenom}.{nom}@entreprise.com), prépare un mail personnalisé et l'envoie
avec le CV en pièce jointe, après confirmation.

Les identifiants ne sont jamais écrits dans le code : ils sont lus depuis un
fichier .env local (voir .env.example).
"""

import os
import smtplib
import unicodedata
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

DOSSIER = Path(__file__).resolve().parent
load_dotenv(DOSSIER / ".env")

EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
CV_PATH = Path(os.getenv("CV_PATH", DOSSIER / "CV.pdf"))
FICHIER_ENTREPRISES = DOSSIER / "entreprises.xlsx"
FICHIER_MODELE = DOSSIER / "modele_mail.txt"

CIVILITES = {"Monsieur": "Monsieur", "Madame": "Madame"}


def normaliser(texte):
    """Minuscules, sans accents ni espaces : 'Hélène' -> 'helene', 'Le Gall' -> 'legall'."""
    texte = unicodedata.normalize("NFKD", texte.strip().lower())
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return texte.replace(" ", "").replace("'", "")


def charger_entreprises(chemin=FICHIER_ENTREPRISES):
    """Retourne un dictionnaire {nom d'entreprise normalisé: format d'adresse}."""
    df = pd.read_excel(chemin)
    return {
        normaliser(str(ligne["Entreprise"])): str(ligne["Format_email"]).strip()
        for _, ligne in df.iterrows()
    }


def generer_email(prenom, nom, entreprise, formats):
    """Construit l'adresse du recruteur, ou None si l'entreprise est inconnue.

    Formats gérés : {prenom}, {nom} et {p} (initiale du prénom).
    """
    format_email = formats.get(normaliser(entreprise))
    if not format_email:
        return None
    prenom_n, nom_n = normaliser(prenom), normaliser(nom)
    return (
        format_email.replace("{prenom}", prenom_n)
        .replace("{nom}", nom_n)
        .replace("{p}", prenom_n[:1])
    )


def rediger_message(civilite, nom, entreprise):
    """Remplit le modèle de mail. La première ligne du modèle est l'objet."""
    lignes = FICHIER_MODELE.read_text(encoding="utf-8").splitlines()
    objet = lignes[0].removeprefix("Objet :").strip()
    corps = "\n".join(lignes[1:]).strip()
    corps = corps.format(civilite=civilite, nom=nom.strip().title(), entreprise=entreprise.strip())
    return objet, corps


def envoyer(destinataire, objet, corps, cv_path=CV_PATH):
    """Envoie le mail avec le CV en pièce jointe."""
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        raise RuntimeError("Identifiants manquants : remplis le fichier .env (voir .env.example).")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinataire
    msg["Subject"] = objet
    msg.attach(MIMEText(corps, "plain", "utf-8"))

    with open(cv_path, "rb") as fichier:
        piece = MIMEBase("application", "octet-stream")
        piece.set_payload(fichier.read())
    encoders.encode_base64(piece)
    piece.add_header("Content-Disposition", "attachment", filename=Path(cv_path).name)
    msg.attach(piece)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as serveur:
        serveur.starttls()
        serveur.login(EMAIL_SENDER, EMAIL_PASSWORD)
        serveur.send_message(msg)


def lancer_interface():
    import tkinter as tk
    from tkinter import messagebox, ttk

    formats = charger_entreprises()

    root = tk.Tk()
    root.title("Candidature Auto")
    root.resizable(False, False)

    champs = {}
    for ligne, libelle in enumerate(["Prénom", "Nom", "Entreprise"]):
        tk.Label(root, text=f"{libelle} :").grid(row=ligne, column=0, padx=10, pady=5, sticky="e")
        champs[libelle] = tk.Entry(root, width=28)
        champs[libelle].grid(row=ligne, column=1, padx=10, pady=5)

    tk.Label(root, text="Civilité :").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    civilite = ttk.Combobox(root, values=list(CIVILITES), state="readonly", width=25)
    civilite.current(0)
    civilite.grid(row=3, column=1, padx=10, pady=5)

    def on_envoyer():
        prenom, nom, entreprise = (champs[c].get().strip() for c in ["Prénom", "Nom", "Entreprise"])
        if not (prenom and nom and entreprise):
            messagebox.showwarning("Champs manquants", "Remplis le prénom, le nom et l'entreprise.")
            return

        destinataire = generer_email(prenom, nom, entreprise, formats)
        if not destinataire:
            messagebox.showwarning(
                "Entreprise inconnue",
                f"{entreprise} n'est pas dans entreprises.xlsx. Ajoute son format d'adresse puis réessaie.",
            )
            return

        objet, corps = rediger_message(CIVILITES[civilite.get()], nom, entreprise)
        if not messagebox.askyesno(
            "Confirmer l'envoi",
            f"Destinataire : {destinataire}\nObjet : {objet}\n\n{corps}\n\nEnvoyer ce mail ?",
        ):
            return

        try:
            envoyer(destinataire, objet, corps)
        except Exception as erreur:
            messagebox.showerror("Échec de l'envoi", str(erreur))
            return
        messagebox.showinfo("Envoyé", f"Candidature envoyée à {destinataire}")
        for champ in champs.values():
            champ.delete(0, tk.END)

    tk.Button(root, text="Envoyer la candidature", command=on_envoyer).grid(
        row=4, column=0, columnspan=2, pady=10
    )
    root.mainloop()


if __name__ == "__main__":
    lancer_interface()
