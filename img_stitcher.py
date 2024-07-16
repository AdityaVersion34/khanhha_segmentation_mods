from pathlib import Path
import os
from PIL import Image

def img_stitcher(img_path, splits_per_dim, dest_path, src_dim) -> None:
    '''
    Stitches the split images into a larger original image
    For instance, consider 100 images in img_path, with splits_per_dim = 10. This function would combine the
    100 images to create a 10x10 composite image.

    Args:
        img_path (Path): Path to the images to be stitched
        splits_per_dim (int): Number of splits to stitch
        dest_path (Path): Path where to save the stitched images

    Returns:
        None, saves stitches images in dest_path
    '''

    #TODO: currently only handles images that are all the same size

    # creating img_path and dest_path if necessary
    p_img_path = Path(img_path)
    p_dest_path = Path(dest_path)
    p_img_path.mkdir(exist_ok=True)
    p_dest_path.mkdir(exist_ok=True)

    # clear the dest path
    for path in p_dest_path.glob('*.*'):
        os.remove(str(path))

    #making a list of the image paths
    img_list = [img for img in os.listdir(img_path) if (img.endswith('.jpg') or img.endswith('.JPG'))]
    print(f"{len(img_list)} images")

    if len(img_list) == 0:
        return

    #loop through each mega-image
    for img_set in range(len(img_list)//(splits_per_dim**2)):
        #offset for the image list wrt the current mega image
        img_list_offset = img_set*(splits_per_dim**2)

        # getting the dimensions of an image (assuming they are all the same size
        sample_img = Image.open(os.path.join(img_path, img_list[img_set*(splits_per_dim**2)]))
        mini_width, mini_height = sample_img.size
        sample_img.close()

        #creating canvas mega image
        mega_img = Image.new('RGB', src_dim)

        #iterating and stitching images
        for i in range(splits_per_dim**2):
            img = img_list[i + img_list_offset]
            curr_img_path = os.path.join(img_path, img)
            curr_img = Image.open(curr_img_path)

            row = i // splits_per_dim   #current mini img row and col
            col = i % splits_per_dim

            mega_img.paste(curr_img, (col * mini_width, row * mini_height))
            curr_img.close()

        mega_img.save(os.path.join(dest_path, f"stitched_no_{img_set}.jpg"))
        mega_img.close()



if __name__ == '__main__':
    img_stitcher("./my_test_results_pred", 10, "./my_stitched_imgs", (5472, 3648))