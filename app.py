from flask import Flask, render_template, request, redirect, url_for,flash
import base
import chiffrement
from Crypto.PublicKey import RSA
# from Crypto.PublicKey import pkcs1_OAEP

# Générer une paire de clés RSA avec une longueur de clé de 2048 bits
key = RSA.generate(2048)

# # Exporter les clés privée et publique au format PEM
private_key_pem = key.export_key().decode('utf-8')
public_key_pem = key.public_key().export_key().decode('utf-8')

# # Importer la clé publique au format PEM
public_key = RSA.import_key(public_key_pem.encode('utf-8'))

# # # Importer la clé privée au format PEM
private_key = RSA.import_key(private_key_pem.encode('utf-8'))

def chiffrer_mot_de_passe(mot_de_passe, public_key):
  # Convertir le mot_de_passe en binaire
  mot_de_passe = mot_de_passe.encode('utf-8')
  # Chiffrer le mot_de_passe binaire avec la clé publique RSA
  chiffre = public_key.encrypt(mot_de_passe, RSA.pkcs1_OAEP)
  return chiffre

# def dechiffrer_mot_de_passe(chiffre, private_key):
#   # Déchiffrer le mot de passe chiffré avec RSA et OAEP
#   mot_de_passe_bytes = private_key.decrypt(chiffre, RSA.pkcs1_OAEP)
#   # Convertir le mot de passe binaire en chaîne
#   mot_de_passe = mot_de_passe_bytes.decode('utf-8')
#   # Renvoyer le mot de passe déchiffré
#   return mot_de_passe

# deuximeme methode!

# key = RSA.generate(1024)
# private_key = key.export_key()
# print("Private key: ",private_key)

# public_key = key.publickey().export_key()
# print("Public key: ",public_key)

app = Flask(__name__)


@app.route('/')
# =========Page d'accueil principale===============
def accueil():
    return render_template("accueil.html", accueil =True)

# ===============Utilisateur==============
@app.route('/ajouter_utilisateur', methods=['GET', 'POST'])
def ajouter_utilisateur():
    if(request.method == "POST"):
        # Récupérer les données du formulaire et les traiter
        data  =  request.form
        nom = data.get('nom')
        type_compte = data.get('type_compte')
        mot_de_passe = data.get('mot_de_passe')
        
        # mot_de_passe_chiffer = chiffrer_mot_de_passe(mot_de_passe, public_key)
        
        mot_de_passe_chiffer = chiffrement.rsa(mot_de_passe,33,3)
        
        db=base.connecter()
        sql_ins = "INSERT INTO utilisateurs(nom,type_compte,mot_de_passe) VALUES(%s,%s, %s)"
        valeurs =(nom,type_compte,mot_de_passe_chiffer,)
       # Creaction un objet curseur
        cur = db.cursor()
        cur.execute(sql_ins, valeurs)
        db.commit()
        cur.close()
        # message = f"Utilisateur ajouté : {0}"
    return render_template('ajouter_utilisateur.html')
        # return redirect(url_for('accueil'))

# =============ajouter client============
@app.route('/ajouter_client', methods=['GET', 'POST'])
def ajouter_client():
    if(request.method == "POST"):   
    # Récupérer les données du formulaire
        data  =  request.form
        numero_telephone = data.get('numero_telephone')
        nom = data.get('nom')
        age = int(data.get('age'))
        pays = data.get('pays')
        ville = data.get('ville')
        email = data.get('email')
        # il faut se connecter au bc pour enregister les donnees
        db=base.connecter()
        sql_ins = "INSERT INTO clients(numero_telephone, nom, age, pays, ville, email) VALUES(%s, %s, %s, %s, %s, %s)"
        valeurs =(numero_telephone,nom, age, pays, ville, email,)
        cur = db.cursor()
        cur.execute(sql_ins, valeurs)
        db.commit()
        cur.close()
        # return 'Client ajouté avec succès!'
    return render_template('ajouter_client.html')

# ============ajouter un compte=========
@app.route('/ajouter-compte', methods=['GET', 'POST'])
def ajouter_compte():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        id = request.form['id']
        num_compte = request.form['num_compte']
        id_client = request.form['id_client']
        solde = float(request.form['solde'])

    return render_template('ajouter-compte.html')  # Afficher le template HTM


@app.route('/depot_sur_compte', methods=['GET', 'POST'])
def depot_sur_compte():
  if request.method == 'POST':
    numero_compte = request.form['numero_compte']
    montant = float(request.form['montant'])

    # Connexion à la base de données
    db=base.connecter()
    cursor = db.cursor()
    # Vérifier si le numéro de compte existe
    sql = "SELECT solde FROM comptes_clients WHERE numero_compte = %s"
    cursor.execute(sql, (numero_compte,))
    compte = cursor.fetchone()

    if compte is None:
      flash('Le numéro de compte saisi est introuvable.', 'error')
      db.close()
      return render_template('depot_sur_compte.html')

    # Mettre à jour le solde du compte
    nouveau_solde = compte[2] + montant
    sql = "UPDATE comptes_clients SET solde = %s WHERE numero_compte = %s"
    cursor.execute(sql, (nouveau_solde, numero_compte))
    db.commit()

    flash(f"Dépôt de {montant:.2f}€ effectué avec succès sur le compte {numero_compte}.", 'success')
    db.close()

  return render_template('depot_sur_compte.html')

        
if __name__ == '__main__':
    app.run(debug=True)
   
