import gymnasium 
from zombieEnv import ZombieEnv
import gym
from stable_baselines3 import PPO
from zombieEnv import ZombieEnv

# Create the environment
env = ZombieEnv(render_mode='human')

# Create the PPO agent
model = PPO("MultiInputPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=10000)

# Render the environment with human interaction
obs = env.reset()
for _ in range(100):
    action, _ = model.predict(obs)
    obs, _, _, _ = env.step(action)
    env.render(mode='human')

