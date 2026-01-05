from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
import pymongo

app = Flask(__name__)


MONGO_URI = "mongodb+srv://deeshamitra3_db_user:<password>@cluster0.k4rxbm4.mongodb.net/?appName=Cluster0"

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client.my_database 
    users_collection = db.users 
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/api', methods=['GET'])
def get_json_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/form')
def show_form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        name = request.form.get('username')
        email = request.form.get('user_email')

        users_collection.insert_one({
            "name": name, 
            "email": email
        })

        return redirect(url_for('success_page'))

    except Exception as e:

        return render_template('form.html', error=str(e))

@app.route('/success')
def success_page():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)