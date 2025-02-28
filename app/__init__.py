import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask
from .extensions import db, cors  # Removed `migrate`

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Database Configuration
    db_config = {
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('DB_PORT'),
        'database': os.getenv('POSTGRES_DB')
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )

    # Initialize Extensions (Only keeping CORS)
    db.init_app(app)
    cors.init_app(app)

    # Create tables using raw SQL
    with app.app_context():
        create_tables()

    # Import Blueprints inside the function to avoid circular imports
    from .routes.orders import orders_bp
    from .routes.received import received_bp
    from .routes.home import home_bp

    # Register Blueprints
    app.register_blueprint(orders_bp)
    app.register_blueprint(received_bp)
    app.register_blueprint(home_bp)

    return app

def create_tables():
    """Executes raw SQL to create tables with all columns predefined."""
    raw_sql = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        order_name VARCHAR(100),
        order_description VARCHAR(250),
        name VARCHAR(50) NOT NULL,
        cost FLOAT NOT NULL,
        space VARCHAR(50),
        vat FLOAT DEFAULT 0,
        quantity INTEGER NOT NULL,
        status VARCHAR(50) NOT NULL,
        date_ordered DATE NOT NULL,
        payment_status VARCHAR(50),
        dispatch_status VARCHAR(50),
        delivery_charges FLOAT DEFAULT 0,
        reason VARCHAR(50) NULL,
        initialiser VARCHAR(50) NULL
    );

    CREATE TABLE IF NOT EXISTS received (
        id SERIAL PRIMARY KEY,
        order_id INTEGER NOT NULL,
        received_quantity INTEGER NOT NULL,
        date_received DATE NOT NULL,
        CONSTRAINT fk_order FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
    );
    """

    # Connect directly using psycopg2
    conn = psycopg2.connect(
        dbname=os.getenv('name'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        host=os.getenv('host'),
        port=os.getenv('port')
    )

    with conn.cursor() as cur:
        cur.execute(raw_sql)
        conn.commit()

    conn.close()
