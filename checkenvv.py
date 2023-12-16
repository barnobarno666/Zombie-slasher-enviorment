from stable_baselines3.common.env_checker import check_env
from zombieEnvV2 import ZombieEnv

env = ZombieEnv()
# It will check your custom environment and output additional warnings if needed
check_env(env)
