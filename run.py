
from app import create_app
from app.orm.database.base import create_tables
import sys
import traceback

def main():
    try:
        app = create_app()
        create_tables(app)  # Ensure tables are created before running the app  
        print("✅ Flask app created successfully")
        print("📊 Available routes:")
        
        # List all routes
        for rule in app.url_map.iter_rules():
            methods = ','.join(rule.methods - {'OPTIONS', 'HEAD'})
            print(f"  {methods:10} {rule.rule}")
        
        print("\n🚀 Starting server on http://127.0.0.1:5000")
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except Exception as e:
        print(f"❌ Error creating or running app: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
