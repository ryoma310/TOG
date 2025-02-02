# wget "https://www.dropbox.com/s/xtud0t70ypk6ur5/SSD300.h5?dl=1" -O "./model_weights/SSD300.h5"

from dataset_utils.preprocessing import letterbox_image_padded
from misc_utils.visualization import visualize_detections
from keras import backend as K
from models.ssd import SSD300
from PIL import Image
from tog.attacks import *
import os
K.clear_session()

# Preparation of Victim Detector
weights = 'model_weights/SSD300.h5'

detector = SSD300(weights=weights)

# Configuration of Attack Hyperparameters
eps = 8 / 255.       # Hyperparameter: epsilon in L-inf norm
eps_iter = 2 / 255.  # Hyperparameter: attack learning rate
n_iter = 10          # Hyperparameter: number of attack iterations

fpath = './assets/example_1.jpg'    # TODO: Change this path to the image to be attacked

input_img = Image.open(fpath)
x_query, x_meta = letterbox_image_padded(input_img, size=detector.model_img_size)
detections_query = detector.detect(x_query, conf_threshold=detector.confidence_thresh_default)
visualize_detections({'Benign (No Attack)': (x_query, detections_query, detector.model_img_size, detector.classes)})

# TOG-untargeted Attack
# Generation of the adversarial example
x_adv_untargeted = tog_untargeted(victim=detector, x_query=x_query, n_iter=n_iter, eps=eps, eps_iter=eps_iter)

# Visualizing the detection results on the adversarial example and compare them with that on the benign input
detections_adv_untargeted = detector.detect(x_adv_untargeted, conf_threshold=detector.confidence_thresh_default)
visualize_detections({'Benign (No Attack)': (x_query, detections_query, detector.model_img_size, detector.classes),
                      'TOG-untargeted': (x_adv_untargeted, detections_adv_untargeted, detector.model_img_size, detector.classes)}, save_path="./img/untargeted.png")

# TOG-vanishing Attack
# Generation of the adversarial example
x_adv_vanishing = tog_vanishing(victim=detector, x_query=x_query, n_iter=n_iter, eps=eps, eps_iter=eps_iter)

# Visualizing the detection results on the adversarial example and compare them with that on the benign input
detections_adv_vanishing = detector.detect(x_adv_vanishing, conf_threshold=detector.confidence_thresh_default)
visualize_detections({'Benign (No Attack)': (x_query, detections_query, detector.model_img_size, detector.classes),
                      'TOG-vanishing': (x_adv_vanishing, detections_adv_vanishing, detector.model_img_size, detector.classes)}, save_path="./img/vanishing.png")

# TOG-fabrication Attack
x_adv_fabrication = tog_fabrication(victim=detector, x_query=x_query, n_iter=n_iter, eps=eps, eps_iter=eps_iter)

# Visualizing the detection results on the adversarial example and compare them with that on the benign input
detections_adv_fabrication = detector.detect(x_adv_fabrication, conf_threshold=detector.confidence_thresh_default)
visualize_detections({'Benign (No Attack)': (x_query, detections_query, detector.model_img_size, detector.classes),
                      'TOG-fabrication': (x_adv_fabrication, detections_adv_fabrication, detector.model_img_size, detector.classes)}, save_path="./img/fabrication.png")

# TOG-mislabeling Attack
# Generation of the adversarial examples
x_adv_mislabeling_ml = tog_mislabeling(victim=detector, x_query=x_query, target='ml', n_iter=n_iter, eps=eps, eps_iter=eps_iter)
x_adv_mislabeling_ll = tog_mislabeling(victim=detector, x_query=x_query, target='ll', n_iter=n_iter, eps=eps, eps_iter=eps_iter)

# Visualizing the detection results on the adversarial examples and compare them with that on the benign input
detections_adv_mislabeling_ml = detector.detect(x_adv_mislabeling_ml, conf_threshold=detector.confidence_thresh_default)
detections_adv_mislabeling_ll = detector.detect(x_adv_mislabeling_ll, conf_threshold=detector.confidence_thresh_default)
visualize_detections({'Benign (No Attack)': (x_query, detections_query, detector.model_img_size, detector.classes),
                      'TOG-mislabeling (ML)': (x_adv_mislabeling_ml, detections_adv_mislabeling_ml, detector.model_img_size, detector.classes),
                      'TOG-mislabeling (LL)': (x_adv_mislabeling_ll, detections_adv_mislabeling_ll, detector.model_img_size, detector.classes)}, save_path="./img/mislabeling.png")

