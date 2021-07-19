import numpy as np
import pytest

# import fastlmmclib  #!!!cmk
# import fastlmmclib.quadform
# import fastlmmclib.quadform.qfc_src
# from fastlmmclib.quadform import qf

# from fastlmmclib.quadform.qfc_src import wrap_qfc

from fastlmmclib.quadform.qfc_src import wrap_qfc


def qf(
    chi2val, coeffs, dof=None, noncentrality=None, sigma=0.0, lim=1000000, acc=1e-08
):
    size = coeffs.shape[0]
    if dof is None:
        dof = np.ones(size, dtype="int32")
        # dof = np.ones(size)
    if noncentrality is None:
        noncentrality = np.zeros(size)
    ifault = np.zeros(1, dtype="int32")
    # ifault=np.zeros(1)
    trace = np.zeros(7)
    # import pdb
    # pdb.set_trace()
    pval = 1.0 - wrap_qfc.qf(
        coeffs, noncentrality, dof, sigma, chi2val, lim, acc, trace, ifault
    )
    return pval, ifault[0], trace


def test_fastlmm_qf():

    eigvals = np.array(
        [
            -6.70841876e-17,
            -5.45265380e-17,
            -2.07429851e-17,
            -3.44770228e-18,
            1.54965877e-17,
            5.22613549e-17,
            4.83909990e-02,
            6.78210272e-02,
            6.98070165e-02,
            7.49885957e-02,
            7.72718890e-02,
            8.72241662e-02,
            9.62501298e-02,
            9.94424065e-02,
            1.05623694e-01,
            1.14926555e-01,
            1.19339175e-01,
            1.25504071e-01,
            1.33332067e-01,
            1.39187986e-01,
            1.42728527e-01,
            1.49490634e-01,
            1.52729644e-01,
            1.58097935e-01,
            1.65987006e-01,
            1.74407521e-01,
            1.84012545e-01,
            1.88030717e-01,
            1.99181157e-01,
            2.00686888e-01,
            2.11451277e-01,
            2.13573052e-01,
            2.19022591e-01,
            2.24772973e-01,
            2.25593701e-01,
            2.28123848e-01,
            2.39433779e-01,
            2.47287309e-01,
            2.61836400e-01,
            2.68403814e-01,
            2.79255589e-01,
            2.83999403e-01,
            3.02121968e-01,
            3.13476780e-01,
            3.17985473e-01,
            3.45773300e-01,
            3.62616345e-01,
            3.75628936e-01,
            4.02637783e-01,
            4.34439331e-01,
            4.37458184e-01,
            4.46547799e-01,
            5.22536033e-01,
            5.58473237e-01,
        ]
    )
    result = qf(11.756721115473242, eigvals, acc=1e-7)
    print(result[0] - 0.321640468662588)
    assert np.abs(result[0] - 0.32164046866258) < 1e-12


if __name__ == "__main__":

    pytest.main([__file__])
