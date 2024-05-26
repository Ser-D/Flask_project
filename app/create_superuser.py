# from app import create_app, db
# from app.models import User, Role
# from werkzeug.security import generate_password_hash
#
#
# def create_superuser():
#     app = create_app()
#     with app.app_context():
#         db.create_all()
#         if not User.query.filter_by(username='admin').first():
#             admin = User(
#                 username='admin',
#                 email='admin@example.com',
#                 password=generate_password_hash('admin', method='scrypt'),
#                 role='Admin'
#             )
#             db.session.add(admin)
#             db.session.commit()
#             print("Superuser created.")
#         else:
#             print("Superuser already exists.")
#
#
# if __name__ == '__main__':
#     create_superuser()

# from app import app, db
# from app.models import User
# from werkzeug.security import generate_password_hash
#
#
# def create_superuser():
#     with app.app_context():
#         admin = User(
#             username='admin',
#             email='admin@example.com',
#             password=generate_password_hash('password'),
#             role='Admin'
#         )
#         db.session.add(admin)
#         db.session.commit()
#         print('Superuser created')
#
#
# if __name__ == '__main__':
#     create_superuser()
