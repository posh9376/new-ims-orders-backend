import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from .extensions import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Database Configuration
    db_config = {
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'POSTGRES_HOST': os.getenv('POSTGRES_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'POSTGRES_DB': os.getenv('POSTGRES_DB')
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{db_config['POSTGRES_USER']}:{db_config['POSTGRES_PASSWORD']}"
        f"@{db_config['POSTGRES_HOST']}:{db_config['DB_PORT']}/{db_config['POSTGRES_DB']}"
    )
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_secret_key')

   
    db.init_app(app)
    CORS(app,resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}},supports_credentials=True)
    jwt = JWTManager(app)

    @app.before_request
    def handle_preflight():
        """ Ensure OPTIONS requests return correct CORS headers. """
        if request.method == "OPTIONS":
            response = jsonify({"message": "CORS Preflight OK"})
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Content-Type"] = "application/json"  # Set JSON Content-Type
            return response, 200

    @app.after_request
    def add_cors_headers(response):
        """ Ensure all responses include correct CORS headers and JSON Content-Type. """
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        #  Ensure the response is always JSON
        if response.content_type == "text/html; charset=utf-8":
            response.headers["Content-Type"] = "application/json"
        
        return response

        


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

    @app.route('/create_access_token', methods=['POST'])
    def create_token():
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({'message': 'User ID is required'}), 400
        
        access_token = create_access_token(identity=str(data['user_id']))
        return jsonify(access_token=access_token)



    return app

def create_tables():
    """Executes raw SQL to create tables with all columns predefined, including foreign keys."""
    raw_sql = """
    CREATE TABLE IF NOT EXISTS "user" (  -- Fix: Enclosed "user" in double quotes
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        phone_number VARCHAR(20) NOT NULL,
        role_id INTEGER NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    order_name VARCHAR(100),
    order_description VARCHAR(250),
    name VARCHAR(50) NOT NULL,
    cost FLOAT NOT NULL,
    vendor_id INTEGER NOT NULL,
    vat FLOAT DEFAULT 0,
    quantity INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    date_ordered DATE NOT NULL,
    payment_status VARCHAR(50),
    dispatch_status VARCHAR(50),
    delivery_charges FLOAT DEFAULT 0,
    reason VARCHAR(50) NULL,
    initialiser VARCHAR(50) NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE, 
    CONSTRAINT fk_vendor FOREIGN KEY (vendor_id) REFERENCES vendors(id) ON DELETE CASCADE
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
    dbname=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('DB_PORT')
    )


    with conn.cursor() as cur:
        cur.execute(raw_sql)
        conn.commit()

    conn.close()
