import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting EasePharma (Docker Mode) on Port 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)