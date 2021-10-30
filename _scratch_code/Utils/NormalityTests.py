import numpy as np
from scipy.stats import anderson, shapiro, normaltest, kurtosistest, skewtest, skew
from scipy.stats import norm
from statsmodels.graphics.gofplots import qqplot
from matplotlib import pyplot as plt


ALPHA = 0.05


def qqplot_wrapper(data):
    qqplot(data)
    plt.show()


def histogram_data_vs_norm_wrapper(data, n_bins=False):
    """
    Source: https://stackoverflow.com/questions/33174249/matplotlib-overlay-a-normal-distribution-with-stddev-axis-onto-another-plot
    :param n_bins:
    :param data:
    :return:
    """
    if not n_bins:
        # n_bins = int(np.sqrt(len(data)))
        n_bins = int(len(data)/3)
    h = sorted(data)
    hmean = np.mean(h)
    hstd = np.std(h)
    h_n = (h - hmean) / hstd
    pdf = norm.pdf( h_n )

    # plot data
    f,ax1 = plt.subplots()

    ax1.hist( h_n, n_bins, density=True, stacked=True)
    ax1.plot( h_n , pdf, lw=3, c='r')
    ax1.set_xlim( [h_n.min(), h_n.max()] )
    ax1.set_xlabel( r'$\sigma$' )
    ax1.set_ylabel( r'Relative Frequency')

    ax2 = ax1.twiny()
    ax2.grid( False )
    ax2.set_xlim( ax1.get_xlim() )
    ax2.set_ylim( ax1.get_ylim() )


def shapiro_wrapper(data, alpha=ALPHA):
    stat, p = shapiro(data)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    if p > alpha:
        print('Sample looks Gaussian (fail to reject H0)')
        return True
    else:
        print('Sample does not look Gaussian (reject H0)')
        return False


def dogostinos_wrapper(data, alpha=ALPHA):
    stat, p = normaltest(data)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    if p > alpha:
        print('Sample looks Gaussian (fail to reject H0)')
        return True
    else:
        print('Sample does not look Gaussian (reject H0)')
        return False


def anderson_wrapper(data):
    result = anderson(data)
    fail_to_rej_H0 = True
    for i in range(len(result.critical_values)):
        sl, cv = result.significance_level[i], result.critical_values[i]
        if result.statistic < result.critical_values[i]:
            print('%.3f: %.3f, data looks normal (fail to reject H0)' % (sl, cv))
        else:
            print('%.3f: %.3f, data does not look normal (reject H0)' % (sl, cv))
            fail_to_rej_H0 = False
    return fail_to_rej_H0


def kurtosistest_wrapper(data, alpha=ALPHA):
    res = kurtosistest(data)[1] > alpha
    if res:
        print('Kurtosis of the population from which the sample was drawn is that of the normal distribution '
              '(fail to reject H0)')
    else:
        print('Kurtosis of the population from which the sample was drawn is NOT of the normal distribution '
              '(reject H0)')
    return res


def skewtest_wrapper(data, alpha=ALPHA, threshold=0.2):
    res = skewtest(data)[1] > alpha
    if res:
        print('Skewness of the population that the sample was drawn from is the same as that of a corresponding normal '
              'distribution. (fail to reject H0)')
    else:
        print('Skewness of the population that the sample was drawn from is NOT the same as that of a corresponding '
              'normal distribution. (reject H0)')

    skew_val = skew(data)
    print("Skew value: {}; threshold: {}".format(skew_val, threshold))
    if skew_val > threshold:
        print("More weight in the left tail of the distribution")
    elif skew_val < -threshold:
        print("More weight in the right tail of the distribution")
    else:
        print("Distribution is approximately symmetric")
    return res

