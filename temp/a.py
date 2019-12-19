
data1=list()
fp1=open('./temp/a1.txt','r',encoding='utf-8')
for line in fp1:
    temp1=line.strip().split(' ')
    data1.append(temp1[0])
#print(data1)

fp2=open('./temp/a2.txt','r',encoding='utf-8')
for line in fp2:
    data2=line.strip().split(',')
#print(data2)

#fp3=open('./temp/a3.txt','w')

data4=list()
fp4=open('./temp/a4.txt','r',encoding='utf-8')
for line in fp4:
    temp4=line.strip().split('（')
    data4.append(temp4[0])


for i in range(len(data1)):
    print('{}:{}:{}'.format(data1[i],data4[i],data2[i]))



fp1.close()
fp2.close()
fp4.close()
