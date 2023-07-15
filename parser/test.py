def test1():
    n, m = (int(x) for x in input().split(','))
# print(n)
# print(m)
    a = [int(x) for x in input().split(',')]
    # for x in input().split(' '):
    #     a.append(int(x))

    q = [int(x) for x in input().split(',')]
    a.sort()
    # print(a)
    # print(q)
    res = []
    for i in range(m):
        cnt = 0
        weight = 0
        j = 0
        while weight <= q[i] and j < n:
            weight += a[j] * a[j]
            cnt += 1
            j += 1
        if weight > q[i]:
            cnt -= 1
        res.append(cnt)
        i += 1
# print((i for i in res), end=' ')
    for r in res:
        print(str(r), end=' ')


def test2():
    s = input()[0: -1]
    ss = s.split(';')
    d = {}
    for sss in ss:
        ssss = sss.split('=')
        d[ssss[0]] = ssss[1]
    # print(d)
    # dd = list(reversed(d))
    # print(dd)
    q = int(input())
    res = []
    for i in range(q):
        r = d.get(input())
        if r is None:
            res.append('EMPTY')
        else:
            res.append(r)
    for x in res:
        print(x)


def test3():
    n = int(input())
    a = [int(x) for x in input().split(' ')]
    i = 0
    j = 0
    sum = 0
    res = 0
    for x in a:
        sum += x
    if sum % 2 != 0:
        print(res)
    else:
        cur_sum = 0
        while j < n - 1:
            cur_sum += a[j]
            if cur_sum >= sum / 2:
                if cur_sum == sum / 2:
                    res += 1
                cur_sum -= a[i]
                i += 1
            j += 1
        print(res)


if __name__ == '__main__':
    # test2()
    # test1()
    test3()
