##from rake_nltk import Metric,Rake
from nltk_rake_test import rake_text
from GetSyriaNewsScoer import readXML
text = readXML('E:\\PY\\test_matirial\\en_20120101_1stheadli17961_990428600000.xml')[3]
print(text)
##text = ' '.join(text)
##print(text)

##text = "Compatibility of systems of linear constraints over the set of natural numbers. \
##Criteria of compatibility of a system of linear Diophantine equations, strict inequations, \
##and nonstrict inequations are considered. Upper bounds for components of a minimal set \
##of solutions and algorithms of construction of minimal generating sets of solutions for all \
##types of systems are given. These criteria and the corresponding algorithms for constructing\
##a minimal supporting set of solutions can be used in solving all the considered types of\
##systems and systems of mixed types."
print(rake_text(text,2,2))
##print(text)
