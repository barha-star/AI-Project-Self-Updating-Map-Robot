import torch
import torch.utils.data as data
import torchvision.datasets as dset
from torchvision import transforms
import torch
from torch.optim import lr_scheduler
import torch.optim as optim
from torch.autograd import Variable
from trainer import fit
import numpy as np
cuda = torch.cuda.is_available()
import matplotlib
import matplotlib.pyplot as plt
import torch.nn as nn
from datasets import BalancedBatchSampler
# Set up the network and training parameters
from networks import EmbeddingNet
from losses import OnlineTripletLoss
from utils import AllTripletSelector,HardestNegativeTripletSelector, RandomNegativeTripletSelector, SemihardNegativeTripletSelector # Strategies for selecting triplets within a minibatch
from metrics import AverageNonzeroTripletsMetric, AccumulatedAccuracyMetric
from sklearn.metrics import f1_score, accuracy_score
import time
import sys
import warnings


warnings.filterwarnings(action='ignore')

# Functions

def plot_embeddings(embeddings, targets, xlim=None, ylim=None):
    plt.figure(figsize=(10,10))
    for i in range(30):
        inds = np.where(targets==i)[0]
        plt.scatter(embeddings[inds,0], embeddings[inds,1], alpha=0.5)
    if xlim:
        plt.xlim(xlim[0], xlim[1])
    if ylim:
        plt.ylim(ylim[0], ylim[1])
    plt.legend(mnist_classes)

def extract_embeddings(dataloader, model):
    with torch.no_grad():
        model.eval()
        embeddings = np.zeros((len(dataloader.dataset), 128))
        labels = np.zeros(len(dataloader.dataset))
        k = 0
        for images, target in dataloader:
            if cuda:
                images = images.cuda()
            embeddings[k:k+len(images)] = model.get_embedding(images).data.cpu().numpy()
            labels[k:k+len(images)] = target.numpy()
            k += len(images)
    return embeddings, labels

def distance(emb1, emb2):
    emb1 = emb1/np.linalg.norm(emb1, ord = 2)
    emb2 = emb2/np.linalg.norm(emb2, ord = 2)
    return np.sum(np.square(emb1 - emb2))

## Main Functions
print("=========== Start Triplet Network ===========")

animation = "|/-\\"

for i in range(100):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()


print("\nLoading Image Data ... ")

batch_size = 256
n_classes = 30

img_dir_t = './Perfect_data/train/'
train_dataset = dset.ImageFolder(img_dir_t, transform = transforms.Compose([transforms.ToTensor()]))
img_dir_te = './Perfect_data/val/'
test_dataset = dset.ImageFolder(img_dir_te, transform = transforms.Compose([transforms.ToTensor()]))

cuda = torch.cuda.is_available()
kwargs = {'num_workers': 1, 'pin_memory': True} if cuda else {}
train_loader = data.DataLoader(train_dataset, batch_size=batch_size, shuffle=False, **kwargs)
test_loader = data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False, **kwargs)

# Train Label 저장
print("Making Train set Labels ...")
l_t = []

for i in range(len(train_dataset)):
    train_dataset.train_label = train_dataset.__getitem__(i)[1]
    l_t.append(train_dataset.train_label)

train_dataset.train_labels = torch.Tensor(l_t)

# Test Label 저장
print("Making Test set Labels ...")
l_te = []

for i in range(len(test_dataset)):
    test_dataset.test_label = test_dataset.__getitem__(i)[1]
    l_te.append(test_dataset.test_label)

test_dataset.test_labels = torch.Tensor(l_te)


fashion_mnist_classes = ['11_Starbucks', '12_Vans', '13_Burberry', '14_ALDO', '15_Polo', '16_ClubMonaco', '17_HatsOn', '18_Guess',
 '19_Victoria', '20_TheBodyShop', '21_Brooks', '22_Zara', '23_VanHart', '24_Starfield', '25_Lacoste', '26_Hollys', '27_Converse',
 '28_Fendi', '29_Chicor', '30_Custom', '31_Yankee', '32_Tommy', '33_GS', '34_KizDom', '35_Cartier', '36_Hermes', '37_HM',
 '38_Gucci', '39_AT', '40_Chanel']

