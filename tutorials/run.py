from pathlib import Path

from hydra_zen import launch
from my_app import Config, task_function
from utils import get_pylogger, print_file

log = get_pylogger(__name__)


def main():
    job = launch(
        Config,
        task_function,
        overrides=[
            "player.name=frodo",
            "player.level=2",
            "player.inventory.costume=robe",
            "hydra.job.chdir=True",
        ],
        version_base="1.2",
    )
    job_dir = Path(job.working_dir)
    log.info(f"Job working directory: {job_dir}")
    log.info(f"Job status: {job.status}")
    log.info(f"Job output: {job.return_value}")
    job_outputs = sorted(job_dir.glob("*"))
    log.info(f"Job files: {job_outputs}")
    print_file(job_dir / "player_log.txt")
    print_file(job_dir / ".hydra" / "config.yaml")


if __name__ == "__main__":
    main()
