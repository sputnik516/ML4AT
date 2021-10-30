from scipy.stats import anderson, shapiro, normaltest, kurtosistest, skewtest
from statsmodels.graphics.gofplots import qqplot
from matplotlib import pyplot


ALPHA = 0.05


def qqplot_wrapper(data):
    qqplot(data)
    pyplot.show()


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


def skewtest_wrapper(data, alpha=ALPHA):
    res = skewtest(data)[1] > alpha
    if res:
        print('Skewness of the population that the sample was drawn from is the same as that of a corresponding normal '
              'distribution. (fail to reject H0)')
    else:
        print('Skewness of the population that the sample was drawn from is NOT the same as that of a corresponding '
              'normal distribution. (reject H0)')
    return res
