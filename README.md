# Pokémon API Template

A clean architecture implementation of a Pokémon API that provides CRUD operations and evolution tracking for Pokémon data.

## Features

- ✅ Create, Read, Update, Delete Pokémon
- ✅ Track Pokémon evolutions
- ✅ Clean architecture design
- ✅ Type-safe with Pydantic models
- ✅ Well-structured codebase with separation of concerns

## Project Structure

```
template/
├── src/
│   ├── common/                # Common utilities and types
│   ├── entrypoints/           # API entry points
│   │   └── http/              # HTTP API implementation
│   │       └── pokemon/       # Pokémon endpoints
│   ├── models/                # Domain models
│   └── repositories/          # Data access layer
├── tests/                     # Test suite
└── README.md                  # This file
```

## Architecture

This project follows clean architecture principles:

- **Models**: Domain entities and business logic
- **Repositories**: Data access layer
- **Entrypoints**: API endpoints and request/response handling
- **Mappers**: Convert between API schemas and domain models

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository
```bash
git clone https://github.com/tienndm/pokemon-api.git
cd pokemon-api
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Starting the server

```bash
python -m src.main
```

### API Examples

#### Create a Pokémon

```bash
curl -X POST http://localhost:8000/pokemon \
  -H "Content-Type: application/json" \
  -d '{
    "no": "025",
    "name": "Pikachu",
    "type_name": ["Electric"],
    "previous_evolution_numbers": ["172"],
    "next_evolution_numbers": ["026"]
  }'
```

#### Get a Pokémon

```bash
curl http://localhost:8000/pokemon/025
```

#### Update a Pokémon

```bash
curl -X PATCH http://localhost:8000/pokemon/025 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pikachu (Updated)"
  }'
```

#### Delete a Pokémon

```bash
curl -X DELETE http://localhost:8000/pokemon/025
```

## Development

### Running Tests

```bash
pytest
```

### Code Style

This project follows PEP 8 guidelines. Use flake8 and black for linting and formatting:

```bash
flake8 src tests
black src tests
```

## License

MIT
