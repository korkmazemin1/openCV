import numpy as np
# numpy dizileri listelere daha iyi performans sunar
mylist=[1,2,3]# liste oluşturuldu -py ile 

print(type(mylist))# tipi  alındı

myarray= np.array(mylist)# liste numpy dizisi haline getirildi

print(type(myarray))

x=np.arange(0,10,2)# 0 dan 10 a kadar ikişer biçimde sayar

print(x)

zeros=np.zeros(shape=(5,5))# 5 satır ve sütündan oluşan 0 lardan oluşan bir matris oluşturdu
print(zeros)

ones=np.ones(shape=(2,4)) # 2 satır ve 4 sütün içersinde 1 ler olan bir matris oluşturur

random=np.random.randint(0,100,10) # 0 ile 100 arasında rastgele 10 adet integer sayı içeren bir dizi oluşturur

print(random)

max_r=random.max# dizi içersindeki en büyük sayıyı atadık
min_r=random.min# dizi içersindeki en küçük sayıyı atadık
min_arg=random.argmin# bu  fonksiyon ile dizi içersindeki en küçük elemanın indisini alırız
shape=random.shape # dizinin boyutunu aldık

mean=random.mean# dizinin elemanlarının toplamının ortalaması çıktı

random2=random.reshape((2,5)) #diziyi 2 satır ve sütun olmak üzere yeniden boyutlandırdık

mat=np.arange(0,100).reshape(10,10) #0 ile 100 arasında rastgele sayıların atandığı  10 satır ve sütundan oluşan dizi oluşturuldu

print(mat)
print(mat.shape)


print(mat[5,4])# mat dizisinde 5.satır ve 4.sütundaki elemana eriştik

print(mat[:,1])# satır kısmını boş geçtiğimiz zaman bütün satırları aldığımızı belirttik virgülden sonra almak istediğim sütunu belirttik-- her satırdaki birinci sütunları verdi

print(mat[5,:])# 5. satırın tüm sütunlarını aldık

print(mat[0:2,0:5])# 0 dan 2. satıra ve sıfırdan 5. sütuna olan sayıları içeren dizi

