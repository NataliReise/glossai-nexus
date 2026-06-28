"""Create a private local activation file for First Spark."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXAMPLE_PATH = ROOT / "activation.example.json"
LOCAL_PATH = ROOT / "activation.local.json"


def create_local_activation(example_path: Path = EXAMPLE_PATH, local_path: Path = LOCAL_PATH) -> str:
    """Create activation.local.json from activation.example.json if needed."""
    if local_path.exists():
        return (
            "Local activation file already exists.\n\n"
            f"Nothing was changed:\n{local_path}\n"
        )

    if not example_path.exists():
        raise FileNotFoundError(f"Example activation file not found: {example_path}")

    shutil.copyfile(example_path, local_path)
    return (
        "Local activation file created.\n\n"
        f"File:\n{local_path}\n\n"
        "Next step:\n"
        "Edit this file and add your private local activation data.\n\n"
        "This file is ignored by Git and should stay private."
    )


def main() -> None:
    """Run the local activation creation helper."""
    print(create_local_activation())


if __name__ == "__main__":
    main()
