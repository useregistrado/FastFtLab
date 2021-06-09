def monitor(a,b,c):
    sa,sb = sum(a), sum(b)
    cs = len(a)*100 #counter squares
    ca = c*cs #count area
    cn = sa+sb #counts
    rhom = ((sa/ca)+(sb/ca))/2 #rho monitor
    return "{0:.4f}".format(rhom), cn
