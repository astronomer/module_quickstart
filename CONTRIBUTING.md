# Module Quickstart Repo

## Guidelines
Quickstarts should:
- **Minimally show a basic connection** (when needed)
- **Minimally show a single example of operator or concept** (some type of hello-world action) 
- Link to other resources rather than reproduce them
- Steps should provide concrete actions with ~1 sentence of description 
- Steps should include code blocks, or images showing what to do in detail, or a direct link to a source that has those
- All DAGs must have Docstrings with the following structure:
```
Before You Start

<do the thing>

Checkpoint

Next Steps

Extras / Reference
```
- Use the following standard for DAGs, unless the example requires otherwise
```python
from airflow import DAG
from datetime import datetime

with DAG("my_example", start_date=datetime(1970, 1, 1), schedule=None):
    ...
```
- Examples should always reflect the most recent version of Airflow at time of writing

## Tagging
PR your addition, merge to `main`, then 
```shell
git checkout main
git pull
git tag v0.1.2
git push --tags
```
The registry should pick up the new tag