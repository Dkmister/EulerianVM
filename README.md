# Eulerian Video Magnification for Revealing Subtle Changes in the World
Final Project for the course Fundamentals of Image Processing, 
abording the paper with the same name.

# What's it?
This works envolves choosing a paper from SIGGRAPH and then developing it with the creation of a software or program.

# About the Paper :
Do you want to know more?

Check the following link: <http://people.csail.mit.edu/mrub/vidmag/>

# About implementation:
We are probably going to use Python 2.7 to solve this problem.

# How to use it?
Using the terminal go to the directory trad_base

## Details
sys.argv[1] => filename

sys.argv[2] => pyramid type: "gaussiana"/"laplaciana"

sys.argv[3] => min frequence, float

sys.argv[4] => max frequence, float

sys.argv[5] => amplification factor, int

sys.argv[6] => numbers of layers (default:4),int

## Use examples:
`python3 emBR.py face.mp4 laplaciana 0.83 1 25 4`

`python emBR.py face.mp4 laplaciana 0.83 1 25 4`
