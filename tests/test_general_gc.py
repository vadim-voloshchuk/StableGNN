from datetime import datetime

import numpy as np
import torch
import torch_geometric.transforms as T

from stable_gnn.graph import Graph
from tutorials.train_model_pipeline import TrainModelGC, TrainModelOptunaGC

dt = datetime.now()

name = "BACE"  # всего там 1000 файлов, но они маленькие, качается довольно долго
conv = "GAT"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
ssl_flag = False
extrapolate_flag = False
root = "../data_validation/"
####

data = Graph(name, root=root + str(name), transform=T.NormalizeFeatures())
print("i have read data")
assert len(data) == 500

#######
train_flag = True
if train_flag:
    optuna_training = TrainModelOptunaGC(
        data=data,
        dataset_name=name,
        conv=conv,
        device=device,
        ssl_flag=ssl_flag,
        extrapolate_flag=extrapolate_flag,
    )

    best_values = optuna_training.run(number_of_trials=10)  # считается достаточно долго
    model_training = TrainModelGC(
        data=data,
        conv=conv,
        dataset_name=name,
        device=device,
        ssl_flag=ssl_flag,
        extrapolate_flag=extrapolate_flag,
    )

    model, train_acc_mi, train_acc_ma, test_acc_mi, test_acc_ma = model_training.run(best_values)
    print(test_acc_mi)
    assert np.isclose(train_acc_mi, 0.7, atol=0.1)
    assert np.isclose(test_acc_mi, 0.7, atol=0.1)

    torch.save(model, "model.pt")
model = torch.load("model.pt")
print(model)
