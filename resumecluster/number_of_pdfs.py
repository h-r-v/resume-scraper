import os
from pdf2image import convert_from_path
import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import shutil
from sklearn.cluster import AgglomerativeClustering

def extract(X):
    model = tf.keras.applications.VGG16(
    include_top=False,
    input_shape=(224,224, 3),
    pooling=None,
    )
    
    return model.predict(X)

def pdf2img(pdf):
    pages = convert_from_path(pdf)
    pages[0].save("temp.jpg", "JPEG")
    img = image.load_img("temp.jpg", target_size=(224, 224, 3))
    x = image.img_to_array(img)
    x = preprocess_input(x)
    return x
    
def number_of_pdfs(fpath):
    featurelist = []
    namelist = {}
    for num, i in enumerate(os.listdir(fpath)):
        #print(num)
        path_ = os.path.join(fpath,i)
        
        if os.path.isfile(path_):
            #pdf to x
            namelist[num+1] = i
            feature = pdf2img(path_)
            featurelist.append(feature)
            
    featurelist = extract(np.array(featurelist))
    featurelist = featurelist.reshape([featurelist.shape[0],-1])

    print("feature extraction done")

    clusters = AgglomerativeClustering(n_clusters=None, compute_full_tree=True, distance_threshold=620).fit(featurelist)

    for i, label in enumerate(list(clusters.labels_)):
        from_ = fpath
        to_ = os.path.join(fpath,str(label))
        if os.path.exists(to_):
            shutil.copy( os.path.join(from_,namelist[i+1]), os.path.join(to_,namelist[i+1]))
        else:
            os.mkdir(to_)
            shutil.copy( os.path.join(from_,namelist[i+1]), os.path.join(to_,namelist[i+1]))

    class__ = list(np.unique(clusters.labels_, return_counts=True)[0])
    count__ = list(np.unique(clusters.labels_, return_counts=True)[1])

    return [len(np.unique(clusters.labels_)),list([class__, count__])]
    
if __name__=='__main__':
    print(number_of_pdfs(os.path.join('resumecluster/dataset','GoodData')))
