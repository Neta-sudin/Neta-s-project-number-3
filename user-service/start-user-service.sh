#!/bin/bash


echo "🚀 Starting User Service..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if ! docker ps > /dev/null 2>&1; then
    echo "⚠️  Docker is not running!"
    echo ""
    echo "Please start Docker Desktop:"
    echo "  1. Open Spotlight (Cmd + Space)"
    echo "  2. Type 'Docker' and press Enter"
    echo "  3. Wait for Docker to start (whale icon in menu bar)"
    echo ""
    echo "Or run: open -a Docker"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

echo "🐳 Starting MySQL database..."
docker run -d \
  --name user_service_db \
  -e MYSQL_DATABASE=user_db \
  -e MYSQL_ROOT_PASSWORD=root_password \
  -p 3306:3306 \
  -v "$SCRIPT_DIR/resources/db-migrations:/docker-entrypoint-initdb.d" \
  mysql:8.0 --default-authentication-plugin=mysql_native_password 2>/dev/null || echo "Database container already exists (this is OK)"

echo "⏳ Waiting for MySQL to initialize (15 seconds)..."
sleep 15

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the User Service, run:"
echo "  uvicorn main:app --reload --port 8000"
echo ""
echo "Then open: http://localhost:8000/docs"
echo ""

