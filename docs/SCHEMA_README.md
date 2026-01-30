**Purpose**: This repository file describes the `bibles.db` schema and provides a short usage snippet for large language models or other tools that need to understand the database layout.

- **SQL DDL**: see `db_schema.sql` for the canonical CREATE statements and indexes.
- **Machine-readable**: see `db_schema.json` for a JSON description of tables, columns, foreign keys, and indexes.

Example prompt you can give an LLM (concise):

"The SQLite database has three tables: `translations(id, name, abbreviation, language)`, `books(id, name, testament)` and `verses(id, translation_id, book_id, chapter, verse, text)` with foreign keys from `verses.translation_id -> translations.id` and `verses.book_id -> books.id`. Indexes: `(book_id,chapter,verse)` and `(translation_id,book_id,chapter,verse)` (unique). Write SQL to retrieve all verses for translation 'KJV' Genesis 1:1-5."

Quick examples:

- Get translation id by abbreviation:
  `SELECT id FROM translations WHERE abbreviation = 'KJV';`
- Retrieve a verse text:
  `SELECT v.text FROM verses v JOIN translations t ON v.translation_id=t.id JOIN books b ON v.book_id=b.id WHERE t.abbreviation='KJV' AND b.name='Genesis' AND v.chapter=1 AND v.verse=1;`
- Efficient range query (Genesis 1:1–5):
  `SELECT v.chapter, v.verse, v.text FROM verses v JOIN translations t ON v.translation_id=t.id JOIN books b ON v.book_id=b.id WHERE t.abbreviation='KJV' AND b.name='Genesis' AND v.chapter=1 AND v.verse BETWEEN 1 AND 5 ORDER BY v.chapter, v.verse;`

If you want the schema in another format (YAML, Protobuf, OpenAPI, etc.), say which and I will add it.
