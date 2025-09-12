# datatrac - Dataset Discovery, Registry, and Lineage Tool

## Installation

1. **Install dependencies**:

   ```bash
   uv pip install typer rich fastapi uvicorn sqlalchemy psycopg2-binary
   ```

2. **Install datatrac**:

   ```bash
   cd /path/to/your/datatrac/project
   uv pip install -e .
   ```

## Quick Start

### Push your first dataset

```bash
uv run datatrac.cli.main push data.csv --source "https://example.com/data.csv"
```

### Fetch dataset details

```bash
uv run datatrac.cli.main fetch <dataset-hash>
```

### List all datasets

```bash
uv run datatrac.cli.main fetch --all
```

### Download a dataset

```bash
uv run datatrac.cli.main fetch <dataset-hash> --download
```

### View dataset lineage

```bash
uv run datatrac.cli.main lineage <dataset-hash>
```

### Create lineage between datasets

```bash
uv run datatrac.cli.main lineage --parent <parent-hash> --child <child-hash>
```

### Delete a dataset (Admin)

⚠️ Admin-only operation. Uses a hardcoded password (default: `admin`).

```bash
uv run datatrac.cli.main delete <dataset-hash>
```

### Delete only local copy

```bash
uv run datatrac.cli.main delete <dataset-hash> --local
```

## Web Dashboard

### Start the API server

```bash
cd /path/to/your/datatrac/project/datatrac/api
uv run fastapi dev main.py --port 8000 --host 0.0.0.0
```

### Access the dashboard

Open your browser at: **[http://localhost:8000](http://localhost:8000)**

The dashboard shows:

* Dataset browser with search
* Dataset details (size, hash, source, downloads)
* Upload support
* Lineage management

## Key Commands

| Command    | Description                        | Example                                 |
| ---------- | ---------------------------------- | --------------------------------------- |
| `push`     | Register a new dataset             | `datatrac push data.csv --source "url"` |
| `fetch`    | Show dataset info or download      | `datatrac fetch <hash>`                 |
| `fetch -a` | List all datasets                  | `datatrac fetch --all`                  |
| `lineage`  | View or create lineage links       | `datatrac lineage <hash>`               |
| `delete`   | Deregister or delete local dataset | `datatrac delete <hash> --local`        |

## Configuration

* Local app data directory: `~/.datatrac`
* PostgreSQL database connection is preconfigured in `datatrac/core/config.py`.
* Remote storage server details are also hardcoded (POC stage).

## Dataset Identification

Datasets can be referenced by:

* **Full hash**: e.g., `a1b2c3d4...`
* **Name**: original filename (e.g., `data.csv`)

## Notes

* Default admin password is **hardcoded** as `admin` (for proof of concept).
* Works with Python **3.12+** and uses **uv** for package and command management.
* Frontend (React) is shipped prebuilt, no manual build required.

