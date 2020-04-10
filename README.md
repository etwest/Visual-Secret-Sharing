# VSS-Encryption
A python implementation of the image secret sharing encryption method described in the Naor-Shamir Visual Cryptography paper, found here: https://link.springer.com/content/pdf/10.1007%2FBFb0053419.pdf

### USAGE
#### Virtual Environment and Packages
- Setup a python2 virtual environment using `python2.7 -m virtualenv kenv`.
- Activate the virtual environment `source kenv/bin/activate`
- Install dependencies `pip install -r requirements.txt`

#### Run
Execute the follwoing command within the virtual machine: `python2.7 parsing.py image` it will split the image file into k shares and then combine these shares in the following ways:
- Using the computer to convert from white/black subpixels -> white pixel and all black -> black pixel this is `result.jpg`
- 'Manually' stacking the shares, this is `stacked.jpg` and shows the true benefit of VSS: the shares my be printed and physically stacked.

#### Images
Any black and white image can be used. Greyscale images are converted to black and white by kofk process and RBG images should not be used. 

The conversion from Greyscale to black and white can produce some unexpected results. Running `parsing.py` on an image will produce `beforeShare.jpg` which is the input image converted to white and black. If the `result.jpg` does not match what you expected checking `beforeShare.jpg` is a good place to start.

### NOTE
This code is done but the command line interface doesn't really exist yet.

Different values of `k` can be set on `line 88` of `parsing.py` and the code in that area can be modified to create different files and images. `k` is the number of shares created by the algorithm, increasing this number increases the complexity of all the calculations and the size of the image. It is not recommended to increase this above 10. 

This implementation only works for k of k and not k of n. This is because k of n is a nightmare. See the paper.

## Contributors
- Matthew Rhea
- Eugene Chou
- Timothy Lo
- Sabrina Tsui
- Sabrina Au
- David Atwell
- Matthew Gray
- Justin Raizes
