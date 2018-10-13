# dogorfrog
The idea is to use to apply gradient descent on the input rather then on the weights. This will change the input to better match the desired output. A script that does this can be found [here](https://github.com/cppio/picoCTF-2018-Writeups/blob/master/dogorfrog.py).

The original templates contains,
```python
img = array_to_img(test)
```
but this is in fact incorrect. Looking at `prepare_image`, it calls `preprocess_input` after `img_to_array`. This has to be undone before `array_to_img` is called. Viewing the [source](https://github.com/keras-team/keras-applications/blob/master/keras_applications/imagenet_utils.py#L45) in keras, it simply scales and offsets the input, so applying the inverse fixes that. This ensures that the predictions that the program sees is the same as the predictions that the server sees.

This method could be sped up by scaling the gradient, but it doesn't take too long.
