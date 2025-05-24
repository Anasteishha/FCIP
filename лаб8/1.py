class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def inverse_mod(self, x):
        x = x % self.p
        for i in range(1, self.p):
            if (x * i) % self.p == 1:
                return i
        return None

    def point_add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        if P == Q:
            return self.point_double(P)
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and (y1 != y2 or y1 == 0):
            return None
        denom = (x2 - x1) % self.p
        inv_denom = self.inverse_mod(denom)
        if inv_denom is None:
            return None
        lamb = ((y2 - y1) * inv_denom) % self.p
        x3 = (lamb**2 - x1 - x2) % self.p
        y3 = (lamb * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def point_double(self, P):
        if P is None:
            return None
        x, y = P
        if y == 0:
            return None
        denom = (2 * y) % self.p
        inv_denom = self.inverse_mod(denom)
        if inv_denom is None:
            return None
        lamb = ((3 * x**2 + self.a) * inv_denom) % self.p
        x3 = (lamb**2 - 2 * x) % self.p
        y3 = (lamb * (x - x3) - y) % self.p
        return (x3, y3)

    def scalar_mult(self, k, P):
        R = None
        Q = P
        while k:
            if k & 1:
                R = self.point_add(R, Q)
            Q = self.point_double(Q)
            k >>= 1
        return R

    def point_inverse(self, P):
        if P is None:
            return None
        x, y = P
        return (x, (-y) % self.p)

# Параметри 
curve = EllipticCurve(a=19, b=16, p=16)
P = (6, 9)
Q = (20 % 16, 9) 

print("P + Q =", curve.point_add(P, Q))
print("2P =", curve.point_double(P))
print("3P =", curve.scalar_mult(3, P))
print("-P =", curve.point_inverse(P))
