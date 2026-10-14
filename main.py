from flask import Flask, request, session, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///app.db"

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(130), nullable=False)
    age = db.Column(db.Integer)
    
    
@app.route("/get-user", methods=["GET"])
def get_user():
    users = User.query.all()
    return render_template("home.html",users=users)



# This is Create Section to insert data in table
@app.route("/add-user", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    age = data.get("age")
    
    user = User(
        name=name,
        email=email,
        age=age
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "message":"the user added successfully",
        "id":user.id,
        "name":user.name,
        "email":user.email,
        "age":age
    })
    
    
    
    
    
    
# This is a Read Section to read All users from database
@app.route("/get-users", methods=["GET"])
def get_users():
    data = User.query.all()
    user_data = []
    
    for user in data:
        user_data.append(
            {
                "id":user.id,
                "name":user.name,
                "email":user.email,
                "age":user.age
            }
        )
    return jsonify(user_data)



# Get User by Id
@app.route("/get-users/<int:id>", methods=["GET"])
def get_user_by_id(id):
    user = db.get_or_404(User,id)
    return jsonify(
        {
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "age":user.age
        }
    )
    
    
    
    
# Update User By ID
@app.route("/update-user/<int:id>", methods=["PATCH"])
def update_user(id):
    data = request.get_json()
    user = db.get_or_404(User,id)
    if "name" in data:
        user.name = data["name"]
        
    if "age" in data:
        user.age = data["age"]
            
    if "email" in data:
        user.email = data["email"]
    
    db.session.commit()
    
    return jsonify(
        {
            "message":"User Updated Successfully",
            "id":user.id
        }
    )    
    
    
    
    
# Delete User From Users
@app.route("/delete-user/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = db.get_or_404(User,id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        "message":"The use is deleted Successfully",
        "id":user.id
    })
        
    
    
    
    

@app.route("/")
def home():
    return "Hello Neeraj"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)