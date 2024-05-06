import urllib.request
from os.path import isfile

import matplotlib.pyplot as plt
import numpy as np
from cudagrad import Tensor

filename = "mnist.npz"
if not isfile(filename):
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz",
        filename,
    )

with np.load(filename, allow_pickle=True) as data:
    train_images = data["x_train"]
    train_labels = data["y_train"]
    test_images = data["x_test"]
    test_labels = data["y_test"]


class ZeroNet:
    def __init__(self):
        pass

    def __call__(self, x):
        return Tensor.zeros(x)


model = ZeroNet()

def accuracy() -> int:
    results = []
    for i, test_image in enumerate(test_images):
        output = model(train_images[i].shape)
        output = int(output.data[0, 0].item())
        results.append(output)

    import numpy as np
    return (np.sum(np.array(results) == test_labels.flatten()) / len(test_labels)) * 100

for i, train_image in enumerate(train_images):
    if i % (len(train_images) // 10) == 0:
        a = accuracy()
        print(f"{a}%", " " if a < 98 else "🔥")

num_row = 3
num_col = 4
fig, axes = plt.subplots(num_row, num_col)
for i in range(num_row * num_col):
    ax = axes[i//num_col, i%num_col]
    ax.imshow(test_images[i], cmap='gray')
    output = model(train_images[i].shape)
    output = int(output.data[0, 0].item())
    ax.set_title(f"Output: {output}")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

fig.tight_layout()
plt.savefig("./examples/plots/mnist-grid.jpg")
