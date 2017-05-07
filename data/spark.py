from pyspark import SparkContext
from itertools import combinations

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)  # each worker loads a piece of the data file

group_1 = data.map(lambda line: line.split(","))  # tell each worker to split each line of it's partition
group_2 = group_1.groupByKey().map(lambda x: (x[0], list(x[1])))

group_3 = group_2.flatMap(lambda x: [(x[0], k) for k in list(combinations(x[1], 2))])
group_3 = group_3.map(lambda x: (x[1], x[0]))
group_4 = group_3.groupByKey().map(lambda x: (x[0], set(x[1])))

group_5 = group_4.map(lambda x: (x[0], len(x[1])))

group_6 = group_5.filter(lambda x: x[1] > 2).collect()
for item, count in group_6:
    print ("item %s count %d" % (item, count))
print ("Popular items done")

sc.stop()
