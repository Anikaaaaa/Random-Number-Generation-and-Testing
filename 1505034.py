import math

import scipy
from scipy import stats

Z_i = []
U_i = []
n = 0

def Generation():
    i=0
    z_0 = 1505034
    z_iMunus1 = z_0
    global Z_i
    global U_i
    global n
    while i<n:
        rand_num = (65539 * z_iMunus1) % (2**31)
        u = rand_num / (2**31)
        z_iMunus1 = rand_num
        Z_i.append(rand_num)
        U_i.append(u)
        i+=1


def Serial_Test(k,alpha,d):

    tuples = int(n / d)
    # print(tuples)
    array = []
    i = 0
    while i < tuples:
        array.append([])
        i += 1
    i = 0
    global U_i
    j = 0
    ############# Keeping in a array tuples-wise
    while j < tuples:
        l = 0
        while l < d:
            array[j].append(U_i[(j * d) + l])
            l += 1
        j += 1

    j = 0
    ############### printing array for checking
    while j < tuples:
        l = 0
        while l < d:
            #print(array[j][l])
            l += 1
        j += 1

    ###################### Calculating range for the given k
    ranges = []
    i = 0
    ranges.append(0)
    while i < k:
        ranges.append((i + 1) / k)
        i += 1

    i = 0
    while i < k:
        # print(ranges[i])
        i += 1
    length = (10 ** d) -1
    f_i_j = [0] * length     #### array for keeping f value
    pos_array = [0]*length   #### array for all possible combination

    i = 0
    ############################ Calculation f value
    while i < tuples:
        flag = 10 ** (d-1)
        j=0
        pos = 100
        result = 0
        all_pos = 0
        positions = 0
        while j<d:
            l=0
            while l < k+1:
                if l < k:
                    if  array[i][j] <= ranges[l+1] and  array[i][j] > ranges[l] :
                       pos = l+1

                    all_pos = l+1
                elif l == k:
                    if array[i][j] <= ranges[l] and array[i][j]> ranges[l-1]:
                        pos = l
                    all_pos = l
                else:
                    pos = 100
                l+=1
            if pos!=100:
                result += (flag*pos)
                positions += flag*all_pos
            flag = int(flag/10)
            #print(flag)

            j+=1
        f_i_j[result] += 1
        #pos_array[i] = positions
        #print(result)
        #print(f_i_j[result])

        i+=1
    ############################### Calculating all possible combinations
    m = 0
    my_pos = 0
    while m < length:
        e = 0
        flag = 10
        new_m = m
        cont = 1

        while e < d:
            is_mod = new_m % flag
            if is_mod==0 or is_mod > k:
                cont = 0
                break
            #flag = int(flag/10)
            new_m = int(new_m / 10)
            e += 1
        if cont == 1:
            pos_array[my_pos] = m
            #print(my_pos)
            #print(pos_array[my_pos])
            my_pos = my_pos + 1
        m += 1

    r=0
    while r<my_pos:
        #print(pos_array[r])
        r+=1
    ############################################## Using the formula
    e = 0
    my_sum = 0.0
    while e<length:
        if pos_array[e] != 0:
            #print(pos_array[e])
            this_pos = pos_array[e]
            #print("position is %d",this_pos)
            #print("value is %d",f_i_j[this_pos])
            my_sum += ((f_i_j[this_pos]-(tuples/(k ** d))) ** 2)
        e += 1

    this_chi_square = ((k ** d) / tuples) * my_sum
    print("My calculated value ",this_chi_square )
    #print(this_chi_square)
    ######################################### Value using library function and comparison
    chi_sqr = stats.chi2.ppf(1-alpha,((k**d)-1))
    print("Using library Function",chi_sqr)
    #print(chi_sqr)
    if this_chi_square > chi_sqr:
        print("Rejected")
    else:
        print("Not Rejected")






