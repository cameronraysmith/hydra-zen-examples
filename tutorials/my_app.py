from pathlib import Path

import hydra
from game_library import Character, inventory
from hydra.core.config_store import ConfigStore
from hydra_zen import instantiate, make_config, make_custom_builds_fn
from utils import get_pylogger, print_file, print_yaml
"""my_app.py

Command line usage examples:

    python my_app.py hydra.job.chdir=True player=rakesh
    python my_app.py hydra.job.chdir=True player=brinda +player/inventory=advanced
"""

builds = make_custom_builds_fn(populate_full_signature=True)

cs = ConfigStore.instance()

# Create inventory configurations
InventoryConf = builds(inventory)
starter_gear = InventoryConf(gold=10, weapon="stick", costume="tunic")
advanced_gear = InventoryConf(gold=500, weapon="wand", costume="magic robe")
hard_mode_gear = InventoryConf(gold=0, weapon="inner thoughts", costume="rags")

# Registers inventory configurations to group:
#   player/inventory
cs.store(group="player/inventory", name="starter", node=starter_gear)
cs.store(group="player/inventory", name="advanced", node=advanced_gear)
cs.store(group="player/inventory", name="hard_mode", node=hard_mode_gear)

# Creates player profile configurations
CharConf = builds(Character, inventory=starter_gear)

brinda_conf = CharConf(
    name="brinda",
    level=47,
    inventory=InventoryConf(costume="cape", weapon="flute", gold=52),
)
rakesh_conf = CharConf(
    name="rakesh",
    level=300,
    inventory=InventoryConf(costume="PJs", weapon="pillow", gold=41),
)

# Registers player profile configurations to group:
#   player
cs.store(group="player", name="base", node=CharConf)
cs.store(group="player", name="brinda", node=brinda_conf)
cs.store(group="player", name="rakesh", node=rakesh_conf)

# Creates the top-level configuration
## Config = make_config("player1", "player2")
## Config = make_config(player=CharConf)
# Set default group for player to:
#   base
Config = make_config("player", hydra_defaults=["_self_", {"player": "base"}])

cs.store(name="my_app", node=Config)

log = get_pylogger(__name__)


@hydra.main(version_base="1.2", config_path=None, config_name="my_app")
def task_function(cfg: Config):

    log.info("Instantiating player configuration")
    player = instantiate(cfg.player)

    # print_yaml(cfg)
    # print(player)
    log.info(f"Configuration: {cfg}")
    log.info(f"Player: {player}")

    log.info(f"Writing output file")
    with open("player_log.txt", "w") as f:
        f.write(f"Game session log:\n")
        f.write(f"Player: {player}\n")

    log.info(f"Printing .hydra/config.yaml")
    print_file(Path(".hydra/config.yaml"))

    log.info(f"Run Complete")
    return player


if __name__ == "__main__":
    task_function()
