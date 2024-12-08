import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

from dashboard.app import app

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
