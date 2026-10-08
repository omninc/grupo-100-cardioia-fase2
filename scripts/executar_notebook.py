"""Executa todas as células em um kernel limpo, sobrescrevendo suas saídas."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
path = root / 'notebooks/cardioia_fase2.ipynb'
nb = nbformat.read(path, as_version=4)
NotebookClient(nb, timeout=180, kernel_name='python3', resources={'metadata': {'path': str(root)}}).execute()
nbformat.write(nb, path)
print('Notebook executado sem erros:', path.name)
