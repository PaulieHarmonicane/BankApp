from flask import Flask, request, jsonify, render_template
from model import db, Donation, Division
from seed import seed_divisions as sd
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

# with app.app_context():
#     db.create_all()

    
@app.get("/")
def home():
    return "Server is running!"

@app.get("/start")
def start_page():
    return render_template("start.html")

@app.get("/admin")
def admin_page():
    return render_template("admin.html")

@app.get("/stat")
def stat_page():
    return render_template("stat.html")

@app.get("/payment")
def payment_page():
    return render_template("payment.html")

@app.get("/withdraw")
def withdraw_page():
    return render_template("withdraw.html")

@app.get("/done")
def done_page():
    return render_template("done.html")




@app.post("/add_donation")
def add_donation():
    print("Request json: ", request.json)
    data = request.json
    donation = Donation(
        fund_name=data["fund_name"],
        rub_sum=data["rub_sum"],
        pieces_num=data["pieces_num"],
        date=data["date"],
        time=data["time"]
    )
    db.session.add(donation)
    db.session.commit()
    return jsonify({"status": "ok", "id": donation.id})

@app.get("/find_donation_by_id")
def get_pieces_balance():
    c_id = request.args.get("id", type=int)
    print("ID из запроса:", c_id)
    if c_id is None:
        return jsonify({"status": -1}), 400
    donation = Donation.query.filter_by(id=c_id).first()
    if not donation:
        return jsonify({"status": -1})
    else:
        return jsonify({"status": "ok", "pieces_num": donation.pieces_num})
    

@app.post("/update_pieces")
def update_pieces():
    data = request.json
    donation_id = data.get("id")
    new_pieces = data.get("pieces_num")
    print("Получено:", data)
    if donation_id is None or new_pieces is None:
        return jsonify({"status": "error", "message": "id и pieces_num обязательны"}), 400
    donation = Donation.query.filter_by(id=donation_id).first()
    if not donation:
        return jsonify({"status": "not_found"}), 404
    elif donation.pieces_num < new_pieces:
        print("Not enough")
        return jsonify({"status": "not_enough"})
    donation.pieces_num -=new_pieces
    db.session.commit()
    return jsonify({"status": "ok", "updated": donation.pieces_num})


@app.post("/add_total")
def add_total():
    data = request.json
    fund_name = data.get("fund")
    new_donation = data.get("don_amount")
    totals = Division.query.filter_by(fund_name=fund_name).first()
    totals.total_sum += new_donation
    db.session.commit()
    if totals.total_sum > totals.goal:
        return jsonify({"status": "ok", "msg": "completed"})
    else:
        return jsonify({"status": "ok", "msg": "go_on"})
    
@app.get("/get_stat")
def get_stats():
    stats = Division.query.all()
    data = [
        {
            "fund": s.fund_name,
            "goal": s.goal,
            "current": s.total_sum
        }
        for s in stats
    ]
    print(data)
    return jsonify({"status": "ok", "data": data})
    
    
@app.route("/clear_db", methods=["POST"])
def reset_db():
    db.drop_all()
    db.create_all()
    sd(app)
    print("done!!")
    return jsonify({"status": "ok"})

    
    
    


if __name__ == "__main__":
    app.run(debug=True)



#gunicorn app:app --workers 4 --bind 0.0.0.0:5050