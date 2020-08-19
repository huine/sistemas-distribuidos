import ehprimo
from timeit import default_timer

alg = ['alg1', 'alg2', 'alg3', 'alg4']
saida = []
for f in alg:
    for num in [7, 27, 8421, 13033, 524287, 664283, 2147483647]:
        print('alg: {0} num: {1}'.format(f, num))
        tmp = []
        primo = 0
        for r in range(30):
            print('iter: {0}'.format(r))
            func = getattr(ehprimo, f, None)
            start = default_timer()
            primo = func(num)
            tmp.append(default_timer() - start)

        saida.append(
            {
                'alg': f,
                'primo': primo,
                'num': num,
                'tempo': '%.5f ms' % (1000 * (sum(tmp) / 30.0))
            }
        )

with open('saida.txt', 'w') as file:
    for item in saida:
        file.writelines(str(item) + '\r\n')
    file.close()