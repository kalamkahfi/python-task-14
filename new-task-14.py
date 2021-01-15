# -*- coding: utf-8 -*-
# Import libraries for plotting
import numpy as np 
import matplotlib.pyplot as plt

NtL = lambda n: 10*np.log10(n)

LtN = lambda x: 10**(x/10)

def pathloss(fq,types,ht,hr,d):

  # If frequency is defined by the range number in MHz, then the result will be assigned at Ca and Cb values
  if fq in range(150,1501):
    Ca=69.55
    Cb=26.16
  elif fq in range(1501,2001):
    Ca=46.3
    Cb=33.9
  else:
    Ca = print("The given frequency does not meet the C1 criteria.")
    Cb = print("The given frequency does not meet the C2 criteria.")
    return Ca,Cb
  
  # Based on the area type
    # types is the type of area given
  if types == 'urban' :
    cm=0
  elif types == 'suburban' :
    cm=-2*((np.log10((fq/28)**2))-5.4)
  elif types == 'open':
    cm=-4.78*(np.log10(fq))+18.33*(np.log10(fq))-40.94
  else:
    cm=print('The given area type(s) is not suitable for this parameter')
  
  # the value a(hr) is
  ahr = (1.1*np.log10(fq)-0.7)*hr-(1.56*np.log10(fq)-1.8)

  # Calculating the Path Loss Model
  Lp = Ca+(Cb*np.log10(fq))-(13.83*np.log10(ht))-ahr+((44.9-6.55*np.log10(ht))*np.log10(d))-cm
  return Lp
    # ht is the height of antenna transmitter in range of 30 to 200 m
    # hr is the height of antenna receiver in range of 1 to 20 m

# The input Pathloss Model Cost 231 for Different Area and Frequency
  # fq is the frequency,ranging from 150 to 2000 MHz
fq1=700 #in Mhz
fq2=900 #in Mhz
fq3=1800 #in MHz
loc1='urban'
loc2='suburban'
loc3='open'
tower=80 #in m
user=1.5 #in m
dmin=300 #in m
dmax=1000 #in m
N=200 #dots
d=np.random.randint(dmin,dmax,N)
  # d is the distance between the transmitter and receiver in m

# Print the random integer of Urban area distance input
print(d)

# Define the Pathloss Cost 231 Model for Area by the given input
LpUrban=pathloss(fq3,loc1,tower,user,d)
LpSubUrban=pathloss(fq3,loc2,tower,user,d)
LpOpen=pathloss(fq3,loc3,tower,user,d)

# Sort the Distance for Area 
d_sort=d[np.argsort(d)]
Urban_sort=LpUrban[np.argsort(d)]
Suburban_sort=LpSubUrban[np.argsort(d)]
Open_sort=LpOpen[np.argsort(d)]

fig, ax = plt.subplots()
ax.plot(d_sort,Urban_sort, color='b', label='Urban')
ax.plot(d_sort,Suburban_sort, color='r', label='Suburban')
ax.plot(d_sort,Open_sort, color='g', label='Open')
ax.set_title('Path loss at 1800 MHz on various areas')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Pathloss (dB)')
ax.legend(loc='upper left')
plt.show()

# Define the Pathloss Cost 231 Model for Frequency by the given input
LpUrbanFQ1=pathloss(fq1,loc1,tower,user,d)
LpUrbanFQ2=pathloss(fq2,loc1,tower,user,d)
LpUrbanFQ3=pathloss(fq3,loc1,tower,user,d)

# Sort the Distance for Area 
d_sort=d[np.argsort(d)]
UrbanFQ_sort=LpUrbanFQ1[np.argsort(d)]
UrbanFQ2_sort=LpUrbanFQ2[np.argsort(d)]
UrbanFQ3_sort=LpUrbanFQ3[np.argsort(d)]

fig, ax = plt.subplots()
ax.plot(d_sort,UrbanFQ_sort, color='b', label='700 MHz')
ax.plot(d_sort,UrbanFQ2_sort, color='r', label='900 MHz')
ax.plot(d_sort,UrbanFQ3_sort, color='g', label='1800 MHz')
ax.set_title('Path Loss in Urban area with various frequencies')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Path Loss (dB)')
ax.legend(loc='upper left')
plt.show()

def ValuePrX(Ptx,Pl,Gtx,Grx):
  
  # Convert the Transmitter Power from mW to dBm
  PtdB=NtL(Ptx)
  
  # Calculating the Prx value
  PrX=PtdB - Pl + Gtx + Grx

  # Convert the Receiver Power from dBm to mW 
  PrXmW=LtN(PrX)

  return PrXmW

# The Input Receiver Power Model for Different Area and Frequency

# tx is the given transmitter power value
# pl is path loss value is derived from the previous calculation model
# gtx is the given transmitter gain value
# grx is the given receiver gain value 

tx = 30000 # in miliwatt
Pla = Urban_sort
Plb = Suburban_sort
Plc = Open_sort
Pld = UrbanFQ_sort
Ple = UrbanFQ2_sort
Plf = UrbanFQ3_sort
gtx = 10 # in dB
grx = 2 # in dB

