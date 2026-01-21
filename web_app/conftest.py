import sys
from pathlib import Path

# Aggiungi la directory root al PYTHONPATH
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Aggiungi anche web_app per gli import relativi interni
web_app_dir = root_dir / "web_app"
sys.path.insert(0, str(web_app_dir))