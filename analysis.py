import json
import pylab
import numpy
import matplotlib
matplotlib.use("AGG")

with open('rates.json') as json_data:
    ratedata = json.load(json_data)
    json_data.close()
    
"""
data looks like this:
    "Option 9": {
        "Deductible": 3000,
        "Out-of-pocket max": 13300,
        "Co-insurance": 0.30,
        "Premium": 1250, 
        "Veracity": 1
"""

veracitycontribution = 750
spa_rebate = 100
mygraycolor = ( 0.95, 0.95, 0.95 )
minor_locator = matplotlib.ticker.AutoMinorLocator(5)

totals = {}
services = numpy.array(range(1,60000))
for option in ratedata:
    if ratedata[option]['Veracity'] == 1:
        prem = (ratedata[option]['Premium']-veracitycontribution)*12
    elif ratedata[option]['SPA'] == 0:
        prem = (ratedata[option]['Premium']-spa_rebate)*12
    else:
        prem = (ratedata[option]['Premium'])*12
    
    if prem < 0:
        prem = 0
    coins = ratedata[option]['Co-insurance']
    oom = ratedata[option]['Out-of-pocket max']
    ded = ratedata[option]['Deductible']

    bottom = numpy.zeros(len(services))
    pylab.figure(figsize=(10,6))
    # first plot premium
    pylab.fill_between(services,bottom,bottom + prem,color='Blue',alpha=0.2,label='Premium')
    bottom = prem

    # Next get amount of services up to deductible
    dedamt = services*(services<=ded) + ded*(services>ded)
    pylab.fill_between(services,bottom,bottom + dedamt,color='Orange',alpha=0.2,label='Deductible')
    bottom += dedamt

    # now get coinsuranace amount above deductible up to out-of-pocket max
    coinsamt = (services - ded)*coins*(services > ded)
    coinsamt = coinsamt*(coinsamt+ded <= oom) + (oom - ded )*(coinsamt + ded > oom)
    pylab.fill_between(services,bottom,bottom + coinsamt,color='Gray',alpha=0.2,label='Co-insurance')

    # Put total amount into a dictionary to plot it below
    totals[option] = bottom + coinsamt
    pylab.ylim([0,40000])
    pylab.title("Cost Comparison vs services received")
    pylab.xlabel("Services received")
    pylab.ylabel("Total paid (less Veracity contribution)")
    pylab.legend(loc='upper left')
    pylab.grid(which='both', color='White',linestyle='-')
    ax = pylab.subplot( 111 )
    ax.set_axisbelow(True)
    ax.set_facecolor( mygraycolor )
    ax.xaxis.set_minor_locator(minor_locator)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    pylab.savefig("{}.png".format(option),dpi=300)
    pylab.close()

colors= ['Blue','Orange','Green','Red', 'Purple', 'Black', 'Teal']
pylab.figure(figsize=(10,6))
i=0
for option in totals:
    pylab.plot(services,totals[option],color=colors[i],alpha=0.5,label=option)
    i += 1
pylab.grid(which='both', color='White',linestyle='-')
ax = pylab.subplot( 111 )
ax.set_axisbelow(True)
ax.set_facecolor( mygraycolor )
ax.xaxis.set_minor_locator(minor_locator)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
pylab.title("Total cost Comparison vs services received")
pylab.xlabel("Services received")
pylab.ylabel("Total paid (less Veracity contribution)")
pylab.legend(loc='upper left')
pylab.ylim([0,30000])
pylab.savefig('totals.png',dpi=300)
pylab.close()
