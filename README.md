# Python-Remove-Watermark
A simple program to remove the watermark from a PDF file. 


### How?

1. convert the PDF file into images using `pdf2image`
2. convert the images to numpy array
3. find the specific pixel by watermarks' rgb values and change them into (255,255,255)
4. save the modified images


### How to use?

First you need to install the dependencies:
```
$ pip install pdf2image scikit-image numba
```

To execute:
```
$ python watermark.py --source source.pdf --target out
```
Don't forget to indicate the pdf's path you want to convert, script will automatically creates an output path.

### Results
![image](./result.png)