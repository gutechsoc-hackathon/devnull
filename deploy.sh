virtualenv VENV
cd server
sqlite3 hackathin.db -init schema.sql
echo "1. Run pip install --no-deps -r requirements.txt after activating VENV"
echo "2. Apply the cert disable hack to foursquare on line 719 of __init__.py"
