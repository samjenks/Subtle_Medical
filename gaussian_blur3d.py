import numpy as np

def gaus_kernel(x, sig):
    """
    creates gaussian kernel with side length l and a sigma of sig
    """

    ax = np.arange(-x // 2 + 1., x // 2 + 1.)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2. * sig**2))
    return kernel / np.sum(kernel)


def gaussian_blur3d(input_3d: np.ndarray, meta_data: dict,
                    config: dict) -> np.array:
    '''Performs 3D Gaussian blur on the input volume

    :param input_3d: input volume in 3D numpy array
    :param meta_data: a dict object with the following key(s):
        'spacing': 3-tuple of floats, the pixel spacing in 3D
    :param config: a dict object with the following key(s):
        'sigma': a float indicating size of the Gaussian kernel

    :return: the blurred volume in 3D numpy array, same size as input_3d
    '''
    (x,y,z) = meta_data['spacing']
    sigma = config['sigma']
    np.empty((x,y,z))

    # create kernel
    kernel = gaus_kernel(x, sigma)

    # apply kernel to image
    output = []
    for i in range(y):
        temp = np.copy(input_3d)
        temp = np.roll(temp, i - 1, axis=0)
        for j in range(x):
            temp_x = np.copy(temp)
            temp_x = np.roll(temp_x, j - 1, axis=1) * kernel[i, j]
            output.append(temp_x)

    output = np.array(output)
    output = np.sum( output, axis=0)
    return output


if __name__ == '__main__':
    out = gaussian_blur3d(np.random.rand(25,25,3),{"spacing": (3,3,1)},{'sigma': 1})