mnist_classes = fashion_mnist_classes


train_batch_sampler = BalancedBatchSampler(train_dataset.train_labels, n_classes=30, n_samples=16)
test_batch_sampler = BalancedBatchSampler(test_dataset.test_labels, n_classes=30, n_samples=16)

kwargs = {'num_workers': 1, 'pin_memory': True} if cuda else {}
online_train_loader = data.DataLoader(train_dataset, batch_sampler=train_batch_sampler, **kwargs)
online_test_loader = data.DataLoader(test_dataset, batch_sampler=test_batch_sampler, **kwargs)

margin = 1.
lr = 2e-4
n_epochs = 60
log_interval = 150

device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
# embedding_net = EmbeddingNet().to(device)
model = torch.load('EmbeddingNet')
model = model.to(device)
model.eval()
if cuda:
    model.cuda()
loss_fn = OnlineTripletLoss(margin, SemihardNegativeTripletSelector(margin))

optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-5)
scheduler = lr_scheduler.StepLR(optimizer, 8, gamma=0.1, last_epoch=-1)


print("Data into EmbeddingNet ...")

animation = "|/-\\"

for i in range(100):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()

# fit(online_train_loader, online_test_loader, model, loss_fn, optimizer, scheduler, n_epochs, cuda, log_interval, metrics=[AverageNonzeroTripletsMetric()])


print("Extracting Embeddings")

animation = "|/-\\"

for i in range(100):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()

train_embeddings_otl, train_labels_otl = extract_embeddings(train_loader, model)
test_embeddings_otl, test_labels_otl = extract_embeddings(test_loader, model)


train_dict = {0:'11_Starbucks', 1:'12_Vans', 2:'13_Burberry', 3:'14_ALDO', 4:'15_Polo', 5:'16_ClubMonaco',
 6:'17_HatsOn', 7:'18_Guess', 8:'19_Victoria', 9:'20_TheBodyShop', 10:'21_Brooks', 11:'22_Zara', 12:'23_VanHart', 13:'24_Starfield',
 14:'25_Lacoste', 15:'26_Hollys', 16:'27_Converse', 17:'28_Fendi', 18:'29_Chicor', 19:'30_Custom', 20:'31_Yankee', 21:'32_Tommy',
 22:'33_GS', 23:'34_KizDom', 24:'35_Cartier', 25:'36_Hermes', 26:'37_HM', 27:'38_Gucci', 28:'39_AT', 29:'40_Chanel'}

train_label_otl = []
for i in range(len(train_labels_otl)):
    train_labels = train_dict[train_labels_otl[i]]
    train_label_otl.append(train_labels)

test_dict = {
    0:'11_Starbucks', 1:'12_Vans', 2:'13_Burberry', 3:'14_ALDO', 4:'15_Tag', 5:'16_ClubMonaco', 6:'17_HatsOn', 7:'18_Guess',
 8:'19_Victoria', 9:'20_Forever21', 10:'21_Brooks', 11:'22_Zara', 12:'23_VanHart', 13:'24_Starfield', 14:'25_Lacoste',
 15:'26_Hollys', 16:'27_Converse', 17:'28_Fendi', 18:'29_Chicor', 19:'30_Custom', 20:'31_Yankee', 21:'32_Tommy', 22:'33_GS',
 23:'34_KizDom', 24:'35_Cartier', 25:'36_Hermes', 26:'37_HM', 27:'38_Gucci', 28:'39_AT', 29:'40_Chanel'}

test_label_otl = []
for i in range(len(test_labels_otl)):
    test_labels = test_dict[test_labels_otl[i]]
    test_label_otl.append(test_labels)



print("\nPrinting Accuracy & F1 Score ...")

distances = [] # squared L2 distance between pairs
identical = [] # 1 if same identity, 0 otherwise

num = len(train_embeddings_otl)

for i in range(num - 1):
    for j in range(i + 1, num):
        distances.append(distance(train_embeddings_otl[i], test_embeddings_otl[j]))
        identical.append(1 if train_label_otl[i] == test_label_otl[j] else 0)

