import numpy as np

from scipy.stats import chisquare
from scipy.stats.distributions import chi2
   
# Sample usage: 
# python  scripts_learn/simple_chi_square_example.py 


# Załóżmy, że mamy pudełka 0,1,2,3,4 i policzyliśmy, że
# w pudełku i-tym powinno średnio być n*p_i obserwacji
# bins_expect = [n*p_0,n*p_1, n*p_2, n*p_3, n*p_4]

bins_expect = np.array([15.0, 20.0, 25.0, 20.0, 20.0])

# z drugiej strony zaobserwowalismy:
bins_observed = np.array([25.0, 21.0, 24.0, 17.0, 13.0])

print("bins_expect = ", bins_expect)
print("bins_observed = ", bins_observed)

print("chi2_points from scipy : ", chisquare(bins_observed,bins_expect))

# jak chcemy wydobyc liczby, to po prostu:
chi_square_stat, p_value = chisquare(bins_observed,bins_expect)

print("Czyli: chi_square_stat = ", chi_square_stat, ", p-value = ", p_value)
print("\n")
print("A znajac wart. stat. oraz liczbe stopni swobody:")
deg_of_freedom = len(bins_expect)-1
print("p-wartosc = ", chi2.sf(chi_square_stat,deg_of_freedom))
