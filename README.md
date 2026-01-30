# Bible Translations API

A FastAPI-based RESTful API for accessing Bible translations, books, and verses from a SQLite database.

## Features

- 📖 Access multiple Bible translations
- 📚 Browse books by testament (Old Testament / New Testament)
- 🔍 Search verses by text content
- 📄 Retrieve individual verses, verse ranges, or entire chapters
- 🚀 Fast and efficient read-only API
- 📝 Interactive API documentation with Swagger UI

## Project Structure

```
bible/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database connection management
│   ├── models.py            # Pydantic models for request/response schemas
│   └── routers/
│       ├── __init__.py
│       ├── translations.py  # Translation endpoints
│       ├── books.py         # Books endpoints
│       └── verses.py        # Verses endpoints
├── docs/
│   ├── db_schema.json       # Database schema documentation
│   └── SCHEMA_README.md     # Schema description
├── bible.db                 # SQLite database (not included in repo)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

1. Ensure you have Python 3.8+ installed

2. Activate your virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make sure your `bible.db` SQLite database is in the project root directory

## Running the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API Base URL: `http://localhost:8000`
- Interactive Documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative Documentation (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Root
- `GET /` - API information and available endpoints
- `GET /health` - Health check

### Translations
- `GET /translations/` - Get all translations
- `GET /translations/{translation_id}` - Get translation by ID
- `GET /translations/abbreviation/{abbreviation}` - Get translation by abbreviation (e.g., KJV, NIV)

### Books
- `GET /books/` - Get all books (optionally filter by testament: `?testament=OT` or `?testament=NT`)
- `GET /books/{book_id}` - Get book by ID
- `GET /books/name/{book_name}` - Get book by name

### Verses
- `GET /verses/` - Get verses with filters:
  - Required: `translation`, `book`, `chapter`
  - Optional: `verse_start`, `verse_end` (for ranges)
- `GET /verses/{verse_id}` - Get verse by ID
- `GET /verses/search/text` - Search verses by text content
  - Parameters: `query`, `translation` (optional), `testament` (optional), `limit`
- `GET /verses/chapter/all` - Get all verses from a chapter
  - Parameters: `translation`, `book`, `chapter`

## Example Usage

### Get all translations
```bash
curl http://localhost:8000/translations/
```

### Get a specific verse (John 3:16 in KJV)
```bash
curl "http://localhost:8000/verses/?translation=KJV&book=John&chapter=3&verse_start=16"
```

### Get a range of verses (Psalm 23:1-6 in NIV)
```bash
curl "http://localhost:8000/verses/?translation=NIV&book=Psalms&chapter=23&verse_start=1&verse_end=6"
```

### Get all verses from a chapter
```bash
curl "http://localhost:8000/verses/chapter/all?translation=KJV&book=Genesis&chapter=1"
```

### Search for verses containing "love"
```bash
curl "http://localhost:8000/verses/search/text?query=love&translation=KJV&limit=10"
```

### Get all Old Testament books
```bash
curl "http://localhost:8000/books/?testament=OT"
```

## Database Schema

The API uses a SQLite database with three main tables:

- **translations**: Bible translation information (id, name, abbreviation, language)
- **books**: Books of the Bible (id, name, testament)
- **verses**: Individual verses (id, translation_id, book_id, chapter, verse, text)

For detailed schema information, see [docs/db_schema.json](docs/db_schema.json) and [docs/SCHEMA_README.md](docs/SCHEMA_README.md).

## Development

### Adding New Endpoints

1. Create or modify routers in `app/routers/`
2. Define Pydantic models in `app/models.py` if needed
3. Import and include the router in `app/main.py`

### API Design Principles

- All endpoints are **read-only** (GET requests only)
- Consistent error handling with appropriate HTTP status codes
- Comprehensive input validation using Pydantic models
- Clear and descriptive endpoint documentation

## Production Deployment

For production deployment:

1. Update CORS settings in `app/main.py` to restrict allowed origins
2. Use a production ASGI server (uvicorn with multiple workers or gunicorn)
3. Set up proper logging and monitoring
4. Consider using a reverse proxy (nginx, traefik)
5. Ensure database file has appropriate permissions

Example production command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Docker / Compose

This repository includes a `Dockerfile` and `docker-compose.yml` for local development.

Build the image:

```bash
docker compose build
```

Run (with host DB mounted):

```bash
docker compose up
```

Alternatively, run a single container with the DB mounted:

```bash
docker build -t bible-api:latest .
docker run -p 8000:8000 -v "$(pwd)/bibles.db":/app/bibles.db:ro -e BIBLES_DB_PATH=/app/bibles.db bible-api:latest
```

## Deploying with Portainer or Production

The CI workflow publishes images to GitHub Container Registry (GHCR) as:

- `ghcr.io/vhmlab/bible-api:latest`
- `ghcr.io/vhmlab/bible-api:<commit-sha>`

Replace `vhmlab` with your GitHub username or organization if different.

Recommended production stack (use this file: `docker-compose.prod.yml`):

```yaml
version: "3.8"
services:
  bible-api:
    image: ghcr.io/vhmlab/bible-api:latest
    environment:
      - BIBLES_DB_PATH=/app/bibles.db
    volumes:
      - /srv/bible/bibles.db:/app/bibles.db:ro
    ports:
      - "8000:8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
      interval: 30s
      timeout: 5s
      retries: 3
```

Portainer: create a new Stack → choose "Repository" or paste the compose content, set branch `main` and compose path `docker-compose.prod.yml` (or paste the YAML directly). If GHCR is private, add registry credentials in Portainer (Registry: `ghcr.io`).

Host DB setup example:

```bash
sudo mkdir -p /srv/bible
sudo cp ./bibles.db /srv/bible/bibles.db
sudo chmod 0444 /srv/bible/bibles.db
```

Then deploy the stack in Portainer or run locally with:

```bash
docker compose -f docker-compose.prod.yml up -d
```

## License

MIT License

## Support

For issues and questions, please refer to the API documentation at `/docs` when running the server.
