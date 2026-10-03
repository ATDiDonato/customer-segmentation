"""Refresh preparation, full-data k=3 segments and PCA; preserve saved diagnostics."""
import copy
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main():
    path = Path(__file__).with_name('customer_segmentation.ipynb')
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)

    indices = [i for i, cell in enumerate(notebook.cells)
               if 'portfolio-refresh' in cell.metadata.get('tags', [])]
    selected = nbformat.v4.new_notebook(
        cells=[copy.deepcopy(notebook.cells[i]) for i in indices],
        metadata=copy.deepcopy(notebook.metadata),
    )
    client = NotebookClient(
        selected, timeout=1800, kernel_name='python3',
        resources={'metadata': {'path': str(path.parent)}},
        on_cell_start=lambda cell, cell_index: print(f'Refreshing portfolio cell {indices[cell_index]}', flush=True),
    )
    client.execute()
    for i, cell in zip(indices, selected.cells):
        notebook.cells[i] = cell
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    print(f'Refreshed {len(indices)} selected cells; saved diagnostics and supplementary figures preserved.')


if __name__ == '__main__':
    main()
