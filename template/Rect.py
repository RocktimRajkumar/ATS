class Rect:

    # Static variable for storing image resolution
    img_dim = 0

    def __init__(self, shape, create="yes"):
        super().__init__()

        if create == 'yes':
            normalized_bounding_box = shape['geometry']
            absolute_bounding_box_width = normalized_bounding_box['Width'] * \
                Rect.img_dim[0]
            absolute_bounding_box_height = normalized_bounding_box['Height'] * \
                Rect.img_dim[1]

            self.x0 = normalized_bounding_box['Left'] * Rect.img_dim[0]
            self.y0 = normalized_bounding_box['Top'] * Rect.img_dim[1]
            self.x1 = self.x0 + absolute_bounding_box_width
            self.y1 = self.y0 + absolute_bounding_box_height
        else:
            self.x0 = shape["x0"]
            self.y0 = shape["y0"]
            self.x1 = shape["x1"]
            self.y1 = shape["y1"]

    # function return true if the element is inside the template group else return false
    def check_element_inside_group(self, other):
        if self.x0 <= other.x0 and self.y0 <= other.y0 and self.x1 >= other.x1 and self.y1 >= other.y1:
            return True
        else:
            return False
