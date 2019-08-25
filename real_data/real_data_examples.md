Real Data Examples with brian2modelfitting
==========================================

This gist showcases the examples of real data optimization with use of model fitting.

Data Source
-----------

Recorded data was provided by prof. Romain Brette and recorded at http://www.computational-neuroscience-of-sensory-systems.org/.

Used code
---------

In the following files, I have still used old, non object oriented version of the code. To re-create the examples, please adapt the code by changing:

~~~python
res, error = fit_traces(model=model, input_var='I', output_var='v',
                        input=input_cur * amp, output=output * volt, dt=dt,
                        method='exponential_euler',
                        callback=callback,
                        EL=[-50*mV, -10*mV],
                        C=[100*pF, 400*pF],
                        gL=[7*nS, 20*nS],                        
                        kn=[5*mV, 20*mV],
                        Vn=[-20*mV, 20*mV],
                        Ek=[-100*mV, 0*mV],
                        g_k=[1e-1*uS, 1e4*uS],
                        taun=[1*ms, 40*ms],
                        param_init={'v': -30 * mV},
                        n_rounds=55, n_samples=30, optimizer=n_opt, metric=metric)
~~~

To a new version, in accordance to rest of documentation:

~~~python
fitter = TraceFitter(...)
fitter.fit(...)

fitter.generate()
~~~


Workload
--------

Following notebooks, required loading the data with
use of clampy software (https://github.com/romainbrette/clampy), development of the suggested models and plenty of testing of ranges of parameters and possible optimization methods.
