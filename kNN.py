import numpy as np
import os
import operator


def img2vector(filename, width, height):
    """将txt文件转为一维数组"""
    return_vector = np.zeros((1, width * height))
    fr = open(filename)
    for i in range(height):
        line = fr.readline()
        for j in range(width):
            return_vector[0, height * i + j] = int(line[j])
    return return_vector


# test_set 单个测试样本
# train_set 训练样本二维数组
# labels 训练样本对应的分类
# k k值

def classify(test_set, train_set, labels, k):
    """对测试样本进行kNN分类,返回测试样本的类别"""
    # 获取训练样本条数
    train_size = train_set.shape[0]  # 0 代表这个np的第1维度（行数）1代表np的第2维度（列数）

    # 计算特征值的差值并求平方
    # tile(A,(m,n))，功能是将数组A行重复m次 列重复n次
    diff_mat = np.tile(test_set, (train_size, 1)) - train_set
    sq_diff_mat = diff_mat ** 2

    # 计算欧式距离 存储到数组 distances
    sq_distances = sq_diff_mat.sum(axis=1)  # 将每一行求和
    distances = sq_distances ** 0.5

    # 按距离由小到大排序对索引进行排序
    sorted_index = distances.argsort()  # argsort函数返回的是数组值从小到大的索引值

    # 求距离最短k个样本中 出现最多的分类
    class_count = {}
    for i in range(k):
        near_label = labels[sorted_index[i]]
        class_count[near_label] = class_count.get(near_label, 0) + 1
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return str(sorted_class_count[0][0])


# train_data_path 训练样本文件夹
# test_data_path 测试样本文件夹
# k k个最近邻居
def get_error_rate(train_data_path, test_data_path, k):
    """统计识别错误率"""
    width, height = 32, 32
    train_labels = []

    training_file_list = os.listdir(train_data_path)  # 获取所有的训练样本的文件名
    train_size = len(training_file_list)  # 2600

    # 生成全为0的训练集数组,2600*1024
    train_set = np.zeros((train_size, width * height))

    # 读取训练样本
    for i in range(train_size):
        file = training_file_list[i]  # 得到每个文件的文件名（包含后缀）
        file_name = file.split('.')[0]  # 去除后缀
        label = str(file_name.split('_')[0])  # 取出含在文件名中的标签
        train_labels.append(label)
        train_set[i, :] = img2vector(os.path.join(train_data_path, training_file_list[i]), width, height)
        a = (train_set[i, :])  # ????

    test_file_list = os.listdir(test_data_path)  # 获取所有的测试样本的文件名（包含后缀.txt）
    # 识别错误的个数
    error_count = 0.0
    # 测试样本的个数
    test_count = len(test_file_list)

    # 统计识别错误的个数
    for i in range(test_count):
        file = test_file_list[i]
        true_label = file.split('.')[0].split('_')[0]  # 读出文件名首的真标签
        # 把当前的测试文件(32*32)转换成一维数组
        test_set = img2vector(os.path.join(test_data_path, test_file_list[i]), width, height)
        # 使用classify计算出预测的标签
        test_label = classify(test_set, train_set, train_labels, k)
        print(true_label, test_label)
        if test_label != true_label:
            error_count += 1.0
    percent = error_count / float(test_count)
    print("识别错误率是:{}".format(str(percent)))


# 计算识别错误率
get_error_rate("D:\MLtrain", "D:\MLtest", 6)

# testset = img2vector('D:/MLtrain/hsf_1_00000.txt',32,32)
# testlabel = classify(testset,'D:/MLtest/hsf_1_00120.txt','a',3)
# print(testlabel)
