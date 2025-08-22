from app import create_app

app = create_app()

@app.route('/test')
def test():
    return {"message": "Test route working"}

if __name__ == "__main__":
    print("Starting Flask app...")
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"Error starting app: {e}")
        import traceback
        traceback.print_exc()