distances = np.array(distances)
identical = np.array(identical)

thresholds = np.arange(0.1, 2, 0.1)

f1_scores = [f1_score(identical, distances < t) for t in thresholds]
acc_scores = [accuracy_score(identical, distances < t) for t in thresholds]

opt_idx = np.argmax(f1_scores)
# Threshold at maximal F1 score
opt_tau = thresholds[opt_idx]
# Accuracy at maximal F1 score
opt_acc = accuracy_score(identical, distances < opt_tau)

# Plot F1 score and accuracy as function of distance threshold
plt.plot(thresholds, f1_scores, label='F1 score');
plt.plot(thresholds, acc_scores, label='Accuracy');
plt.axvline(x=opt_tau, linestyle='--', lw=1, c='lightgrey', label='Threshold')
plt.title(f'Accuracy at threshold {opt_tau:.2f} = {opt_acc:.3f}');
plt.xlabel('Distance threshold')
plt.legend();
plt.show()

# Eunbi code

print('Reprocessing Data ... ')

animation = "|/-\\"

for i in range(100):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()

import numpy as np
import os.path

class IdentityMetadata():
    def __init__(self, base, name, file):
        # dataset base directory
        self.base = base
        # identity name
        self.name = name
        # image file name
        self.file = file

    def __repr__(self):
        return self.image_path()

    def image_path(self):
        return os.path.join(self.base, self.name, self.file)

def load_metadata(path):
    metadata = []
    for i in sorted(os.listdir(path)):
        for f in sorted(os.listdir(os.path.join(path, i))):
            # Check file extension. Allow only jpg/jpeg' files.
            ext = os.path.splitext(f)[1]
            if ext == '.jpg' or ext == '.jpeg':
                metadata.append(IdentityMetadata(path, i, f))
    return np.array(metadata)

metadata2 = load_metadata(img_dir_t)
metadata3 = load_metadata(img_dir_te)

import cv2
import matplotlib.patches as patches

def load_image(path):
    img = cv2.imread(path, 1)
    # OpenCV loads images with color channels
    # in BGR order. So we need to reverse them
    return img[...,::-1]

def show_pair(idx1, idx2):
    plt.figure(figsize=(8,3))
    plt.suptitle(f'Distance = {distance(train_embeddings_otl[idx1], test_embeddings_otl[idx2]):.2f}')
    plt.subplot(121)
    plt.imshow(load_image(metadata2[idx1].image_path()))
    plt.subplot(122)
    plt.imshow(load_image(metadata3[idx2].image_path()))
    plt.show();

k = []
for i in range(len(train_embeddings_otl)):
    k.append(round(distance(train_embeddings_otl[i], test_embeddings_otl[i]), 4))
w = np.arange(0, len(train_embeddings_otl), 1)
plt.plot(w, k);


from collections import Counter

label_c = Counter(test_label_otl)

samples = []
for i in range(len(test_dict)):
    samples.append(label_c[test_dict[i]])

bb = 0
bb_l = []
c_l = []

for i in range(len(samples)):
    cnt = 0
    bb += samples[i]
    bb_l.append(bb)
    b_n = bb-samples[i]
    a = k[b_n:bb]
    for j in range(samples[i]):
        if a[j] >= opt_tau:
            cnt+=1
    c_l.append(cnt)

thres = []
for i in range(len(samples)):
    thres.append(int(samples[i] - samples[i]*0.5))

changed_class_idx = []
for i in range(len(c_l)):
    if c_l[i] > thres[i]:
        changed_class_idx.append(i)
changed_list = []
f = open("./mall_change.txt", 'w')
for i in range(len(changed_class_idx)):
    j = int(bb_l[changed_class_idx[i]] - 4)
    print('before:',train_dict[changed_class_idx[i]],
          'after:',test_dict[changed_class_idx[i]])
    changed_list.append((train_dict[changed_class_idx[i]],test_dict[changed_class_idx[i]]))
    f.write('before:'+str(train_dict[changed_class_idx[i]]+"\n"))
    f.write('after:'+str(test_dict[changed_class_idx[i]]+"\n"))
    show_pair(j,j)
f.close()

print("=========== Program Ended! ===========")
