from pathlib import Path
import os
from PIL import Image

def img_splitter(img_path, splits_per_dim, dest_path) -> tuple:
    '''
    Splits each image found in img_path into splits_per_dim images per dimension

    For instance, if splits_per_dim = 10, each image in img_path will be split into 10 images per dimension.
    i.e. 100 smaller images will be made, and saved in dest_path.

    Args:
        img_path (string): path to images
        splits_per_dim (int): number of sub-images per dimension
        dest_path (string): path to destination folder

    Returns:
        None, saves split images in destination folder
    '''

    #TODO: no longer allows images of different dimensions

    #creating img_path and dest_path if necessary
    p_img_path = Path(img_path)
    p_dest_path = Path(dest_path)
    p_img_path.mkdir(exist_ok=True)
    p_dest_path.mkdir(exist_ok=True)

    #clear the dest path
    for path in p_dest_path.glob('*.*'):
        os.remove(str(path))

    #iterate through all files in img path
    for filename in os.listdir(img_path):
        #only consider jpg files
        if filename.endswith('.jpg') or filename.endswith('.JPG'):
            #open images
            img = Image.open(os.path.join(img_path, filename))

            width, height = img.size
            #getting the dimensions of sub images
            sub_width = width // splits_per_dim
            sub_height = height // splits_per_dim

            for i in range(splits_per_dim):
                for j in range(splits_per_dim):
                    #creating coordinate bounds for current sub image
                    top = i * sub_height
                    left = j * sub_width

                    #condition to account for leftover pixels
                    bottom = top + sub_height
                    if i == splits_per_dim - 1:
                        bottom += height % splits_per_dim

                    right = left + sub_width
                    if j == splits_per_dim - 1:
                        right += width % splits_per_dim

                    sub_img = img.crop((left, top, right, bottom))
                    #saving the sub image
                    #hardcoded to jpg for now
                    sub_filename = f"{os.path.splitext(filename)[0]}_{i}_{j}.jpg"
                    sub_img.save(os.path.join(dest_path, sub_filename))

            img.close()

    return img.size

if __name__ == '__main__':
    print(img_splitter("./my_test_imgs", 10, "./my_split_imgs"))