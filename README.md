# DataTrac - Dataset Management & Lineage Tool

DataTrac helps you **discover, manage, and trace datasets**. It combines a CLI for power users with a FastAPI + React web dashboard for interactive exploration.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourname/datatrac.git
   cd datatrac
   ```

2. **Install dependencies using [uv](https://github.com/astral-sh/uv)**

   ```bash
   uv pip install -r requirements.txt
   ```

3. **Run in editable mode** (so you can use the CLI and API directly):

   ```bash
   uv pip install -e .
   ```

---

## Quick Start

### CLI Usage

Run CLI commands using `uv run`:

#### List all datasets

```bash
uv run python -m datatrac.cli.main fetch -a
```

#### Fetch details of a dataset

```bash
uv run python -m datatrac.cli.main fetch <dataset_hash>
```

#### Download a dataset

```bash
uv run python -m datatrac.cli.main fetch <dataset_hash> --download
```

#### Push a new dataset

```bash
uv run python -m datatrac.cli.main push path/to/file.csv --source "http://example.com/data"
```

#### View or create lineage

```bash
# View lineage
uv run python -m datatrac.cli.main lineage <dataset_hash>

# Create a lineage link
uv run python -m datatrac.cli.main lineage --parent <parent_hash> --child <child_hash>
```

#### Delete a dataset

```bash
# Delete locally only
uv run python -m datatrac.cli.main delete <dataset_hash> --local

# Delete remotely (admin only)
uv run python -m datatrac.cli.main delete <dataset_hash> --password admin
```

---

### Web Dashboard

Start the FastAPI + React dashboard:

```bash
cd datatrac/api
uv run fastapi run
```

Then open your browser at:

```
http://localhost:8000
```

The dashboard includes:

* **Dataset browser**: List and search datasets
* **Lineage explorer**: View parent/child relationships
* **Metadata view**: Size, source, registry path, and download stats

---

## Key Commands

| Command   | Description                        | Example                          |
| --------- | ---------------------------------- | -------------------------------- |
| `fetch`   | Retrieve dataset info or download  | `fetch <hash> --download`        |
| `push`    | Register a new dataset             | `push data.csv --source "url"`   |
| `lineage` | View or create lineage links       | `lineage --parent h1 --child h2` |
| `delete`  | Remove dataset locally or remotely | `delete <hash> --local`          |

---

## How It Works

* **Hashing**: Every dataset file is identified by a unique SHA256 hash.
* **Registry**: Metadata is stored in a PostgreSQL database.
* **Remote storage**: Files are uploaded via `scp` to a central server.
* **Lineage tracking**: Relationships between parent and derived datasets are recorded.
* **Web UI**: React frontend lets you browse datasets visually.

---

## For Developers

* Database schema is defined in `datatrac/core/models.py`
* Business logic in `datatrac/core/manager.py`
* API in `datatrac/api/main.py`
* CLI in `datatrac/cli/main.py`

Contributions are welcome!
