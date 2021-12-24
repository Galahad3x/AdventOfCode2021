import re

from rtree import index

p = index.Property()
p.dimension = 3
ix = index.Index(properties=p)

def volume(cuboids):
    return sum((
        (x2-x1)*(y2-y1)*(z2-z1)
        for (x1,y1,z1, x2,y2,z2) in cuboids
    ))

def is_empty(c):
    (x1,y1,z1, x2,y2,z2) = c
    return x1 == x2 or y1 == y2 or z1 == z2

def intersects1d(c, d):
    (c1, c2), (d1, d2) = c, d
    return (c2 > d1 and d2 > c1)

def intersects(c, d):
    (cx1,cy1,cz1, cx2,cy2,cz2) = c
    (dx1,dy1,dz1, dx2,dy2,dz2) = d

    return (
        intersects1d((cx1,cx2), (dx1,dx2))
        and intersects1d((cy1,cy2), (dy1,dy2))
        and intersects1d((cz1,cz2), (dz1,dz2))
    )

# Return a list of up to six cuboids representing
# the difference (c - d)
def subtract(c, d):
    (cx1,cy1,cz1, cx2,cy2,cz2) = c
    (dx1,dy1,dz1, dx2,dy2,dz2) = d

    if not intersects(c, d):
        return [c]

    # Clip d to the bounds of c
    (dx1,dy1,dz1, dx2,dy2,dz2) = (
        max(cx1,dx1), max(cy1,dy1), max(cz1,dz1),
        min(cx2,dx2), min(cy2,dy2), min(cz2,dz2)
    )

    cuboids = [
        (cx1,cy1,cz1, cx2,cy2,dz1),
        (cx1,cy1,dz2, cx2,cy2,cz2),
        (dx1,cy1,dz1, cx2,dy1,dz2),
        (dx2,dy1,dz1, cx2,cy2,dz2),
        (cx1,dy2,dz1, dx2,cy2,dz2),
        (cx1,cy1,dz1, dx1,dy2,dz2),
    ]

    return [
        cuboid for cuboid in cuboids if not is_empty(cuboid)
    ]

def difference(cs, ds):
    for d in ds:
        cs = sum([ subtract(c, d) for c in cs ], [])
    return cs

total = 0
cuboids = []

for line in reversed(list(open("input.txt", "r"))):
    mo = re.match(r"^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)", line)
    on_off, *coords = mo.groups()
    x1,x2, y1,y2, z1,z2 = map(int, coords)
    cuboid = (x1,y1,z1, x2+1,y2+1,z2+1)
    if on_off == "on":
        total += volume(difference([cuboid], [ cuboids[i] for i in ix.intersection(cuboid) ]))
    ix.insert(len(cuboids), cuboid)
    cuboids.append(cuboid)

print(total)