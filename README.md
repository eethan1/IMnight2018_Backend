# IMnight2018_Backend

DataBase Module

User:
  ID


表演者(User):


使用者(User):  
  當天表演者(表演者ID)  
  表演者清單(List表演者ID)  

# API ENDPOINT

### Human
- [抽取本日人物](#抽取本日人物) `GET /human/drawCard/ `
- `GET /human/listCard/ `

## 抽取本日人物
URL : `/human/drawCard/ `

Method : `GET`

Auth Require : YES

Data constraints

```json
{
  data
}
```


```python
if 當天抽的人 == null:  
  抽一個人  
  把他加到表演者清單  
  更新當天狀態  
return 當天表演者
```

* 取的清單

`GET /human/listCard/ `
```python
return 表演者清單
```


## EARTH
