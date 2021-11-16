import random as r


def RC4(n, M, K=r.sample(range(10000000), k=60)):

    def ksa(K):
        S = [i for i in range(M)]
        l = len(K)
        j = 0
        for i in range(M):
            j = (j + S[i] + K[i % l]) % M
            S[i], S[j] = S[j], S[i]
        return S

    def prga(r, M, S):
        x = []
        i, j = 0, 0
        for _ in range(n):
            i = (i + 1) % M
            j = (j + S[i]) % M
            S[i], S[j] = S[j], S[i]
            x.append(S[(S[i] + S[j]) % M])
        return x

    return prga(r, M, ksa(K))


if __name__ == '__main__':
    print(RC4(10, 100))
