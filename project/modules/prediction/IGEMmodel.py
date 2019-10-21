
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import torch 
from torch.autograd import Variable 
import torch.nn.functional as F
from torch import nn

Max_length = 200
Batch_size = 64
Base_num = 25
Zymolyte_num = 27
Zymolyte_Max_length = 60
weight_decay = 0.01
class CNNnet(torch.nn.Module):
    def __init__(self):
        super(CNNnet,self).__init__()
        
        Vocab = 1000
        Dim = Base_num
        zy_Dim = Zymolyte_num
        Cla = 2
        Ci = 1
        Knum = 200
        Ks = [2,2,3,3,4,4,6,6,8,8,10,10] 
        feature_size = 50
        fc1_num = 300
        self.convs1 = nn.ModuleList([
                            nn.Sequential(nn.Conv1d(in_channels=Dim, 
                                                    out_channels=feature_size, 
                                                    kernel_size=h),  
                            nn.BatchNorm1d(num_features=feature_size),           								
                            nn.ReLU(),
                            nn.MaxPool1d(kernel_size=Vocab-h+1))
                            
                    for h in Ks	
                    ])			
        self.convs2 = nn.ModuleList([
                            nn.Sequential(nn.Conv1d(in_channels=zy_Dim, 
                                                    out_channels=feature_size, 
                                                    kernel_size=h),  
                            nn.BatchNorm1d(num_features=feature_size),           									
                            nn.ReLU(), 
                            nn.MaxPool1d(kernel_size=Vocab-h+1)) 
                            
                    for h in Ks	
                    ])			
        self.convscat = nn.ModuleList([
                            nn.Sequential(nn.Conv1d(in_channels=2, 
                                                    out_channels=feature_size, 
                                                    kernel_size=h), 
                            nn.BatchNorm1d(num_features=feature_size),           									
                            nn.ReLU(), 
                            nn.MaxPool1d(kernel_size=Vocab-h+1))
                            
                    for h in Ks	
                    ])			
        
        self.mlp0 = torch.nn.Sequential(
            torch.nn.Linear(1800,100),
            nn.BatchNorm1d(num_features=100),
            torch.nn.ReLU()
        )
        self.mlp2 = torch.nn.Linear(100,2)
    def forward(self, x1,x2):
    
        x1 = x1.permute(0, 2, 1)
        x1 = [conv(x1) for conv in self.convs1]
        x1 = torch.cat(x1,1)
        
        x2 = x2.permute(0, 2, 1)
        x2 = [conv(x2) for conv in self.convs2]
        x2 = torch.cat(x2,1)

        x = torch.cat([x1,x2],dim=2)#[64,500,2]
        x = x.permute(0,2,1)
        x = [conv(x) for conv in self.convscat]
        x = torch.cat(x,1)
        x = x.view(-1, x.size(1))
        x1 = x1.view(x1.size(0),-1)
        x2 = x2.view(x2.size(0),-1)
        x = torch.cat([x1,x,x2],dim=1)
        x = self.mlp0(x)
        x = self.mlp2(x)
        x_soft = F.softmax(x, dim=1)
        return x,x_soft

def one_hot(base):
    protein = np.zeros([Max_length,Base_num])
    for i in range(len(base)):
        if(i>=Max_length):
            break
        count = ord(base[i]) - ord("A")
        if(count>=25 or count<0):
            continue
        protein[i][count] = 1
    return protein

def zymolyte_one_hot(zymolyte):
    compound = np.zeros([Zymolyte_Max_length,Zymolyte_num])
    list_zymolyte = [2,7,3,4,15,18,26,27,28,32,34,36,45,46,-30,-25,-24,-22,-20,-19,-18,-16,-15,-14,-13,-4,-1]
    for i in range(len(zymolyte)):
        if(i>=Zymolyte_Max_length):
            break
        count = ord(zymolyte[i]) - ord("A")
        try:
            index = list_zymolyte.index(count)
        except:
            index = 0
        if(count>=Zymolyte_num or count<0):
            continue
        compound[i][index] = 1
    return compound

 
class Regularization(torch.nn.Module):
    def __init__(self,model,weight_decay,p=2):
        '''
        :param model 模型
        :param weight_decay:正则化参数
        :param p: 范数计算中的幂指数值，默认求2范数,
                  当p=0为L2正则化,p=1为L1正则化
        '''
        super(Regularization, self).__init__()
        if weight_decay <= 0:
            print("param weight_decay can not <=0")
            exit(0)
        self.model=model
        self.weight_decay=weight_decay
        self.p=p
        self.weight_list=self.get_weight(model)
        self.weight_info(self.weight_list)
 
    def forward(self, model):
        self.weight_list=self.get_weight(model)#获得最新的权重
        reg_loss = self.regularization_loss(self.weight_list, self.weight_decay, p=self.p)
        return reg_loss
 
    def get_weight(self,model):
        weight_list = []
        for name, param in model.named_parameters():
            if 'weight' in name:
                weight = (name, param)
                weight_list.append(weight)
        return weight_list
 
    def regularization_loss(self,weight_list, weight_decay, p=2):
        reg_loss=0
        for name, w in weight_list:
            l2_reg = torch.norm(w, p=p)
            reg_loss = reg_loss + l2_reg
 
        reg_loss=weight_decay*reg_loss
        return reg_loss
 
    def weight_info(self,weight_list):
        print("---------------regularization weight---------------")
        for name ,w in weight_list:
            print(name)
        print("---------------------------------------------------")

# In[20]:


def predict(species="ALY",entry="OC(=O)C(=C)OP(=O)(O)O",enzyme="MGSLKES"):
    model = CNNnet()
    species_total = ["ALY","BNA","BRP","CMAX","CSAT","GAB","NHE"]
    if species not in species_total:
        species = "ALY"
    model.load_state_dict(torch.load("model/"+species+"_new.pkl"))
    x1 = np.zeros([Batch_size,Max_length,Base_num])
    x2 = np.zeros([Batch_size,Zymolyte_Max_length,Zymolyte_num])
    x1[0] = one_hot(enzyme)
    x2[0] = zymolyte_one_hot(entry)    
    x1 = torch.from_numpy(x1)
    x2 = torch.from_numpy(x2)   
    batch_x1 = Variable(x1) # torch.Size([16, 1, 1000, 25])
    batch_x2 = Variable(x2)
    out,out_soft = model(batch_x1.float(),batch_x2.float())
    predict_score = out_soft.detach().numpy()[0][1]
    return predict_score