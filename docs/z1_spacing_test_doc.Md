# Spacing Test
## Algorithm
Spacing test performs series of operations on sequence of numbers $U_1,... U_n$ in range $[0,1]$ in order to test the hypothesis, that they are random sample from standard uniform distribution.

Let's assume that $U_1,...U_n$ are independent random variables from uniform distribution with pdf:
$$f(x) = I_{[0,1]}$$

Now we need to choose any interval $I = (\alpha, \beta) \subset [0,1]$ of width $\delta$.
In the first step of algorithm we will calculate numbers reffered to as "spacings" defined in the following way:

$$C_1 = min\{i \geq 0 : U_{i+1} \in I\}$$
$$C_{j+1} = min\{i \geq 0 : U_{C_j + 1 + i} \in I\}$$

Intuitively, we mark all occurences of $U_j$ that fits into interval $I$ and then write down number of unmarked numbers between them. $C_1$ is 1 less than index of first number that fits in $I$. We end up with sequence $C_1, ... C_k$.

**Under the null hypothesis, spacings are geometrically distributed**, e.g. for $i = 1, ... k$ $$P(C_i = y) = \delta(1 - \delta)^y$$

Now we define another variable indicating how many occurences of specific value of $C_i$ we observed - for values $y$ less than number $s$ we have $O_y = \#\{i: C_i = y\}$ and for $y \geq s$ let $O_y = \#\{i: C_i \geq s\}$. It is recommended to take
$$s \geq max\{5, \frac{5(1-\delta)}{\delta}\}$$

We will test the distribution ofIt can be shown that under the null hypothesis expected value $E[O_i] = kp_i$

where $p_i = \delta(1 - \delta)^i$ for $i = 0, ... s-1$ and $p_s = \sum_{i=0}^{s-1}{p_i}$.

The last step is to compute the $\chi^2$ statistic based on sequence $O_i$ which is:
$$\chi^2 = \sum_{i=0}^{s}{\frac{(O_i - kp_i)^2}{kp_i}}$$

and find it's p-value with $s$ degrees of freedom. 

**If p-value of computed statistic is smaller than the predeterminate significance level, we can reject the null (randomness) hypothesis.**




### Example
## How to use script?
### Input
- `input_file`: path to a file containing a dictionary-like object with at least the following keys:
    - **"numbers"**: sequence of n integers (they will be mapped to numbers in range [0,1]). 
    - **"int_range"**: maximum theorethically possible value of generated numbers (the highest number doesn't have to occur when numbers are "randomly" generated, so it's impossible to guess what was the range and thus we cannot tell in such case how well generator works).
- `output_file`: path to output file (safe to use .txt); if provided, summary of test in form of dictionary with the following keys: "test", "input_file", "alpha", "delta", "result" will overwrite contents of this file.
- `alpha`: number in range (0,1) indicating the beginning of test's interval (default: 0)
- `delta`: number in range (0, 1 - `alpha`) indicating width of test's interval (default: 0.5)

### Output
**p-value** of a test printed in console next to info about tested numbers and running time.

### Examples
```
python scripts/z1_spacing_test.py --input-file 'results/mt_numbers_int.pkl'

python scripts/z1_spacing_test.py --input-file 'results/z1_XORG_numbers_int.pkl --output-file 'test_results/spacing_XORG.txt' --alpha 0.2 --delta 0.4'
```

## Test results
TODO