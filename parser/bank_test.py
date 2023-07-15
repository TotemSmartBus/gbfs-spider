import sys
from functools import cmp_to_key


def prepare():
    n = int(sys.stdin.readline().strip())
    lines = []
    infos = []
    for i in range(n):
        line = sys.stdin.readline().strip()
        lines.append(line)
        info = {}
        strs = line.split(' ')
        info['line'] = line
        info['ori_name'] = strs[0]
        if strs[0] == '?':
            info['name'] = 'zzzzzzzzzzz'
        else:
            info['name'] = strs[0]
        if strs[4] != '?':
            info['sum'] = int(strs[4])
        else:
            sum = 0
            info['sum'] = 0
            info['grade'] = []
            for j in range(1, 4):
                # info['grade'].append(strs[j])
                if strs[j] == '?':
                    info['sum'] = -1
                    break
                info['sum'] += int(strs[j])
        info['grade'] = list(strs[1:4])
        infos.append(info)
    # print(infos)
    infos.sort(key=cmp_to_key(cmp))
    # print(infos)
    for info in infos:
        refine(info)
    # print(infos)
    output(n, infos)


def cmp(a, b):
    if int(a['sum']) > int(b['sum']):
        return -1
    if int(a['sum']) < int(b['sum']):
        return 1
    if int(a['sum']) == int(b['sum']):
        if a['name'] >= b['name']:
            return 1
        return -1


def refine(info):
    if info['sum'] != -1 and '?' in info['grade']:
        g = info['grade']
        cnt = 0
        for i in range(3):
            if g[i] == '?':
                cnt += 1
        if cnt == 1:
            j = -1
            grade = info['sum']
            for i in range(3):
                if g[i] != '?':
                    grade -= int(g[i])
                else:
                    j = i
            g[j] = str(grade)
    if info['sum'] == -1:
        info['sum'] = '?'


def output(n, infos):
    for i in range(n):
        print(infos[i]['ori_name'], infos[i]['grade'][0], infos[i]['grade'][1], infos[i]['grade'][2], str(infos[i]['sum']))


if __name__ == '__main__':
    # print('12' < '9')
    prepare()
    # s1 = 'aaa'
    # s2 = 'bbb'
    # print(s1, s2)
