from app import db, User
admin = User.query.filter_by(username='admin').first()
print(admin)  # Should show your admin user