def Runs_Test(alpha):

    runs = []
    i=0
    while i<6:
        runs.append(0)
        i+=1
    i=0
    global U_i
    global n
    pos = 0
    ############### Run length calculation
    while i<n :
        j=pos
        run_len = 0
        while j<n:
            if j < (n-1):
                if U_i[(j+1)] > U_i[j]:
                    run_len += 1
                    pos += 1
                elif U_i[(j+1)] < U_i[j]:
                    run_len += 1
                    pos += 1
                    break
            if j == n-1:

                if U_i[j] > U_i[j-1]:
                    run_len += 1
                    pos += 1
                elif U_i[j] < U_i[j-1]:
                    run_len += 1
                    pos += 1
                    break
            j+=1



        if run_len > 0 and run_len < 6:
            runs[run_len-1] += 1
        if run_len >= 6:
            runs[5] += 1

        i+=1

    for elements in runs:
        print(elements)
    a = [[4529.4, 9044.9, 13568, 18091, 22615, 27892],
         [9044.9, 18097, 27139, 36187, 45234, 55789],
         [13568, 27139, 40721, 54281, 67852, 83685],
         [18091, 36187, 54281, 72414, 90470, 111580],
         [22615, 45234, 67852, 90470, 113262, 139476],
         [27892, 55789, 83685, 111580, 139476, 172860]]

    b = [1/6, 5/24, 11/120, 19/720, 29/5040, 1/840]

    i=0
    ################## Using the formula
    my_sum = 0.0
    while i<6:
        #print(i)
        sum = 0.0
        j = 0
        while j<6:
            #print(a[i][j])
            sum += (a[i][j] * (runs[i] - n*b[i]) * (runs[j] - n*b[j]))
            j += 1

        my_sum += sum
        i += 1

    sum = my_sum/n
    print(sum)

    ############### chi square using library function and comparison
    chi_square_alpha = stats.chi2.ppf(1-alpha,6)
    print(chi_square_alpha)
    if sum > chi_square_alpha:
        print("Rejected")
    else:
        print("Not rejected")



def Uniformity_Test(k,alpha):

    i=0
    f_j = [0]*k
    global n
    global U_i
    while i<k:
        lower = float((i)/k)
        upper = float((i+1)/k)
        j=0
        while j < n:
            if U_i[j]>=lower and U_i[j]<upper:
                f_j[i]+=1
            j+=1
        i+=1
    #for element in f_j:
       # print(element)
    sum = 0.0
    j=1
    while j<=k:
        sum += (f_j[j-1] - n/k) ** 2
        j+=1

    chi_square = (k/n) * sum
    print("My calculated chi square is ",chi_square)
    chi_square_k = stats.chi2.ppf(1-alpha,k-1)
    print("Using library function is ",chi_square_k)
    if chi_square > chi_square_k:
        print("Rejected")
    else:
        print("Not rejected")

def Correlation_Test(J,alpha):
    global n
    global U_i
    h=math.floor((((n-1)/J)-1))
    k=0
    sum=0.0
    while k <= h:
        sum += (U_i[(k*J)] * U_i[((k+1)*J)])
        k += 1
    ro_cap_j = (12/(h+1)) * sum - 3

    var = (13*h + 7) / ((h+1) ** 2)

    A_j = ro_cap_j / math.sqrt(var)
    print(abs(A_j))

    param = 1 - alpha/2
    z_alpha = scipy.stats.norm.ppf(param)
    print(z_alpha)
    if abs(A_j) > z_alpha :
        print("Rejected")
    else:
        print("Not rejected")

def main():
    global n
    n = int(input("Enter n"))
    Generation()
    global Z_i
    global U_i
    ###################### print
    #i = 0
    #while i < n:
    #    print(Z_i[i])
    #    i+=1
    #i=0
    #while i < n:
        #print(U_i[i])
        #i+=1
    #######################

    k = int(input("Enter k"))
    alpha = float(input("Enter Alpha"))
    #Uniformity_Test(k,alpha)


    d = int(input("Enter d"))
    Serial_Test(k,alpha,d)

    #Runs_Test(alpha)

    #J = int(input("Enter J"))
    #Correlation_Test(J,alpha)



main()