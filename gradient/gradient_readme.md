Gradient Optimization for brian2modelfitting
============================================

Following gist describes work done for adding gradient based optimization to brian2modelfitting toolbox.

General idea
------------
brian2modelfitting uses global optimization methods in order to avoid getting stuck in local minima, by using gradient-free methods of optimization. To improve the results, we decided to investigate the possibility of integration of local optimization with use of gradient based method.

Main idea included usage of local sensitivity to solve the local optimization. For that we have to calculate additional differential equations, that need to be run in parallel with models equations. Equations can be obtained for each of the variables with use of a ```get_sensitivity_equations()``` and are described in next file.


Two approaches were investigated:
---------------------------------

1. basin hoppin - algorithm that performs both global and local optimization

2. local gradient optimization - to be used as `polish` step at the end of global optimization (or each round of the global optimization)


Local gradient optimization was tested for up to two parameters with use of ```scipy.minimize()```:

  - automatically calculated gradients, where we provide our error as output
  - local sensitivity equations as gradients calculated manually and plugged alongside with the error into ```minimize()```

Additionally, the resulting from local sensitivity equations gradient fields have been calculated for ranges around the goal value and visualized.

How it works
------------

We calculate additional equations for evaluated parameters with ```get_sensitivity_equations``` and add them to the model that is going to be evaluated:

~~~python
new_eqs = get_sensitivity_equations(group, para['gl', 'g_na', 'g_kd'])
model = model_eqs + new_eqs
~~~

We need to define the function that is going to be optimized, and returns the error ``E`` for given parameters:
~~~python
minimize(eval_neurons, [8, 18], method='BFGS', jac=False)
~~~
where: ```range=[8, 18]``` and ```method``` can be chosen

To use the local sensitivity calculations, ```eval_neurons``` has to return error ``E`` and gradient over the parameter ``dEdp``
~~~python
minimize(eval_neurons, [8, 18], method='BFGS', jac=True)
~~~
