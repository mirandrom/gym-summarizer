from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.policies import MlpPolicy
from gym.envs.registration import register
from stable_baselines import DQN, A2C
import gym
import os
import numpy as np

best_mean_reward, n_steps = -np.inf, 0


def callback(_locals, _globals):
    global n_steps, best_mean_reward
    if (n_steps + 1) % 100 == 0:
        print(n_steps)
    n_steps += 1
    return True


register(
    id='ExtractiveEnv-v0',
    entry_point='gym_summarizer.envs:ExtractiveEnv',
)

# Create log dir
log_dir = "logs/gym"
os.makedirs(log_dir, exist_ok=True)

env_name = 'ExtractiveEnv-v0'
env = gym.make(env_name)
env = DummyVecEnv([lambda: env])
model = A2C(MlpPolicy, env, tensorboard_log=f"../logs/tensorboard/{env_name}/",ent_coef=0.1, verbose=1)
model.learn(total_timesteps=1000, callback=callback)