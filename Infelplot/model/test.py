import stadistic_scripts as st
x = [0,0.5,1,1.4,2.1,2.5]
y = [0.1,0.5,1.4,1.5,1.9,2.5]

m=st.regression(xi=x,yi=y)
print(m)
