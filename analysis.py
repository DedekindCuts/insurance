import json
import pylab
import numpy
import matplotlib

# plot settings
matplotlib.use("AGG")
svc_lim = None # x-axis limit for plots––set to None to set automatically
oop_lim = None # y-axis limit for plots––set to None to set automatically
colors = pylab.get_cmap("tab10")

def roundto(x, nearest = 1):
    "Rounds x to the nearest multiple of `nearest`"
    return(round(x/nearest)*nearest)

def PlanPlot(plan_data, plan_name, svc_limit = None, oop_limit = None):
    # extract the plan data
    prem = plan_data['Premium']
    coins = plan_data['Co-insurance']
    oom = plan_data['Out-of-pocket max']
    ded = plan_data['Deductible']

    if svc_limit is None:
        svc_limit = roundto(((oom - ded)/coins)*1.5, nearest = 1000)

    if oop_limit is None:
        oop_limit = roundto((oom + (prem*12))*1.5, nearest = 1000)

    services = numpy.array(range(0, svc_limit))

    # calculate the amount spent in each category for each level of services
    premamt = prem*12
    dedamt = numpy.minimum(services, ded)
    coinsamt = numpy.maximum(services - ded, 0)*coins
    coinsamt = numpy.minimum(coinsamt, oom - ded)

    # create the plot 
    pylab.figure(figsize=(10,6))

    # plot the amount spent in each category and calculate the total OOP cost 
    # for each level of services
    oop = numpy.zeros(len(services))
    pylab.fill_between(services, oop, oop + premamt, color='Blue', alpha=0.2, label='Premium')
    oop += premamt
    pylab.fill_between(services, oop, oop + dedamt, color='Orange', alpha=0.2, label='Deductible')
    oop += dedamt
    pylab.fill_between(services, oop, oop + coinsamt, color='Gray', alpha=0.2, label='Co-insurance')
    oop += coinsamt

    # specify the plot details
    mygraycolor = ( 0.95, 0.95, 0.95 )
    minor_locator = matplotlib.ticker.AutoMinorLocator(5)
    pylab.ylim([0, oop_limit])
    pylab.title("Cost comparison vs services received")
    pylab.xlabel("Services received")
    pylab.ylabel("Total out of pocket cost")
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

    # save and close
    pylab.savefig("plots/{}.png".format(plan_name),dpi=300)
    pylab.close()

    # return the total OOP cost for each level of services
    # (to use in comparison plot)
    return(oop)

def ComparisonPlot(costs, svc_limit = None, oop_limit = None, colors = None):
    # set the axis limits if not specified
    if svc_limit is None:
        svc_limit = max([len(costs[x]) for x in costs])
    if oop_limit is None:
        max_oop = max([costs[x].max() for x in costs])
        oop_limit = roundto(max_oop*1.5, nearest = 1000)

    # choose colors if not specified
    if colors is None:
        colors = pylab.get_cmap("tab10")

    # extend the cost arrays so they are all the same size
    for option in costs:
        if len(costs[option] != svc_limit):
            short = svc_limit - len(costs[option])
            pad = numpy.full(short, costs[option][-1])
            costs[option] = numpy.append(costs[option], pad)

    services = numpy.array(range(0, svc_limit))

    # create the plot
    pylab.figure(figsize=(10,6))
    for option in costs:
        pylab.plot(services, costs[option], alpha=0.5, label=option)

    # specify the plot details
    mygraycolor = ( 0.95, 0.95, 0.95 )
    minor_locator = matplotlib.ticker.AutoMinorLocator(5)
    pylab.grid(which='both', color='White',linestyle='-')
    ax = pylab.subplot( 111 )
    ax.set_prop_cycle(color = [colors(i/len(costs)) for i in range(len(costs))])
    ax.set_axisbelow(True)
    ax.set_facecolor( mygraycolor )
    ax.xaxis.set_minor_locator(minor_locator)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    pylab.title("Total cost comparison vs services received")
    pylab.xlabel("Services received")
    pylab.ylabel("Total out of pocket cost")
    pylab.legend(loc='upper left')
    pylab.ylim([0, oop_limit])
    pylab.savefig('plots/totals.png',dpi=300)
    pylab.close()

with open('rates.json') as json_data:
    ratedata = json.load(json_data)
    json_data.close()

totals = {}
for option in ratedata:
    totals[option] = PlanPlot(ratedata[option], option, svc_lim, oop_lim)

ComparisonPlot(totals, svc_lim, oop_lim, colors)
