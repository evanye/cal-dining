from app import db, models

date = '2013-05-28'
already_removed = set()
count = 0
for entry in models.Menu.query.filter_by(date=date).all():
	m = models.Menu(date=date, location=entry.location, meal = entry.meal, food_id = entry.food_id)
	if str(m) in already_removed:
		continue
	else:
		already_removed.add(str(m))
	dups = models.Menu.query.filter_by(date=date, location=m.location, meal=m.meal, food_id=m.food_id).all()
	count += len(dups)-1
	for d in dups[1:]:
		db.session.delete(d)

