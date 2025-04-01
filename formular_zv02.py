from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(dbname="formular_zv02", user="postgres", password="postgre", host="localhost")
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)  

        nume_familie = request.form['nume-familie']
        prenume = request.form['prenume']
        varsta = int(request.form['varsta'])
        telefon = request.form['telefon']
        judet = request.form['judet']
        oras = request.form['oras']
        email = request.form['email']

        # Dacă utilizatorul are sub 18 ani, verifică acordul părinților, altfel pune NULL
        if varsta < 18:
            parinti_de_acord = "DA" if 'acord-parinti' in request.form else "NU"
        else:
            parinti_de_acord = None  # Se va salva NULL în baza de date pentru 18+

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(''' 
                INSERT INTO inscriere (nume_familie, prenume, varsta, telefon, judet, oras, email, parinti_de_acord)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (nume_familie, prenume, varsta, telefon, judet, oras, email, parinti_de_acord))
            conn.commit()
            print("Datele au fost salvate cu succes!")
            return 'Datele au fost salvate cu succes!'
        except Exception as e:
            print(f"Eroare la salvarea datelor: {e}")
            return 'A apărut o eroare la salvarea datelor.'
        finally:
            cur.close()
            conn.close()

    return render_template('index.html')

@app.route('/vizualizare')
def vizualizare():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, nume_familie, prenume, varsta, telefon, judet, oras, email, COALESCE(parinti_de_acord, \'\') FROM inscriere')
    date = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('vizualizare.html', date=date)


if __name__ == '__main__':
    app.run(debug=True)
