import numpy as np
from pathlib import Path
import logging
log = logging.getLogger(__name__)


class Writer:
    """Abstract output formatter class."""

    def __init__(self, fname: str):
        self.fname = fname

    def save(self, output_dir: str = "."):
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        with open(output_dir / self.fname, "w") as file:
            file.write(str(self))
        log.info(f"Saved output to {output_dir / self.fname}")


class PA5(Writer):
    """Output formatter class for programming assignment 1."""

    def __init__(self, name: str, arr, iteration):
        super().__init__(f"{name}-Output.txt")
        self.name = name
        self.arr = arr
        self.iteration = iteration

    def __str__(self):
        outputs = []
        name = self.name
        iteration = self. iteration
        header = name + "-Output.txt"
        # outputs.append(f"{self.iteration}, {header}, 6")
        outputs.append(f"{iteration}, {header}, 6")
        outputs.append(
            f"76.6341  -37.1834   -9.9843  159.6028  -33.5675  101.9273")
        arr = self.arr

        for i in range(int(iteration)):
            # for i in range(150):
            outputs.append(" ".join(map(lambda x: f"  {x:.03f}", arr[i])))

        return "\n".join(outputs)
