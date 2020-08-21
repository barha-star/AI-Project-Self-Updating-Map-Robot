from flask import Flask, render_template
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.image as img
import pandas as pd
import cv2

app = Flask(__name__)

@ app.route('/')
def index() :
    # 파일 읽기
    slam_dir = '.\\shape4.shp'
    slam_map = gpd.read_file(slam_dir)
    
    # 매장 전체 이름 컬럼 생성
    slam_map['StoreName'] = pd.Series(['Starbucks', 'Vans','Buberry','ALDO','Polo Ralph Lauren','Club Monaco',"Hat's On",'Guess','Victoria Secret',
                                       'The Body Shop', 'Brooks Brothers','Zara','Van Hart','Starfield Hanam','Lacoste',
                                       'Hollys Coffee','Converse','Fendi','Chicor','Custom Mellow','Yankee Candle','Tommy Hilfiger','GS25',
                                       'Kiz Dom','Cartier','Hermes','H & M','Gucci','AT & T', 'Chanel'])
    
    fileName = '.\\slam_map1.png'
    ndarray = img.imread(fileName)
    plt.imshow(ndarray)
    
    # plot으로 그려보기
    ax = slam_map.convex_hull.plot(color = 'salmon', figsize=(16,12), marker = "X", markersize = 600)
    ax.invert_yaxis()

    # 변화 전 후 매장 이름 저장
    before_store = None
    after_store = None

    # 그래프 작성

    for x in range(len(slam_map.label)) :
        # 변화 전 후 라벨 이름이 들어온다면 빨간 색으로 표시
        if slam_map['StoreName'][x] == before_store :
            ax.annotate(after_store, (slam_map['X'][x]-15, slam_map['Y'][x]-17), color = 'red', fontsize = 16, weight = 'bold')
        # 아니면 전체 하얀색 폰트로 표시
        else :
            ax.annotate(slam_map['StoreName'][x], (slam_map['X'][x]-15, slam_map['Y'][x]-17), color = 'white', fontsize = 12)

    # ax.set_title('Store Map Before', fontsize = 40,)
    ax.set_axis_off()
    fileName = '.\\slam_map1.png'
    ndarray = img.imread(fileName)
    plt.imshow(ndarray)
    plt.savefig("./static/images/target.png")
    
    return render_template('index.html')

@ app.route('/second')
def second() :
    # 파일 읽기
    slam_dir = '.\\shape4.shp'
    slam_map = gpd.read_file(slam_dir)
    
    # 매장 전체 이름 컬럼 생성
    slam_map['StoreName'] = pd.Series(['Starbucks', 'Vans','Buberry','ALDO','Polo Ralph Lauren','Club Monaco',"Hat's On",'Guess','Victoria Secret',
                                       'The Body Shop', 'Brooks Brothers','Zara','Van Hart','Starfield Hanam','Lacoste',
                                       'Hollys Coffee','Converse','Fendi','Chicor','Custom Mellow','Yankee Candle','Tommy Hilfiger','GS25',
                                       'Kiz Dom','Cartier','Hermes','H & M','Gucci','AT & T', 'Chanel'])
    
    fileName = '.\\slam_map1.png'
    ndarray = img.imread(fileName)
    plt.imshow(ndarray)
    
    # plot으로 그려보기
    ax = slam_map.convex_hull.plot(color = 'salmon', figsize=(16,12), marker = "X", markersize = 600)
    ax.invert_yaxis()

    # 변화 전 후 매장 이름 저장
    f = open('./mall_change.txt', 'r')
    li_index = list()
    li = list()

    for line in f:
        li_index.append(line.split(':')[1].rstrip('\n').split('_')[0])
        li.append(line.split(':')[1].rstrip('\n').split('_')[1])

    before_store_list = list()
    after_store_list = list()

    for index in range(len(li)) :
        if index % 2 == 0 :
            before_store_list.append(slam_map['StoreName'][int(li_index[index])-11])
        else :
            after_store_list.append(li[index])

    # 그래프 작성
    before_store = before_store_list[0]
    after_store = after_store_list[0]

    for x in range(len(slam_map.label)) :
        # 변화 전 후 라벨 이름이 들어온다면 빨간 색으로 표시
        if slam_map['StoreName'][x] == before_store :
            ax.annotate(after_store, (slam_map['X'][x]-15, slam_map['Y'][x]-17), color = 'red', fontsize = 16, weight = 'bold')
            before_store = before_store_list[1]
            after_store = after_store_list[1]
        # 아니면 전체 하얀색 폰트로 표시
        else :
            ax.annotate(slam_map['StoreName'][x], (slam_map['X'][x]-15, slam_map['Y'][x]-17), color = 'white', fontsize = 12)


    # ax.set_title('Store Map Before', fontsize = 40,)
    ax.set_axis_off()
    fileName = '.\\slam_map1.png'
    ndarray = img.imread(fileName)
    plt.imshow(ndarray)
    plt.savefig("./static/images/target_update.png")
    
    return render_template('index2.html')

app.run()