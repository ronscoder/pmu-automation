```
In [76]: table = pd.pivot_table(df,values=['hh bal'], index=['district'], columns=['hab type'], aggfunc=np.sum)

In [77]: table
Out[77]:
                hh bal
hab type         rural   urban
district
Bishnupur       1941.0  1698.0
Chandel        13093.0     NaN
Churachandpur  15963.0     NaN
Imphal East     5198.0   160.0
Imphal West     5344.0   638.0
Senapati       27639.0     NaN
Tamenglong     12838.0     NaN
Thoubal         9988.0   870.0
Ukhrul         12137.0     NaN

```

```
In [85]: tab2 = pd.pivot_table(df, index=['district'], fill_value = 0, aggfunc='sum')

In [86]: tab2
Out[86]:
               bpl bal  hh bal  total bpl  total hh
district
Bishnupur         2304    3639       8175     26884
Chandel          12129   13093      24068     27047
Churachandpur     9217   15963      19611     52119
Imphal East       2738    5358       6063     42046
Imphal West       2013    5982       3521     44727
Senapati          8026   27639       9252     55533
Tamenglong        2080   12838       5166     26666
Thoubal           4414   10858      12250     50377
Ukhrul            5139   12137       9271     19972

```