import gym
from stable_baselines3 import PPO
from Snake_game import Snake_game
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Load the trained model
model = PPO.load("ppo_snake_initial")
#model = PPO.load("ppo_snake_from_model7")

# Create the environment
env = Snake_game()

n_try = 1000
for i in range(n_try):
#Image for initial state
    fig, ax = plt.subplots(figsize=(6,6))
    # plt.imshow(env.render(mode='rgb_array'))
    # plt.axis('off')
    # plt.savefig("snake_init.png",dpi=150)

    #Framework to save animgif
    frames = []
    fps=24

    n_steps = 1000
    obs = env.reset()
    for step in range(n_steps):
        #print("Step {}".format(step + 1))
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        #print('position=', obs['position'], 'direction=', obs['direction'])
        #print('reward=', reward, 'done=', done)
        frames.append([ax.imshow(env.render(mode='rgb_array'), animated=True)])
        if done:
            print("Game over!", "steps run =", step)
            final_step = step
            break

    if (final_step > 50):
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None) #to remove white bounding box        
        anim = animation.ArtistAnimation(fig, frames, interval=int(1000/fps), blit=True,repeat_delay=1000)
        anim.save("snake_test.gif",dpi=150)
        break

    plt.close()

# Close the environment
env.close()
