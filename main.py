from app import app  # Importing the Flask app instance from the app module

if __name__ == "__main__":
    # Running the Flask app with debugging enabled on port 5001
    # 'host="0.0.0.0"' makes the app accessible from any network interface
    app.run(host="0.0.0.0", port=5001, debug=True)