# Define the Receiver Power Model for Area by the given input
PrxUrban = ValuePrX(tx, Pla, gtx, grx)
PrxSubUrban = ValuePrX(tx, Plb, gtx, grx)
PrxOpen = ValuePrX(tx, Plc, gtx, grx)

# Define the Receiver Power Model for Frequency by the given input
PrxUrban700  = ValuePrX(tx, Pld, gtx, grx)
PrxUrban900  = ValuePrX(tx, Ple, gtx, grx)
PrxUrban1800 = ValuePrX(tx, Plf, gtx, grx)

fig, ax = plt.subplots()
ax.plot(d_sort,PrxUrban, color='b', label='Urban')
ax.plot(d_sort,PrxSubUrban, color='r', label='Suburban')
ax.plot(d_sort,PrxOpen, color='g', label='Open')
ax.set_title('Power received in various areas')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Power Received (mWatt)')
ax.legend(loc='upper right')
plt.show()

fig, ax = plt.subplots()
ax.plot(d_sort,PrxUrban700, color='b', label='700 MHz')
ax.plot(d_sort,PrxUrban900, color='r', label='900 MHz')
ax.plot(d_sort,PrxUrban1800, color='g', label='1800 MHz')
ax.set_title('Power received at various frequencies')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Power Received (mWatt)')
ax.legend(loc='upper right')
plt.show()

def SNRValue(Prx,BW):

  #No to BW
  No=-174+10*np.log10(BW)

  # Convert No in BW to numeric
  NoW=LtN(No)

  # Calculating the SNR value
  SNR= Prx/NoW

  return SNR

# The Input SNR Model for Different Area and Frequency

# prx is receiver power value derived from the previous calculation value
# bw is the given bandwith value

Prx1 = PrxUrban
Prx2 = PrxSubUrban
Prx3 = PrxOpen
Prx4 = PrxUrban700
Prx5 = PrxUrban900
Prx6 = PrxUrban1800
BW   = 50000000

# Define the SNR Model for Area by the given input
SNRUrban = SNRValue(Prx1,BW)
SNRSubUrban = SNRValue(Prx2,BW)
SNROpen = SNRValue(Prx3,BW)

# Define the SNR Model for Frequency by the given input
SNRUrban700 = SNRValue(Prx4,BW)
SNRUrban900 = SNRValue(Prx5,BW)
SNRUrban1800 = SNRValue(Prx6,BW)

fig, ax = plt.subplots()
ax.plot(d_sort,SNRUrban, color='b', label='Urban')
ax.plot(d_sort,SNRSubUrban, color='r', label='Sub Urban')
ax.plot(d_sort,SNROpen, color='g', label='Open')
ax.set_title('SNR model for various areas')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('SNR (dB)')
ax.legend(loc='upper right')
plt.show()

fig, ax = plt.subplots()
ax.plot(d_sort,SNRUrban700, color='b', label='700 MHz')
ax.plot(d_sort,SNRUrban900, color='r', label='900 MHz')
ax.plot(d_sort,SNRUrban1800, color='g', label='1800 MHz')
ax.set_title('SNR model for various frequencies')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('SNR (dB)')
ax.legend(loc='upper right')
plt.show()

def Capacity(SNR,BW):

  # Calculating the Cellular Capacity
  Cellcap = BW*np.log2(1+SNR)

  return Cellcap

# Input Capacity Model for Different Area and Frequency
# SNR is a signal to noise ratio value derived from the previous calculation value
# BW is the given bandwith value

SNR1 = SNRUrban 
SNR2 = SNRSubUrban
SNR3 = SNROpen
SNR4 = SNRUrban700
SNR5 = SNRUrban900
SNR6 = SNRUrban1800
BW   = 50000000

#Cellular Capacity Model for Area
cellcapUrban = Capacity(SNR1, BW)
cellcapSubUrban = Capacity(SNR2, BW)
cellcapOpen = Capacity(SNR3, BW)

#Cellular Capacity Model for Frequency
cellcapUrban700 = Capacity(SNR4, BW)
cellcapUrban900 = Capacity(SNR5, BW)
cellcapUrban1800 = Capacity(SNR6, BW)

fig, ax = plt.subplots()
ax.plot(d_sort,cellcapUrban, color='b', label='Urban')
ax.plot(d_sort,cellcapSubUrban, color='r', label='Suburban')
ax.plot(d_sort,cellcapOpen, color='g', label='Open')
ax.set_title('Capacity in various areas')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Capacity')
ax.legend(loc='upper left')
plt.show()

fig, ax = plt.subplots()
ax.plot(d_sort,cellcapUrban700, color='b', label='700 MHz')
ax.plot(d_sort,cellcapUrban900, color='r', label='900 MHz')
ax.plot(d_sort,cellcapUrban1800, color='g', label='1800 MHz')
ax.set_title('Capacity on various frequencies')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Capacity')
ax.legend(loc='upper left')
plt.show()

