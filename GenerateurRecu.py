from flask import Flask, request, render_template_string
from datetime import datetime
import os

app = Flask(__name__)

# Modèle HTML/CSS pour l'interface utilisateur
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Générateur de Reçus de Caisse</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; margin: 30px; text-align: center; }
        .container { max-width: 600px; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: inline-block; text-align: left; }
        h2 { color: #333; text-align: center; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        label { font-weight: bold; display: block; margin-bottom: 5px; color: #555; }
        input[type="text"], input[type="number"] { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
        .row { display: flex; gap: 10px; }
        button { width: 100%; padding: 12px; font-size: 16px; background-color: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; margin-top: 10px; }
        button:hover { background-color: #218838; }
        .receipt-box { background: #fee; border-left: 4px solid #dc3545; padding: 15px; font-family: monospace; white-space: pre-wrap; background-color: #fdfdfd; border: 1px dashed #777; margin-top: 25px; border-radius: 4px; }
        .success-alert { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 6px; margin-bottom: 15px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🧾 Générateur de Reçus Professionnels</h2>
        
        {% if message %}
            <div class="success-alert">{{ message }}</div>
        {% endif %}

        <form method="POST">
            <div class="form-group">
                <label>Nom du Client :</label>
                <input type="text" name="client" placeholder="Ex: Client Comptant" value="{{ client_name }}">
            </div>
            
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="font-weight: bold; color: #0056b3;">🛒 Ajouter un article :</p>
            
            <div class="form-group">
                <label>Désignation du produit :</label>
                <input type="text" name="article" placeholder="Ex: Sac à dos Sacoche" required>
            </div>
            
            <div class="row">
                <div class="form-group" style="flex: 1;">
                    <label>Prix Unitaire ($) :</label>
                    <input type="number" name="prix" step="0.01" min="0" placeholder="0.00" required>
                </div>
                <div class="form-group" style="flex: 1;">
                    <label>Quantité :</label>
                    <input type="number" name="qte" min="1" value="1" required>
                </div>
            </div>
            
            <button type="submit">Générer et Enregistrer le Reçu</button>
        </form>

        {% if receipt_content %}
            <h3>📄 Aperçu du reçu généré :</h3>
            <div class="receipt-box">{{ receipt_content }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    receipt_content = ""
    client_name = "Client Comptant"

    if request.method == "POST":
        client_name = request.form.get("client").strip() or "Client Comptant"
        article = request.form.get("article").strip()
        try:
            prix = float(request.form.get("prix", 0))
            qte = int(request.form.get("qte", 1))
            total_item = prix * qte
        except ValueError:
            return render_template_string(HTML_TEMPLATE, message="Erreur de saisie dans les montants.", client_name=client_name)

        # Création du texte au format ticket de caisse
        date_file = datetime.now().strftime("%Y%m%d_%H%M%S")
        date_display = datetime.now().strftime("%Y-%m-%d %H:%M")
        filename = f"recu_{date_file}.txt"
        
        lines = []
        lines.append("========================================")
        lines.append("             BOUTIQUE EN LIGNE          ")
        lines.append(f" Date : {date_display}")
        lines.append(f" Client : {client_name}")
        lines.append("========================================")
        lines.append(f"{'Article':<18} {'Qté':<5} {'P.U.':<8} {'Total':<8}")
        lines.append("----------------------------------------")
        lines.append(f"{article[:17]:<18} {qte:<5} {prix:<8.2f} {total_item:<8.2f}")
        lines.append("----------------------------------------")
        lines.append(f"TOTAL À PAYER :                {total_item:.2f} $")
        lines.append("========================================")
        lines.append("        Merci pour votre confiance !    ")
        
        receipt_content = "\n".join(lines)
        
        # Sauvegarde du fichier texte sur le serveur EC2
        with open(filename, "w", encoding="utf-8") as f:
            f.write(receipt_content)
            
        message = f"✅ Reçu enregistré avec succès sous le nom '{filename}' !"

    return render_template_string(HTML_TEMPLATE, message=message, receipt_content=receipt_content, client_name=client_name)

if __name__ == "__main__":
    # Changement de port à 5001 pour ne pas entrer en conflit avec le premier script
    app.run(host="0.0.0.0", port=5001)
    