# User-CRUD APIs
- Python v3.6 or greater

## Installation requirements
- pip3 install -r requirements.txt 

## Configuration ⚙️
- Copy `config.template.py` as `config.py`
- Create an empty database in database server
- Update values in `config.py`

## Generate Salt value
- Open terminal
- `python3`
- `import bcrypt`
- `bcrypt.gensalt(rounds=12)`
- Copy value and update `salt` key in `config.py`

## Quick Start 🚀
- Open terminal in project root
- Run server: uvicorn main:app --reload --host 0.0.0.0