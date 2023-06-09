import tensorflow as tf

def adam(loss, lr, train_vars, beta_1=0.9, beta_2=0.999, epsilon=1e-8):
    opt = tf.optimizers.Adam(
    learning_rate=lr,
    beta_1=beta_1,
    beta_2=beta_2,
    epsilon=epsilon,
    name="Adam"
    )
    grads_and_vars = opt.get_gradients(loss, train_vars)
    apply_gradient_op = opt.apply_gradients(grads_and_vars)
    return apply_gradient_op, grads_and_vars

def adam_clipping(loss, lr, train_vars, beta_1=0.9, beta_2=0.999,
    epsilon=1e-8, clip_norm=5.0):
    grads, _ = tf.clip_by_global_norm(tf.gradients(loss, train_vars),
    clip_norm)
    capped_gvs = list(zip(grads, train_vars))
    opt = tf.optimizers.Adam(
    learning_rate=lr,
    beta_1=beta_1,
    beta_2=beta_2,
    epsilon=epsilon,
    name="Adam"
    )
    apply_gradient_op = opt.apply_gradients(capped_gvs)
    return apply_gradient_op, capped_gvs

def adam_clipping_list_lr(loss, list_lrs, list_train_vars,
    beta_1=0.9, beta_2=0.999,
    epsilon=1e-8, clip_norm=5.0):
    assert len(list_lrs) == len(list_train_vars)
    train_vars = []
    for v in list_train_vars:
        if len(train_vars) == 0:
            train_vars = list(v)
        else:
            train_vars.extend(v)

    grads, _ = tf.clip_by_global_norm(tf.gradients(loss, train_vars),
                                    clip_norm)

    offset = 0
    apply_gradient_ops = []
    grads_and_vars = []
    for i, v in enumerate(list_train_vars):
        g = grads[offset:offset+len(v)]
        opt = tf.optimizers.Adam(
            learning_rate=list_lrs[i],
            beta_1=beta_1,
            beta_2=beta_2,
            epsilon=epsilon,
            name="Adam"
        )
        gvs = list(zip(g, v))
        apply_gradient_op = opt.apply_gradients(gvs)

        apply_gradient_ops.append(apply_gradient_op)
        if len(grads_and_vars) == 0:
            grads_and_vars = list(gvs)
        else:
            grads_and_vars.extend(gvs)
        offset += len(v)

    apply_gradient_ops = tf.group(*apply_gradient_ops)
    return apply_gradient_ops, grads_and_vars
