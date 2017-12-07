# packagesimport csvimport randomimport copyimport matplotlib.pyplot as pltimport numpy as npimport sysimport win32com.clientfrom cvxopt import matrix, spdiag, solvers, sparseoutfile = '100%ev_opt_losses.csv'loadsfile = '100%ev_opt_total_loads.csv'pfStem = '%ev_pf.csv'household_profiles = []vehicle_profiles = []#start_times = []total_loads = []for i in range(0,1000):    household_profiles.append([0.0]*1440)    vehicle_profiles.append([0.0]*1440)# the following is using CREST'''i = 0with open('household_demand_pool.csv','rU') as csvfile:    reader = csv.reader(csvfile)    for row in reader:        if row == []:            continue        for j in range(0,1000):            household_profiles[j][i] = float(row[j])        i += 1'''# and this uses smart meter datai = 0with open('household_demand_pool_HH.csv','rU') as csvfile:    reader = csv.reader(csvfile)    for row in reader:        hh = []        for cell in row:            hh.append(float(cell))        hh.append(hh[0])        for j in range(0,1440):            p1 = int(j/30)            p2 = p1 + 1            f = float(j%30)/30            household_profiles[i][j] = (1-f)*hh[p1] + f*hh[p2]        i += 1i = 0with open('vehicle_demand_pool.csv','rU') as csvfile:    reader = csv.reader(csvfile)    for row in reader:        if row == []:            continue        for j in range(0,1440):            vehicle_profiles[i][j] = float(row[j])        i += 1'''with open('start_time_pool.csv','rU') as csvfile:    reader = csv.reader(csvfile)    for row in reader:        if row == []:            continue        start_times.append(int(row[0]))'''t_int = 10 # minsvehicle_req = []for profile in vehicle_profiles:    start = 0    energy = sum(profile)/t_int #kW-min    if energy == 0:        vehicle_req.append([0,0.0])        continue        if profile[start] != 0:        while profile[start] != 0:            start += 1    while profile[start] == 0 and start < 1439:        start += 1    vehicle_req.append([start,energy])del(vehicle_profiles)        engine = win32com.client.Dispatch("OpenDSSEngine.DSS")engine.Start("0")L = []# I want to do this first without EVs, then withfor mc in range(0,200):    #powerFactor = []    # pick the household demand profiles    chosen = []    while len(chosen) < 55:        ran = int(random.random()*1000)        if ran not in chosen:            chosen.append(ran)    chosenV = []    while len(chosenV) < 55:        ran = int(random.random()*1000)        if ran not in chosenV:            chosenV.append(ran)    # here the optimisation happens    t = int(2160/t_int) # 32 hrs to wrap around    # first calculate base load    baseLoad = [0.0]*int(1440/t_int)    for i in range(0,len(baseLoad)):        for j in range(0,len(chosen)):            for k in range(0,t_int):                baseLoad[i] += household_profiles[chosen[j]][i*t_int+k]/t_int    baseLoad += baseLoad[:int(12*(60/t_int))]        # then collect energy and timing requirements    b = []    t_av = []    unused = []    for i in range(0,len(chosenV)):        if vehicle_req[chosenV[i]][1] == 0:            unused.append(i)            continue        b.append(vehicle_req[chosenV[i]][1])        t_av.append(int(vehicle_req[chosenV[i]][0]/t_int))    n = len(chosenV)-len(unused)    if n == 0:        print 'no charging'    else:        A1 = matrix(0.0,(n,t*n)) # ensures right amount of energy provided        A2 = matrix(0.0,(n,t*n)) # ensures vehicle only charges when avaliable        b += [0.0]*n        b = matrix(b)        skp = 0        for j in range(0,len(chosenV)):            if j in unused:                skp += 1                continue            v = j-skp            arrival = t_av[v]            departure = int((np.random.normal(8,2)*60+1440)/t_int)            for i in range(0,t):                A1[n*(t*v+i)+v] = 1.0                if i < arrival:                    A2[n*(t*v+i)+v] = 1.0                elif i > departure:                    A2[n*(t*v+i)+v] = 1.0        A = sparse([A1,A2])        A3 = spdiag([-1]*(t*n)) # ensures non-negative charging power        A4 = spdiag([1]*(t*n)) # ensures charging powers less than pMax        G = sparse([A3,A4])        h = []        for i in range(0,t*n):            h.append(0.0)        for i in range(0,t*n):            h.append(3.5)        h = matrix(h)        q = [] # incorporates base load into the objective function        for i in range(0,n):            for j in range(0,len(baseLoad)):                q.append(baseLoad[j])        q = matrix(q)        I = spdiag([1]*t)        P = sparse([[I]*n]*n)        try:            sol = solvers.qp(P,q,G,h,A,b) # solve quadratic program            if sol['status'] != 'optimal':                print 'gotcha'                continue            X = sol['x']        except:            print 'boo'            continue    optimal_profiles = []    v = 0    for i in range(0,len(chosenV)):        if i in unused:            optimal_profiles.append([0.0]*1440)            continue         load = []        for j in range(0,t):            load.append(X[v*t+j]) # extract each vehicles load        new = [0.0]*1440        for j in range(0,t):            for k in range(0,t_int):                ti = j*t_int+k                if ti < 1440:                    new[ti] = load[j]                else:                    new[ti-1440] = load[j]        optimal_profiles.append(new)        v += 1    # peace of mind check    '''    total = [0.0]*1440    for i in range(0,1440):        total[i] += baseLoad[int(i/t_int)]        for j in range(0,55):            total[i] += optimal_profiles[j][i]    plt.figure(1)    for i in range(0,6):        plt.plot(np.linspace(0,24,num=1440),total)        plt.plot(np.linspace(0,24,num=int(1440/t_int)),baseLoad[:int(24*60/t_int)])    plt.show()    #'''    for i in range(1,56):        with open('household-profiles/'+str(i)+'.csv','w') as csvfile:            writer = csv.writer(csvfile)            for j in range(0,1440):                writer.writerow([household_profiles[chosen[i-1]][j]+                                 optimal_profiles[i-1][j]])                                         engine.text.Command='clear'    circuit = engine.ActiveCircuit    engine.text.Command='compile master.dss'    engine.Text.Command='Export mon LINE1_PQ_vs_Time'    powerIn = [0.0]*1440    powerOut = [0.0]*1440    #pf = [0.0]*1440    with open('LVTest_Mon_line1_pq_vs_time.csv','rU') as csvfile:        reader = csv.reader(csvfile)        next(reader)        i = 0        for row in reader:            powerIn[i] -= float(row[2])            powerIn[i] -= float(row[4])            powerIn[i] -= float(row[6])                        i += 1    for hh in range(1,56):        engine.Text.Command='Export mon hh'+str(hh)+'_pQ_vs_time'                i = 0        with open('LVTest_Mon_hh'+str(hh)+'_pq_vs_time.csv','rU') as csvfile:            reader = csv.reader(csvfile)            next(reader)            for row in reader:                powerOut[i] += float(row[2])                i += 1    total_loads.append(powerOut)        net = []    for i in range(0,1440):        net.append(powerIn[i]-powerOut[i])    L.append(net)    #powerFactor.append(pf)newL = []for i in range(0,1440):    newL.append([0.0]*len(L))for i in range(0,len(L)):    for j in range(0,1440):        newL[j][i] = L[i][j]with open(outfile,'w') as csvfile:    writer = csv.writer(csvfile)    for row in newL:        writer.writerow(row)            with open(loadsfile,'w') as csvfile:    writer = csv.writer(csvfile)    for row in total_loads:        writer.writerow(row)'''with open(pfStem,'w') as csvfile:    writer = csv.writer(csvfile)    for row in powerFactor:        writer.writerow(row)'''            