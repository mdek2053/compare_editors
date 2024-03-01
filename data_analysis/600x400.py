import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stat

def removeOutliers(arr):
    mean = np.mean(arr)
    std = np.std(arr)
    res = list(filter(lambda x: x < mean + 3*std and x > mean - 3*std, arr))
    return res

def printMedian(name, arr):
    print('Median of ' + name + ': ' + str(np.median(arr)))

def printMeanAndStd(name, arr):
    print('Mean of ' + name + ': ' + str(np.mean(arr)))
    print('Standard deviation of ' + name + ': ' + str(np.std(arr)))
    print()

def shapiroWilkNormalityTest(name, arr):
    _, pvalue = stat.shapiro(arr)
    print('ShapiroWilkNormalityTest: ' + name + ' is normally distributed: ' + str(pvalue > 0.05).upper() + ' (with p-value ' + str(pvalue) + ')')

def compareNotNormal(name, subl, gedit):
    print('PercentageOfPairs for case \'' + name + ' \': Sublime is higher in ' + str(min(100, 100*len(list(filter(lambda s: s[0] > s[1], zip(subl, gedit)))) / min(len(subl), len(gedit)))) + '% of cases')

    _, pvalue = stat.mannwhitneyu(subl, gedit, alternative='two-sided')
    print('MannWhitneyU: Sublime is significntly higher than Gedit: ' + str(pvalue < 0.05).upper() + ' (with p-value ' + str(pvalue) + ')')

def compareNormal(name, subl, gedit):
    _, pvalue = stat.ttest_ind(subl, gedit, equal_var=False, alternative='two-sided')
    print('Welch\'s t-test for case \'' + name + '\': Sublime is significantly higher than Gedit: ' + str(pvalue < 0.05).upper() + ' (with p-value ' + str(pvalue) + ')')

# Data fullscreen
subl_lorem_ipsum = removeOutliers([0.19925, 0.21532, 0.22276, 0.21225, 0.20029, 0.19442, 0.19545, 0.2145, 0.19317, 0.2056, 0.19937, 0.21879, 0.19405, 0.2196, 0.21749, 0.20028, 0.21173, 0.22063, 0.21881, 0.19733, 0.19779, 0.19723, 0.21808, 0.20266, 0.20025, 0.19626, 0.21421, 0.20249, 0.19719, 0.21333])
subl_python_code_long = removeOutliers([0.21824, 0.23135, 0.21907, 0.2182, 0.22282, 0.22069, 0.21294, 0.2202, 0.21253, 0.22162, 0.20662, 0.22301, 0.21106, 0.2174, 0.21653, 0.22278, 0.21923, 0.21747, 0.21511, 0.28139, 0.21113, 0.21309, 0.20655, 0.21095, 0.21697, 0.20664, 0.2203, 0.20829, 0.20551, 0.21639])
gedit_lorem_ipsum = removeOutliers([0.10314, 0.11233, 0.08797, 0.11432, 0.10908, 0.0982, 0.09854, 0.09885, 0.09975, 0.1139, 0.09519, 0.10925, 0.10791, 0.08873, 0.09993, 0.10171, 0.10719, 0.10036, 0.10767, 0.09289, 0.10177, 0.1116, 0.09683, 0.1154, 0.11373, 0.10964, 0.0943, 0.11586, 0.11776, 0.09638])
gedit_python_code_long = removeOutliers([0.09683, 0.20554, 0.10406, 0.10478, 0.10587, 0.10095, 0.09864, 0.1008, 0.10071, 0.0972, 0.10804, 0.09953, 0.10157, 0.09734, 0.10524, 0.10069, 0.10631, 0.09592, 0.22289, 0.09726, 0.09817, 0.09775, 0.0981, 0.0954, 0.10072, 0.10045, 0.10153, 0.10105, 0.10601, 0.09583])
sleep = removeOutliers([0.01521, 0.0196, 0.0057, 0.01347, 0.01308, 0.0044, 0.01145, 0.01039, 0.01773, 0.01485, 0.00801, 0.01427, 0.01156, 0.01589, 0.00903, 0.01128, 0.00402, 0.00317, 0.00529, 0.0049, 0.00723, 0.01193, 0.01055, 0.01317, 0.00535, 0.01473, 0.00872, 0.01058, 0.01208, 0.00965])

shapiroWilkNormalityTest("subl_lorem_ipsum", subl_lorem_ipsum)
shapiroWilkNormalityTest("subl_python_code_long", subl_python_code_long)
shapiroWilkNormalityTest("gedit_lorem_ipsum", gedit_lorem_ipsum)
shapiroWilkNormalityTest("gedit_python_code_long", gedit_python_code_long)
shapiroWilkNormalityTest("sleep", sleep)
print()

# printMedian("subl_lorem_ipsum", subl_lorem_ipsum)
# printMedian("subl_python_code_long", subl_python_code_long)
# printMedian("gedit_lorem_ipsum", gedit_lorem_ipsum)
# printMedian("subl_python_code_long", subl_python_code_long)
# printMedian("sleep", sleep)
# print()
#
# compareNotNormal("Lorem ipsum", subl_lorem_ipsum, gedit_lorem_ipsum)
# compareNotNormal("Python Long", subl_python_code_long, gedit_python_code_long)
# print()

compareNormal("Lorem ipsum", subl_lorem_ipsum, gedit_lorem_ipsum)
compareNormal("Python Long", subl_python_code_long, gedit_python_code_long)
print()

printMeanAndStd("subl_lorem_ipsum", subl_lorem_ipsum)
printMeanAndStd("subl_python_code_long", subl_python_code_long)
printMeanAndStd("gedit_lorem_ipsum", gedit_lorem_ipsum)
printMeanAndStd("gedit_python_code_long", gedit_python_code_long)
printMeanAndStd("sleep", sleep)
print()

data = [subl_lorem_ipsum, subl_python_code_long, gedit_lorem_ipsum, gedit_python_code_long, sleep]
labels = ['Sublime Text File', 'Sublime Python Code Long', 'Gedit Text File', 'Gedit Python Code Long', 'Sleep']

# Plot
plt.figure(figsize=(10, 6))
plt.violinplot(data, showmeans=False, showmedians=True)

# Customize plot
plt.title('Violin Plot of 600x400 Editor Performance')
plt.ylabel('Power (W)')
plt.xticks(range(1, len(labels) + 1), labels)

# Show plot
plt.tight_layout()
plt.show()
