from model import db, Division

def seed_divisions(app):
    with app.app_context():
        if Division.query.count() == 0:
            divisions = [
                Division(fund_name="Благотворительная больница", total_sum=0, goal=457000),
                Division(fund_name="Одинаково разные", total_sum=0, goal=300000),
                Division(fund_name="Вместо мамы", total_sum=0, goal=639900),
                Division(fund_name="С другой стороны", total_sum=0, goal=688622),
                Division(fund_name="Лагерь в боброво", total_sum=0, goal=140000)
            ]
            db.session.add_all(divisions)
            db.session.commit()
            print("Divisions seeded!")
        else:
            print("Divisions already exist — skipping.")
