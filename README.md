# Water Drops Detection

![](https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/logo(2).jpg)

---

<img src = "https://img.shields.io/badge/Python 3.9-006C6B?style=for-the-badge&color=3C7270&labelColor=%23006C6B&logo=python&logoColor=FFFFFF"> <img src ='https://img.shields.io/github/watchers/HerrPhoton/Water_drop_detection?style=for-the-badge&color=3C7270&labelColor=%23006C6B&logo=actigraph&logoColor=FFFFFF'>
<img src = 'https://img.shields.io/github/actions/workflow/status/HerrPhoton/Water_drop_detection/Project-tests.yml?style=for-the-badge&color=3C7270&labelColor=%23006C6B&logo=githubactions&logoColor=FFFFFF'>
<img src = 'https://img.shields.io/github/contributors/HerrPhoton/Water_drop_detection?style=for-the-badge&color=3C7270&labelColor=%23006C6B&logo=teamspeak&logoColor=FFFFFF'>  
<img src ='https://img.shields.io/github/repo-size/HerrPhoton/Water_drop_detection?style=for-the-badge&color=3C7270&labelColor=%23006C6B&logo=weightsandbiases&logoColor=FFFFFF'>
<img src = "https://img.shields.io/badge/Code%20Coverage-81%25-success?style=for-the-badge&color=3C7270&labelColor=%23006C6B&logo=textpattern&logoColor=FFFFFF">
<img src = "https://img.shields.io/docker/image-size/alincnl/drop_detection/detect?style=for-the-badge&color=3C7270&labelColor=%23006C6B&logo=docker&logoColor=FFFFFF">


---
### Выполнили: 
+ [Володина Софья](https://github.com/PiroJOJO)
+ [Лейсле Александр](https://github.com/HerrPhoton)
+ [Шитенко Алина](https://github.com/alincnl)
### Дата: 25.06.2023г.
---

## Введение

Проект создан для детектирования на изображении капель воды на любой поверхности. Эта задача стала интересна, так как мы хотели 
попрактиковать свои навыки в обучении нейронных сетей, собрать своими руками датасет и сделать модель доступной для любого пользователя, который захочет проверить работу детекции на своем собственном изображении.

---

## Neural Net

Для детекции капель была выбрана нейросеть с архитектурой Unet, имеющая энкодер ResNet50. Она представляет из себя сверточную нейронную сеть из  двух блоков: энкодера и декодера. Первый из них уменьшает разрешение изображения и увеличивает информационный объем каждого пикселя. Декодер, наоборот, разворачивает выход из энкодера до первоначального размера и выдает маску искомого объекта.  

---

![](https://github.com/HerrPhoton/Water_drop_detection/blob/master/images/unet.jpg))

---

Данная нейронная сеть проста в реализации и удобна в использовании для решения поставленных целей проекта. Для Unet характерна высокая точность работы при малом объеме данных. В результате её работы есть возможность не только получить маску изображения, 
но и найти площадь сегментированного объекта.

---

## Датасет

Сборка датасета состояла из нескольких частей: 
- поиск изображений в интернете/съемка фотографии с каплями воды
- создание маски в фоторедакторе, на которой белым цветом отображен участок капли, черным - фон 
- перевод маски с помощью скрипта на языке Python в бинарную матрицу True-False и сохранение ее с расширением .npz 
- создание датасета путем объединения исходной фотографии и соответствующей ей npz-маски

---

![](https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/dataset)

---

## UI

UI сделан с помощью языка Python, библиотеки PyQT5 и программы QtDesigner. 
Интерфейс принимает изображение или папку с изображениями и отправляет их в нейронную сеть для детектирования. Результат сохраняется в новую папку в двух форматах: на одном капли закрашиваются, на другом добавляется bounding box. Пользователь может выбрать любую из версий для просмотра. Также при передаче изображения есть возможность отредактировать его: повернуть в любую сторону или обрезать. Каждая страница UI изначально создана в QtDesigner, в коде представлена в виде класса со своими методами. Взаимодействие между страницами происходит с помощью функций библиотеки PyQT5

---

![](https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/ui.jpg)

---

## Управление проектом

### Установка и запуск программы

Для пользователя:
```
pip install water-drop-detection
```
+ Для запуска проекта через py файл:
```
from water_drop_detection import main
main.main()
```
+ Или при клонировании репозитория можно вызвать:
```
python water_drop_detection/main.py
```

Для разработчика:
+ Вы можете скачать проект по этой ссылке: https://github.com/HerrPhoton/Water_drop_detection
+ Или клонировать репозиторий нижеприведенной командой:
```
git clone https://github.com/HerrPhoton/Water_drop_detection
```
+ Откройте проект в IDE
+ Установите необходимые библиотеки командой ниже:
```
pip -r install requirements.txt
```
+ Запуск приложения осуществяется через запуск файла main.py:
```
python main.py
```
+ Страница документации может быть запущена через:
```
start docs\build\html\index.html
```

Работа с Docker:
+ Команды для сборки и запуска проекта в терминале:
```
docker build . -t drop_detection
docker run drop_detection
```
+ Образ можно скачать с Docker Hub по ссылке: https://hub.docker.com/repository/docker/alincnl/drop_detection

Информация о покрытии тестами:
https://app.codecov.io/gh/HerrPhoton/Water_drop_detection

---

## Результаты работы программы

---

| Тестовое изображение            | Маска изображения                | Маска + bounding box + окружность |
| :---                            |    :----:                        |                              ---: |
| <img src="https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/test1-1.jpg"  alt="1" width = 360px height = 360px > | <img src="https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/test1-2.png"  alt="1" width = 360px height = 360px > | <img src="https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/test1-3.png"  alt="1" width = 360px height = 360px > |
| <img src="https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/test2-1.jpg"  alt="1" width = 360px height = 360px > | <img src="https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/test2-2.png"  alt="1" width = 360px height = 360px > | <img src="https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/test2-3.png"  alt="1" width = 360px height = 360px > |
| <img src="https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/test3-1.jpg"  alt="1" width = 360px height = 360px >  | <img src="https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/test3-2.png"  alt="1" width = 360px height = 360px > | <img src="https://github.com/HerrPhoton/Water_drop_detection/blob/Documentation/images/test3-3.png"  alt="1" width = 360px height = 360px > |

## Источники

---
[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)
