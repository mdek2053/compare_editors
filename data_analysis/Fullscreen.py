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
subl_lorem_ipsum = removeOutliers([0.21443, 0.22792, 0.21804, 0.21095, 0.22288, 0.21719, 0.2242, 0.21133, 0.21698, 0.22425, 0.21364, 0.23407, 0.22336, 0.20693, 0.22364, 0.2201, 0.23389, 0.21732, 0.20755, 0.2113, 0.23016, 0.21376, 0.20492, 0.22161, 0.22258, 0.21637, 0.21946, 0.2112, 0.22938, 0.22643])
subl_python_code_long = removeOutliers([0.23508, 0.23648, 0.23164, 0.23056, 0.24303, 0.2356, 0.23628, 0.23435, 0.23384, 0.23427, 0.23567, 0.23792, 0.23352, 0.23384, 0.23762, 0.22936, 0.2401, 0.22908, 0.24204, 0.23005, 0.24081, 0.22447, 0.22269, 0.23266, 0.23059, 0.2361, 0.22499, 0.22869, 0.22489, 0.22859])
gedit_lorem_ipsum = removeOutliers([0.11047, 0.08792, 0.08219, 0.0791, 0.08552, 0.08935, 0.08741, 0.10639, 0.10337, 0.09279, 0.09904, 0.08489, 0.09113, 0.10355, 0.09097, 0.10904, 0.10281, 0.10088, 0.08898, 0.09231, 0.09347, 0.08638, 0.09433, 0.0926, 0.10172, 0.11006, 0.0803, 0.09234, 0.07821, 0.10979])
gedit_python_code_long = removeOutliers([0.10235, 0.09373, 0.10459, 0.09237, 0.09796, 0.09673, 0.10164, 0.09661, 0.09469, 0.08752, 0.10118, 0.10105, 0.09575, 0.0971, 0.09515, 0.09284, 0.10216, 0.10008, 0.09959, 0.09423, 0.09148, 0.09558, 0.10271, 0.09447, 0.09722, 0.09389, 0.09397, 0.09368, 0.09464, 0.09354])
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
plt.title('Violin Plot of Fullscreen Editor Performance')
plt.ylabel('Power (W)')
plt.xticks(range(1, len(labels) + 1), labels)

# Show plot
plt.tight_layout()
plt.show()
