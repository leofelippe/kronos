from flask_frozen import Freezer
from kronos import app

freezer = Freezer(app)

if __name__ == '__main__':
    app.run(debug=True)