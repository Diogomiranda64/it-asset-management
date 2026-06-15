from flask import Flask, render_template, request, redirect, session, send_file
from database import get_connection
import pandas as pd

app = Flask(__name__)
app.secret_key = "evolve_secret_key"


@app.route('/')
def home():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM assets")
    total_assets = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM assets WHERE status='Active'"
    )
    active_assets = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        total_assets=total_assets,
        active_assets=active_assets
    )

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM users
            WHERE username=%s
            AND password=%s
        """, (username, password))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['user'] = user['username']
            return redirect('/dashboard')

        return "Invalid username or password"

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM assets")
    total_assets = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM assets WHERE status='Active'"
    )
    active_assets = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_assets=total_assets,
        active_assets=active_assets
    )


@app.route('/assets')
def assets():

    if 'user' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM assets")
    assets = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("assets.html", assets=assets)


@app.route('/add-asset', methods=['GET', 'POST'])
def add_asset():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        asset_tag = request.form['asset_tag']
        name = request.form['name']
        brand = request.form['brand']
        model = request.form['model']
        status = request.form['status']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO assets
            (asset_tag, name, brand, model, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (asset_tag, name, brand, model, status))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/assets')

    return render_template("add_asset.html")


@app.route('/edit-asset/<int:id>', methods=['GET', 'POST'])
def edit_asset(id):

    if 'user' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        asset_tag = request.form['asset_tag']
        name = request.form['name']
        brand = request.form['brand']
        model = request.form['model']
        status = request.form['status']

        cursor.execute("""
            UPDATE assets
            SET asset_tag=%s,
                name=%s,
                brand=%s,
                model=%s,
                status=%s
            WHERE id=%s
        """, (
            asset_tag,
            name,
            brand,
            model,
            status,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/assets')

    cursor.execute(
        "SELECT * FROM assets WHERE id=%s",
        (id,)
    )

    asset = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "edit_asset.html",
        asset=asset
    )


@app.route('/delete-asset/<int:id>')
def delete_asset(id):

    if 'user' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM assets WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/assets')


@app.route('/reports')
def reports():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM assets")
    total_assets = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM assets WHERE status='Active'"
    )
    active_assets = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        'reports.html',
        total_assets=total_assets,
        active_assets=active_assets
    )


@app.route('/interventions')
def interventions():

    if 'user' not in session:
        return redirect('/login')

    return render_template('interventions.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/export-assets')
def export_assets():

    conn = get_connection()

    query = "SELECT * FROM assets"

    df = pd.read_sql(query, conn)

    conn.close()

    filename = "assets_report.csv"

    df.to_csv(filename, index=False)

    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)