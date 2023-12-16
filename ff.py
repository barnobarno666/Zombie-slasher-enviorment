from stable_baselines3 import DQN
# from stable_baselines3.common.envs import DummyVecEnv
from zombieEnvV2 import ZombieEnv
# Create the environment
env = ZombieEnv(render_mode="human")

# Wrap the environment in a vectorized environment
# env = DummyVecEnv([lambda: env])

# Create the PPO agent
model = DQN("MultiInputPolicy", env, verbose=1)
# Train the agent
model.learn(total_timesteps=10000)

# # Render each training episode
# for _ in range(10):
#     obs,_ = env.reset()
#     done = False
#     while not done:
#         # Handle Pygame events


#         action, _ = model.predict(obs)
#         obs, _, done, _, _ = env.step(action)
#         #env.render()

