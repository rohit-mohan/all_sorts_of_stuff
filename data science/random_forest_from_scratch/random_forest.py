# Random Forest
from decision_tree import DecisionTree
import numpy as np
import matplotlib.pyplot as plt

class RandomForest:
    def __init__(self, 
                 num_trees, 
                 forest_type="regression", 
                 metric="var",
                 aggregate_measure="mean"):
        
        self.num_trees = num_trees
        self.forest = [{"tree" : DecisionTree(metric=metric, tree_type=forest_type, randomize=True),
                        "feature_index" : None}\
                       for i in range(num_trees)]
        
        if aggregate_measure == "mean" : self.measure_func = self.aggregate_mean
            
    
    def aggregate_mean(self, tree_outputs):
        return np.mean(tree_outputs, 1)
    
    def train(self, data):
        total_num_features = data["sample"].shape[1]
        for i in xrange(self.num_trees):
            num_random_features = np.random.randint(total_num_features)
            random_feature_index = np.random.choice(total_num_features, 
                                                    size=num_random_features+1,
                                                    replace=False)
            tree_data = {"sample" : data["sample"][:,random_feature_index],
                         "label" : data["label"]}
            
            self.forest[i]["feature_index"] = list(random_feature_index)
            self.forest[i]["tree"].train(tree_data)
    
    def test(self, data):
        num_data_samples = data["sample"].shape[0]
        tree_outputs = np.zeros([num_data_samples, self.num_trees])
        
        for i in xrange(self.num_trees) :
            random_feature_index = self.forest[i]["feature_index"]
            tree_data = {"sample" : data["sample"][:,random_feature_index],
                         "label" : data["label"]}
            
            tree_outputs[:,i] = self.forest[i]["tree"].test(tree_data)
        
        forest_output = self.aggregate_mean(tree_outputs)
        return forest_output


if __name__ == "__main__"  :
    randy = np.random.randint(0, high=100, size = 3)
    
    feature1 = range(20) + range(25,45) + range(50,70)
    feature1 = np.array(feature1).reshape([len(feature1),1])
    feature2 = [randy[0]] * 20 + [randy[1]] * 20 + [randy[2]] * 20
    feature2 = np.array(feature2).reshape([len(feature2),])
    data = {"sample" : feature1, "label" : feature2}
    
    random_forest = RandomForest(10)
    random_forest.train(data)
    plt.scatter(feature1, feature2)
    output = random_forest.test(data)
    
    count = 0.0
    for i in xrange(output.shape[0]):
        #print output[i], data["label"][i]
        if randy[np.argmin(randy- output[i])] : count += 1
    print "accuracy : ", 100 * float(count)/60 , "%"