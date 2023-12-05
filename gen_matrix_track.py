from PIL import Image
import numpy as np

SCREEN_HEIGHT = 750
SCREEN_WIDTH = 400

def load_track_matrix(image_path):
    image = Image.open(image_path)
    image = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT))

    image_matrix = np.array(image)

    track_matrix = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH), dtype=int)

    track_color = np.array([77, 77, 77, 255])
    off_track_color = np.array([255, 255, 255, 255])

    p=0
    b=0
    fp=0
    for i in range(SCREEN_HEIGHT):
        for j in range(SCREEN_WIDTH):
            if np.array_equal(image_matrix[i, j], track_color):
                track_matrix[i][j] = 0  # Pista
                p+=1
            elif np.array_equal(image_matrix[i, j], off_track_color):
                track_matrix[i][j] = 2  # Fuera de la pista
                fp+=1
            else:
                track_matrix[i][j] = 1  # Bordes
                b+=1
    print(p,b,fp)
    return track_matrix

if __name__ == "__main__":
    track_matrix = load_track_matrix('track1.png')
    track_matrix_list = track_matrix.tolist()
    track_matrix_code = "track_matrix = {}".format(track_matrix_list)

    with open('track_matrix.py', 'w') as file:
        file.write(track_matrix_code)
