from matplotlib import rcParams
import matplotlib.pyplot as plt
from pyRadialPlot import radialplot
from io import BytesIO
import base64

def radialp(file,transform='linear'):
    rcParams["figure.dpi"] = 300
    ax = radialplot(file=file, transform=transform)
    plt.axes = ax
    tmpfile=BytesIO()
    plt.savefig(tmpfile,format="png")
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return encoded
