from typing import Dict, Tuple
from numpy.typing import NDArray  

def random_translate(image: NDArray[np.int16], max_translation: int=100) -> NDArray[np.int16]:
    image = np.array(image)
    translation_x = np.random.randint(-max_translation, max_translation)
    translation_y = np.random.randint(-max_translation, max_translation)
    new_image = np.zeros_like(image)
    activated_pixels_x, activated_pixels_y = np.where(image > 0)
    new_x = np.clip(activated_pixels_x + translation_x, 0, image.shape[0] - 1)
    new_y = np.clip(activated_pixels_y + translation_y, 0, image.shape[1] - 1)
    new_image[new_x, new_y] = image[activated_pixels_x, activated_pixels_y]

    return new_image


def random_rotate(image: NDArray[np.int16]) -> NDArray[np.int16]:
    k = random.choice(range(0, 3))
    return np.rot90(image, k=k)


def cut_edges(image: NDArray[np.int16], xmin:int, xmax:int, ymin:int, ymax:int) -> NDArray[np.int16]:
    return image[xmin: xmax, ymin: ymax]