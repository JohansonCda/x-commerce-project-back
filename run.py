
from app import create_app
from app.orm.database import create_tables


app = create_app()
create_tables(app)

if __name__ == "__main__":
    app.run(debug=True)
