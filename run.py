from app import app, db
from app.models import User, Ticket, Group


if __name__ == "__main__":
    app.run(debug=True)