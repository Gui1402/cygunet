import numpy as np


class CygImage(np.ndarray):
    """A subclass of numpy.ndarray with additional image processing methods.

    Parameters
    ----------
    input_array : array_like
        An array-like object to be converted to a CygImage instance.

    Attributes
    ----------
    info : str, optional
        Additional information about the image.
    """

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.info = getattr(obj, "info", None)

    def random_translate(self, max_translation: int):
        """Randomly translates the image within the specified range.

        Parameters
        ----------
        max_translation : int
            Maximum number of pixels to translate the image in both x and y directions.

        Returns
        -------
        CygImage
            A new CygImage instance with the translated image.

        Examples
        --------
        >>> data = np.array([[1, 2, 0], [4, 5, 0], [0, 0, 6]])
        >>> img = CygImage(data)
        >>> translated_img = img.random_translate(1)
        >>> print(translated_img)
        """
        translation_x = np.random.randint(-max_translation, max_translation)
        translation_y = np.random.randint(-max_translation, max_translation)

        new_image = np.zeros_like(self)
        activated_pixels_x, activated_pixels_y = np.where(self > 0)
        new_x = np.clip(
            activated_pixels_x + translation_x, 0, self.shape[0] - 1
        )
        new_y = np.clip(
            activated_pixels_y + translation_y, 0, self.shape[1] - 1
        )
        new_image[new_x, new_y] = self[activated_pixels_x, activated_pixels_y]
        return new_image

    def cut_edges(self, xmin: int, xmax: int, ymin: int, ymax: int):
        """Cuts the image to the specified bounding box.

        Parameters
        ----------
        xmin : int
            Minimum x-coordinate of the bounding box.
        xmax : int
            Maximum x-coordinate of the bounding box.
        ymin : int
            Minimum y-coordinate of the bounding box.
        ymax : int
            Maximum y-coordinate of the bounding box.

        Returns
        -------
        CygImage
            A new CygImage instance with the cropped image.

        Examples
        --------
        >>> data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> img = CygImage(data)
        >>> cropped_img = img.cut_edges(1, 3, 1, 3)
        >>> print(cropped_img)
        [[5 6]
         [8 9]]
        """
        return self[xmin:xmax, ymin:ymax]

    def scale(self, imin: float, imax: float, dtype: np.dtype = np.float16):
        """Scales the image pixel values to the range [0, 1] and converts to
        the specified dtype.

        Parameters
        ----------
        imin : float
            Minimum intensity value to scale from.
        imax : float
            Maximum intensity value to scale to.
        dtype : data-type, optional
            The desired data-type for the scaled image (default is np.float16).

        Returns
        -------
        CygImage
            A new CygImage instance with scaled pixel values.

        Examples
        --------
        >>> data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> img = CygImage(data)
        >>> scaled_img = img.scale(1, 9)
        >>> print(scaled_img)
        [[0.      0.125   0.25  ]
         [0.375   0.5     0.625 ]
         [0.75    0.875   1.    ]]
        """
        clipped_img = np.clip(self, imin, imax)
        scaled_img = (clipped_img - imin) / (imax - imin)
        return scaled_img.astype(dtype)
