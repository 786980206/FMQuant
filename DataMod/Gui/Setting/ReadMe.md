## 使用QTAPI更新板块配置文件的方法
---

```
GetPlates()[2].sort_values(by=['PlateID']).to_csv(r'当前路径\Plate.ini')
```
