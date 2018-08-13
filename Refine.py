import triangle as tri

def area(A, B, C):
    return abs(A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1])) / 2

def refine1(t, k):
    t['triangle_max_area'] = []
    m = 0
    for i in range(len(t['triangles'])):
        a = t['triangles'][i][0]
        b = t['triangles'][i][1]
        c = t['triangles'][i][2]
        min_thick = min(t['thick1'][a], t['thick1'][b], t['thick1'][c], t['mid_thick'][i])
        max_thick = max(t['thick1'][a], t['thick1'][b], t['thick1'][c], t['mid_thick'][i])
        if area(t['vertices'][a], t['vertices'][b], t['vertices'][c]) > k * min_thick ** 2:
            m = 1
            new_area = min(area(t['vertices'][a], t['vertices'][b], t['vertices'][c]) * 0.99, k * max_thick ** 2)
            t['triangle_max_area'].append(new_area)
        else:
            t['triangle_max_area'].append(-1)
    if m == 1:
        t = tri.triangulate(t, 'Drpq30a')
    return t, m

def refine2(t, k, d):
    t['triangle_max_area'] = []
    m = 0
    for triangle in t['triangles']:
        a = triangle[0]
        b = triangle[1]
        c = triangle[2]
        v = t['vertices']
        max_thick = max(t['thick1'][a], t['thick1'][b], t['thick1'][c])
        min_thick = min(t['thick1'][a], t['thick1'][b], t['thick1'][c])
        diff_y = max(v[a][1], v[b][1], v[c][1]) - min(v[a][1], v[b][1], v[c][1])
        if ((max_thick / min_thick >= k and k > 0) or (max_thick - min_thick >= d and d > 0)) and diff_y > 10:
            m = 1
            t['triangle_max_area'].append(area(t['vertices'][a], t['vertices'][b], t['vertices'][c]) * 0.99)
        else:
            t['triangle_max_area'].append(-1)
    if m == 1:
        t = tri.triangulate(t, 'Drpq30a')
    return t, m

def refine3(t, k, d):
    t['triangle_max_area'] = []
    m = 0
    for i in range(len(t['triangles'])):
        a = t['triangles'][i][0]
        b = t['triangles'][i][1]
        c = t['triangles'][i][2]
        v = t['vertices']
        ave_thick = (t['thick1'][a] + t['thick1'][b] + t['thick1'][c]) / 3
        diff_y = max(v[a][1], v[b][1], v[c][1]) - min(v[a][1], v[b][1], v[c][1])
        if (t['mid_thick'][i] > k * ave_thick or t['mid_thick'][i] < ave_thick / k or abs(t['mid_thick'][i] - ave_thick) > d) and diff_y > 10:
            m = 1
            t['triangle_max_area'].append(area(t['vertices'][a], t['vertices'][b], t['vertices'][c]) * 0.99)
        else:
            t['triangle_max_area'].append(-1)
    if m == 1:
        t = tri.triangulate(t, 'Drpq30a')
    return t, m
