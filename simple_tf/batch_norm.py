from simple_tf.global_params import GlobalConstants

import tensorflow as tf


def batch_norm(x, network, node, decay, iteration, is_decision_phase, is_training_phase):
    gamma_name = network.get_variable_name(node=node, name="gamma")
    beta_name = network.get_variable_name(node=node, name="beta")
    pop_mean_name = network.get_variable_name(node=node, name="pop_mean")
    pop_var_name = network.get_variable_name(node=node, name="pop_var")
    if GlobalConstants.USE_TRAINABLE_PARAMS_WITH_BATCH_NORM:
        gamma = tf.Variable(name=gamma_name, initial_value=tf.ones([x.get_shape()[-1]]))
        beta = tf.Variable(name=beta_name, initial_value=tf.zeros([x.get_shape()[-1]]))
    else:
        gamma = None
        beta = None
    batch_mean, batch_var = tf.nn.moments(x, [0])
    pop_mean = tf.Variable(name=pop_mean_name, initial_value=tf.constant(0.0, shape=[x.get_shape()[-1]]), trainable=False)
    pop_var = tf.Variable(name=pop_var_name, initial_value=tf.constant(0.0, shape=[x.get_shape()[-1]]), trainable=False)
    new_mean = tf.where(iteration > 0, is_decision_phase * (decay * pop_mean + (1.0 - decay) * batch_mean) +
                        (1.0 - is_decision_phase) * pop_mean, batch_mean)
    new_var = tf.where(iteration > 0, is_decision_phase * (decay * pop_var + (1.0 - decay) * batch_var) +
                       (1.0 - is_decision_phase) * pop_var, batch_var)
    pop_mean_assign_op = tf.assign(pop_mean, new_mean)
    pop_var_assign_op = tf.assign(pop_var, new_var)

    def get_population_moments_with_update():
        with tf.control_dependencies([pop_mean_assign_op, pop_var_assign_op]):
            return tf.identity(batch_mean), tf.identity(batch_var)

    final_mean, final_var = tf.cond(is_training_phase > 0,
                                    get_population_moments_with_update,
                                    lambda: (tf.identity(pop_mean), tf.identity(pop_var)))

    normed = tf.nn.batch_normalization(x=x, mean=final_mean, variance=final_var, offset=beta, scale=gamma,
                                       variance_epsilon=1e-5)

    return normed
    # return normed, final_mean, final_var, batch_mean, batch_var