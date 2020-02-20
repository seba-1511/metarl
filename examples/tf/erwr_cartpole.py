#!/usr/bin/env python3
"""This is an example to train a task with ERWR algorithm.

Here it runs CartpoleEnv on ERWR with 100 iterations.

Results:
    AverageReturn: 100
    RiseTime: itr 34
"""
from metarl import wrap_experiment
from metarl.experiment.deterministic import set_seed
from metarl.np.baselines import LinearFeatureBaseline
from metarl.tf.algos import ERWR
from metarl.tf.envs import TfEnv
from metarl.tf.experiment import LocalTFRunner
from metarl.tf.policies import CategoricalMLPPolicy


@wrap_experiment
def erwr_cartpole(ctxt=None, seed=1):
    """Train with ERWR on CartPole-v1 environment.

    Args:
        ctxt (metarl.experiment.ExperimentContext): The experiment
            configuration used by LocalRunner to create the snapshotter.
        seed (int): Used to seed the random number generator to produce
            determinism.

    """
    set_seed(seed)
    with LocalTFRunner(snapshot_config=ctxt) as runner:
        env = TfEnv(env_name='CartPole-v1')

        policy = CategoricalMLPPolicy(name='policy',
                                      env_spec=env.spec,
                                      hidden_sizes=(32, 32))

        baseline = LinearFeatureBaseline(env_spec=env.spec)

        algo = ERWR(env_spec=env.spec,
                    policy=policy,
                    baseline=baseline,
                    max_path_length=100,
                    discount=0.99)

        runner.setup(algo=algo, env=env)

        runner.train(n_epochs=100, batch_size=10000, plot=False)


erwr_cartpole(seed=1)