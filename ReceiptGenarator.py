from datetime import datetime

def generer_facture():
    print("=== CRÉATEUR DE REÇU DE CAISSE ===")
    nom_client = input("Nom du client (optionnel) : ").strip() or "Client Comptant"
    articles = []

    while True:
        nom_article = input("Nom de l'article (ou tapez 'fin' pour terminer) : ").strip()
        if nom_article.lower() == 'fin':
            break
        if not nom_article:
            continue
        try:
            prix = float(input(f"Prix unitaire de '{nom_article}' : $"))
            qte = int(input(f"Quantité : "))
            articles.append({"nom": nom_article, "prix": prix, "qte": qte, "total": prix * qte})
        except ValueError:
            print("Données invalides. Réessayez cet article.")

    if not articles:
        print("Aucun article saisi. Annulation.")
        return

    # Génération du texte de la facture
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nom_fichier = f"recu_{date_str}.txt"
    
    total_general = sum(item["total"] for item in articles)

    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write("========================================\n")
        f.write("             BOUTIQUE EN LIGNE          \n")
        f.write(f" Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f" Client : {nom_client}\n")
        f.write("========================================\n")
        f.write(f"{'Article':<18} {'Qté':<5} {'P.U.':<8} {'Total':<8}\n")
        f.write("----------------------------------------\n")
        for item in articles:
            f.write(f"{item['nom'][:17]:<18} {item['qte']:<5} {item['prix']:<8.2f} {item['total']:<8.2f}\n")
        f.write("----------------------------------------\n")
        f.write(f"TOTAL À PAYER :                {total_general:.2f} $\n")
        f.write("========================================\n")
        f.write("        Merci pour votre confiance !    \n")

    print(f"\n✅ Le reçu a été généré avec succès sous le nom : {nom_fichier}")

if __name__ == "__main__":
    generer_facture()
    