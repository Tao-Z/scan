def plot(ax, **tri):
    for triangle in tri['triangles']:
        x = [tri['vertices'][j][0] for j in triangle]
        y = [tri['vertices'][j][1] for j in triangle]
        x.append(tri['vertices'][triangle[0]][0])
        y.append(tri['vertices'][triangle[0]][1])
        ax.plot(x, y, 'k-')

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    t={'vertices':[[0, 0], [5, 0], [0, 5], [5, 5], [2.5, 8]], 'triangles':[[0, 1, 2], [1, 2, 3], [2, 3, 4]]}
    ax = plt.subplot(aspect = 'equal')
    plot(ax, **t)
    plt.show()
