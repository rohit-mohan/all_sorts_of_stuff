# Decision Tree
import numpy as np
import matplotlib.pyplot as plt

class DecisionTree:
    
    def __init__(self, 
                 max_depth = 10, 
                 min_sample_ratio = 0.1, 
                 num_intervals=10, 
                 metric="var", 
                 thresholding = "interval", 
                 tree_type="regression", 
                 randomize=False):
        # dataset (including sampels and labels) that is currently being used.
        self.data = None
        # range of the features (used to calculate the intervals to sample at)
        self.feature_min = None
        self.feature_max = None
        
        # the root of the tree
        self.root = None
        
        # limitation on the maximum depth of the resulting tree
        self.max_depth = max_depth
        # limitation on the minimum number of training samples that should reach a node
        self.min_sample_ratio = min_sample_ratio
        # number of intervals into which we should divide the feature axes
        self.num_intervals = num_intervals
        
        if tree_type == "regression": 
            # function that calculates the metric upon which the best split is decided
            self.metric_func = self.variance_based_selection
            # function that returns a list of candidate (feature, threshold) pairs 
            self.thresholding_func = self.interval_based_thresholding
            # funciton that calculates whether a node is "pure"
            self.is_optimum_leaf = self.variance_is_zero
            # function that calculates the output of a node
            self.output_func = self.mean_output
        
        if randomize : 
            self.thresholding_func = self.random_thresholding
        
        self.latest_ID = 1
    
    
    """
        Returns an object node of the tree with optional initial information.
    """
    def newNode(self, ID = None,
            parentage = None,
            left=None, 
            right=None, 
            feature_index=None, 
            threshold=None, 
            data_index=None, 
            sample_ratio=None, 
            output=None):
        
        return  {"ID" : ID,
                 "parentage" : parentage,
                 "left" : left, 
                 "right" : right, 
                 "feature_index" : feature_index, 
                 "threshold" : threshold, 
                 "data_index" : data_index,
                 "sample_ratio" : sample_ratio,
                 "output" : output}
    
    """
        Calculates the total variance of data labels in both regions of the split.
        This quantity is to be minimized by choosing an appropriate feature and threshold to split at.
    """
    def calculate_variance(self, data_index, feat_index, threshold):
        region1 = []
        region2 = []
        for i in data_index : 
            if threshold < self.data["sample"][i, feat_index] : region1.append(self.data["label"][i])
            else : region2.append(self.data["label"][i])
        
        return np.var(np.array(region1)) if len(region1) else 0.0 + \
               np.var(np.array(region2)) if len(region2) else 0.0
    
    """
        Returns the seperated data indices of the two regions of the split as a tuple.
    """
    def calculate_split(self, data_index, feat_index, threshold):
        region1 = []
        region2 = []
        for i in data_index : 
            if threshold > self.data["sample"][i, feat_index] : region1.append(i)
            else : region2.append(i)
        
        return region1, region2
    
    def random_thresholding(self, node):
        feat_thresh_pair = list()
        threshold_sample = self.data["sample"][np.random.choice(node["data_index"])]
        for feat_ind in xrange(self.data["sample"].shape[1]):
            feat_thresh_pair.append((feat_ind, threshold_sample[feat_ind]))
        
        return feat_thresh_pair
    
    """
        Samples the feature axes for <self.num_intervals> equidistant points to use as candidates 
        for threshold and returns a list of tuples (feature, threshold)
    """
    def interval_based_thresholding(self, node):
        feat_thresh_pair = list()
        for feat_ind in xrange(self.data["sample"].shape[1]):
            gap = (self.feature_max[feat_ind] - self.feature_min[feat_ind]) / (self.num_intervals + 2)
            threshold = self.feature_min[feat_ind] + gap
            while threshold <= (self.feature_max[feat_ind] - gap) :
                feat_thresh_pair.append((feat_ind, threshold))
                threshold += gap
        
        return feat_thresh_pair
    
    """
        Returns the (feature, threshold pair) that has the lowest total variance for the split it enforces.
    """
    def variance_based_selection(self, node):
        variance_list = list()
        feat_thresh_pair = self.thresholding_func(node)
        for feat_ind, threshold in feat_thresh_pair : 
            variance = self.calculate_variance(node["data_index"], feat_ind, threshold)
            #print '\t', feat_ind, " ", threshold, variance
            variance_list.append((variance, feat_ind, threshold))
        
        _, feat_ind_best, threshold_best = min(variance_list, key=lambda x : x[0])
        #print "\t** ", feat_ind_best, " ", threshold_best, "**"
        return feat_ind_best, threshold_best
    
    """
        Checks if the variance of a particular node is zero. If so, then the node is "pure".
    """
    def variance_is_zero(self, node) :
        return np.var(self.data["label"][node["data_index"]]) == 0.0
    
    """
        Calculates the output of a node as the mean of labels of all the samples that reached it.
    """
    def mean_output(self, data_index):
        return np.mean(self.data["label"][data_index])
    
    
    """
        Checks for different criteria based on which a tree's growth should be stopped.
    """
    def stop_growth(self, node):
        if self.is_optimum_leaf(node) : return True
        if self.max_depth and len(node["parentage"]) >= self.max_depth : return True
        if self.min_sample_ratio and node["sample_ratio"] < self.min_sample_ratio : return True
        
        return False
        
    
    """
        Recursively creates a binary tree with nodes containing information needed to make
        decisions.
    """
    def recursive_grow(self, node):
        #print "{ ID : ", node["ID"], " parent_ID : ", node["parentage"][-1], "sample_ratio", node["sample_ratio"], " }"
        if self.stop_growth(node) : return

        feat_ind, threshold = self.metric_func(node)
        region1, region2 = self.calculate_split(node["data_index"], feat_ind, threshold)
        
        node["feature_index"] = feat_ind
        node["threshold"] = threshold
        
        if len(region1) : 
            node["left"] = self.newNode(data_index = region1, 
                               output = self.output_func(region1), 
                               sample_ratio = float(len(region1))/len(self.data["label"]),
                               ID = self.latest_ID,
                               parentage= node["parentage"] + [node["ID"]])
            self.latest_ID += 1
            self.recursive_grow(node["left"])
        
        if len(region2) : 
            node["right"] = self.newNode(data_index = region2, 
                                output = self.output_func(region2),
                                sample_ratio = float(len(region2))/len(self.data["label"]),
                                ID = self.latest_ID,
                                parentage = node["parentage"] + [node["ID"]])
            self.latest_ID += 1
            self.recursive_grow(node["right"])
    
    """
        Entry function that sets up the required initial variables and calls the recursive_grow function.
    """
    def train(self, data): 
        self.data = data
        self.feature_min = np.min(data["sample"], 0)
        self.feature_max = np.max(data["sample"], 0)
        
        data_index = range(data["sample"].shape[0])
        self.root = self.newNode(data_index = data_index,
                                 output = self.output_func(data_index), 
                                 sample_ratio=1.0, 
                                 ID=self.latest_ID, 
                                 parentage=[0])
        self.latest_ID += 1
        
        self.recursive_grow(self.root)
        self.data = None
    
    """
        Display the tree nodes in a sequential manner.
    """
    def display_tree(self, node):
        print "{ ID : ", node["ID"], " parent_ID : ", node["parentage"][-1]," feature_index : ", \
                node["feature_index"], " threshold : ", node["threshold"], \
                "sample_ratio : ", node["sample_ratio"], "output : ", node["output"], " }"
        
        if node["left"] : self.display_tree(node["left"])
        if node["right"] : self.display_tree(node["right"])
    
    
    """
        Recursively traverse the tree until a leaf node is reached. Then show the output 
        value of that node.
    """
    def recursive_test(self, sample, node):
        if node == None : 
            print "error"
            return None
        if node["feature_index"] == None : 
            return node["output"]
        
        
        if sample[node["feature_index"]] < node["threshold"] : 
            return self.recursive_test(sample, node["left"])
        else :
            return self.recursive_test(sample, node["right"])
    
    """
        Entry function for testing.
    """
    def test(self, data) :
       self.data = data
       output = np.zeros([data["sample"].shape[0],])
       for i, sample in enumerate(data["sample"])  :
           output[i] = self.recursive_test(sample, self.root)
       
       self.data = None
       return output
           
    
    def test_single(self, data):
        output = self.recursive_test(data["sample"], self.root)
        return output
    
    
    
    
if __name__ == "__main__" :
    randy = np.random.randint(0, high=100, size = 3)
    
    feature1 = range(20) + range(25,45) + range(50,70)
    feature1 = np.array(feature1).reshape([len(feature1),1])
    feature2 = [1.0] * 20 + [100.0] * 20 + [50.0] * 20
    feature2 = np.array(feature2).reshape([len(feature2),1])
    data = {"sample" : feature1, "label" : feature2}
    
    tree = DecisionTree()
    tree.train(data)
    plt.scatter(feature1, feature2)
    tree.display_tree(tree.root)
    output = tree.test(data)
    count = 0
    for i in range(data["label"].shape[0]):
        print output[i], data["label"][i]
        if output[i] == data["label"][i] : count += 1
    
    print float(count)/data["label"].shape[0]
    #test_data = {"sample" : np.array([33]), "label" : np.array([100])}
    #print tree.test_single(test_data)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


        