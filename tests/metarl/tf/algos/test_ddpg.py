"""This script creates a test that fails when metarl.tf.algos.DDPG performance
is too low.
"""
import gym
import pytest
import tensorflow as tf

from metarl.envs import normalize
from metarl.np.exploration_strategies import OUStrategy
from metarl.replay_buffer import SimpleReplayBuffer
from metarl.tf.algos import DDPG
from metarl.tf.envs import TfEnv
from metarl.tf.experiment import LocalTFRunner
from metarl.tf.policies import ContinuousMLPPolicy
from metarl.tf.q_functions import ContinuousMLPQFunction
from tests.fixtures import snapshot_config, TfGraphTestCase


class TestDDPG(TfGraphTestCase):
    """Tests for DDPG algorithm."""

    @pytest.mark.large
    def test_ddpg_double_pendulum(self):
        """Test DDPG with Pendulum environment."""
        with LocalTFRunner(snapshot_config, sess=self.sess) as runner:
            env = TfEnv(gym.make('InvertedDoublePendulum-v2'))
            action_noise = OUStrategy(env.spec, sigma=0.2)
            policy = ContinuousMLPPolicy(env_spec=env.spec,
                                         hidden_sizes=[64, 64],
                                         hidden_nonlinearity=tf.nn.relu,
                                         output_nonlinearity=tf.nn.tanh)
            qf = ContinuousMLPQFunction(env_spec=env.spec,
                                        hidden_sizes=[64, 64],
                                        hidden_nonlinearity=tf.nn.relu)
            replay_buffer = SimpleReplayBuffer(env_spec=env.spec,
                                               size_in_transitions=int(1e5),
                                               time_horizon=100)
            algo = DDPG(
                env_spec=env.spec,
                policy=policy,
                policy_lr=1e-4,
                qf_lr=1e-3,
                qf=qf,
                replay_buffer=replay_buffer,
                steps_per_epoch=20,
                target_update_tau=1e-2,
                n_train_steps=50,
                discount=0.9,
                min_buffer_size=int(5e3),
                exploration_strategy=action_noise,
            )
            runner.setup(algo, env)
            last_avg_ret = runner.train(n_epochs=10, batch_size=100)
            assert last_avg_ret > 60

            env.close()

    @pytest.mark.large
    def test_ddpg_pendulum(self):
        """Test DDPG with Pendulum environment.

        This environment has a [-3, 3] action_space bound.
        """
        with LocalTFRunner(snapshot_config, sess=self.sess) as runner:
            env = TfEnv(normalize(gym.make('InvertedPendulum-v2')))
            action_noise = OUStrategy(env.spec, sigma=0.2)
            policy = ContinuousMLPPolicy(env_spec=env.spec,
                                         hidden_sizes=[64, 64],
                                         hidden_nonlinearity=tf.nn.relu,
                                         output_nonlinearity=tf.nn.tanh)
            qf = ContinuousMLPQFunction(env_spec=env.spec,
                                        hidden_sizes=[64, 64],
                                        hidden_nonlinearity=tf.nn.relu)
            replay_buffer = SimpleReplayBuffer(env_spec=env.spec,
                                               size_in_transitions=int(1e6),
                                               time_horizon=100)
            algo = DDPG(
                env_spec=env.spec,
                policy=policy,
                policy_lr=1e-4,
                qf_lr=1e-3,
                qf=qf,
                replay_buffer=replay_buffer,
                steps_per_epoch=20,
                target_update_tau=1e-2,
                n_train_steps=50,
                discount=0.9,
                min_buffer_size=int(5e3),
                exploration_strategy=action_noise,
            )
            runner.setup(algo, env)
            last_avg_ret = runner.train(n_epochs=10, batch_size=100)
            assert last_avg_ret > 10

            env.close()

    @pytest.mark.large
    def test_ddpg_pendulum_with_decayed_weights(self):
        """Test DDPG with Pendulum environment and decayed weights.

        This environment has a [-3, 3] action_space bound.
        """
        with LocalTFRunner(snapshot_config, sess=self.sess) as runner:
            env = TfEnv(normalize(gym.make('InvertedPendulum-v2')))
            action_noise = OUStrategy(env.spec, sigma=0.2)
            policy = ContinuousMLPPolicy(env_spec=env.spec,
                                         hidden_sizes=[64, 64],
                                         hidden_nonlinearity=tf.nn.relu,
                                         output_nonlinearity=tf.nn.tanh)
            qf = ContinuousMLPQFunction(env_spec=env.spec,
                                        hidden_sizes=[64, 64],
                                        hidden_nonlinearity=tf.nn.relu)
            replay_buffer = SimpleReplayBuffer(env_spec=env.spec,
                                               size_in_transitions=int(1e6),
                                               time_horizon=100)
            algo = DDPG(
                env_spec=env.spec,
                policy=policy,
                policy_lr=1e-4,
                qf_lr=1e-3,
                qf=qf,
                replay_buffer=replay_buffer,
                steps_per_epoch=20,
                target_update_tau=1e-2,
                n_train_steps=50,
                discount=0.9,
                policy_weight_decay=0.01,
                qf_weight_decay=0.01,
                min_buffer_size=int(5e3),
                exploration_strategy=action_noise,
            )
            runner.setup(algo, env)
            last_avg_ret = runner.train(n_epochs=10, batch_size=100)
            assert last_avg_ret > 10

            env.close()
