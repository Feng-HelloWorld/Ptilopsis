import coc.card
import time
import os

cmd=['2d10','-3d6','23','-d5','-2d','-3']
#print(coc.card.dice(cmd))

'''
success=list()
for i in range(0,50):
    data=list()
    Sum=int()
    fail_times=0
    stander=5
    stander=int(stander)
    times=5
    times=int(times)
    for i in range(0,times):
        data=data+coc.card.dice()
        Sum=Sum+data[-1]
        if data[-1]>stander:
            fail_times+=1
        time.sleep(0.005)
    #print('success rate:', (times-fail_times)/times*100,'%')
    success.append((times-fail_times)/times*100)
    #print('average:' , Sum/times)
    #print(data)
    #print(sum(data),Sum)
print("="*20)
print(success)
print("-"*20)
print("Finall success:",sum(success)/50,"%")
'''


a=coc.card.investigator()
for i in range(1):
    print(a)
    

#print(31//5)

#print(coc.card.build_and_DB(524))

cardList=os.listdir('./coc/cards/')
#print(cardList)