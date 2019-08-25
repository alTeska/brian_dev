import numpy as np
from brian2 import *
from sympy import *
from brian2.units.fundamentalunits import DIMENSIONLESS
from tqdm import tqdm

def get_sensitivity_equations(group, parameters):
    eqs = group.equations
    diff_eqs = eqs.get_substituted_expressions(group.variables)
    diff_eq_names = [name for name, _ in diff_eqs]

    system = Matrix([diff_eq[1] for diff_eq in diff_eqs])
    J = system.jacobian(diff_eq_names)

    sensitivity = []
    sensitivity_names = []
    for parameter in parameters:
        F = system.jacobian([parameter])
        names = ['S_{}_{}'.format(diff_eq_name, parameter)
                 for diff_eq_name in diff_eq_names]
        sensitivity.append(J * Matrix(names) + F)
        sensitivity_names.append(names)

    new_eqs = []
    for names, sensitivity_eqs, param in zip(sensitivity_names, sensitivity, parameters):
        for name, eq, orig_var in zip(names, sensitivity_eqs, diff_eq_names):
            unit = eqs[orig_var].dim / group.namespace[parameter].dim
            new_eqs.append('d{lhs}/dt = {rhs} : {unit}'.format(lhs=name,
                                                           rhs=eq,
                                                           unit=repr(unit) if unit is not DIMENSIONLESS else '1'))
    new_eqs = Equations('\n'.join(new_eqs))
    return new_eqs


def eval_neurons(param):
    # init neurons
    start_scope()
    neurons = NeuronGroup(1, model, method='exponential_euler',)
    neurons.namespace['output_var'] = output_traces
    neurons.namespace['Nsteps'] = Nsteps
    neurons.namespace['Ntraces'] = Ntraces
    neurons.namespace['t_start'] = t_start

    # set new parameters
    state = {'gl': param*nS, 'g_na': 20 * uS, 'g_kd': 6 * uS}
    neurons.set_states(state)

    # run simulation
    neurons.I = '1*nA'
    neurons.v = El
    mon = StateMonitor(neurons, ['v', 'S_v_gl','S_v_g_na', 'S_v_g_kd' ], record=True)
    run(20*ms)

    # get traces
    v_trace = mon.v[0]
    svgl = mon.S_v_gl[0]
    svgkd = mon.S_v_g_kd[0]
    svgna = mon.S_v_g_na[0]

    # analyze results
    dSdp = svgl # svgkd + svgna
    data = output[0]

    E = np.sum(np.square(data - v_trace))/Nsteps /250
    dEdp = np.sum(2 * dSdp * (v_trace - data)) / Nsteps

    return E / mV**2, dEdp  / (mV**2/nS)
