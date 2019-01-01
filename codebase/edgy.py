import matplotlib.pyplot as plt
import numpy as np, scipy.ndimage as ndi, utility


class TestSuite:
    # Define dimensions of test images [All the same]
    test_width = 0
    test_height = 0
    # Hard Coding the test images for easy external access
    basic = [[]]
    medium = [[]]
    hard = [[]]
    final = [[]]

    def __init__(self, width, height):
        self.test_width = width
        self.test_height = height
        self.basic = TestSuite.simple_test_case(self.test_width,
                                                self.test_height, False)
        self.medium = TestSuite.simple_border_test(self.test_width,
                                                   self.test_height, 5, False)
        self.hard = TestSuite.complex_test_case(self.test_width,
                                                self.test_height, 10, False)
        self.final = self.final_test_case(True)

    @staticmethod
    def simple_test_case(width, height, show):
        """
        Return the most basic test case, a blank
        white space with a centered black box with the
        parameterized width and height. [4 Edges].
        :param width:
        :param height:
        :param show:
        :return:
        """
        test = np.zeros((width, height))
        center_x = int(width / 2)
        center_y = int(height / 2)
        bar_size_x = int(width / 8)
        bar_size_y = int(height / 4)
        test[center_x - bar_size_x:center_x + bar_size_x,
        center_y - bar_size_y:bar_size_y + center_y] = 1

        if show:
            plt.imshow(test, 'gray_r')
            plt.title('Simple Bar Test')
            plt.show()
        return test

    @staticmethod
    def simple_border_test(width, height, thickness, show):
        """
        Return a test image that simple contains a border with
        designated thickness (pixels). [4 Edges]
        :param width:
        :param height:
        :param thickness:
        :param show:
        :return:
        """
        test = np.zeros((width, height))
        test[0:thickness, :] = 1
        test[:, 0:thickness] = 1
        test[:, height - thickness:height] = 1
        test[width - thickness:width, :] = 1
        # Show the Test Case
        if show:
            plt.imshow(test, 'gray_r')
            plt.show()
        return test

    @staticmethod
    def complex_test_case(width, height, thickness, show):
        """
        Return an image with both a box in the center, and
        a black border. [8 Edges]
        :param width:
        :param height:
        :param thickness:
        :param show:
        :return:
        """
        test = np.zeros((width, height))
        # Create box in the center
        center_x = int(width / 2)
        center_y = int(height / 2)
        db = 2 * thickness  # Box-depth
        test[center_x - db:center_x + db, center_y - db:center_y + db] = 1
        # Add border too
        test[0:thickness, :] = 1
        test[:, 0:thickness] = 1
        test[:, height - thickness:height] = 1
        test[width - thickness:width, :] = 1
        # Show the Test Case
        if show:
            plt.imshow(test, 'gray_r')
            plt.show()
        return test

    @staticmethod
    def final_test_case(show):
        path_to_image = '/media/root/CoopersDB/buzzhole.jpg'
        test = plt.imread(path_to_image)[100:600, 100:600, 0]
        avg = np.mean(test)
        dims = test.shape
        test_image = np.zeros(dims).flatten()
        print "Avg: "+str(avg)

        ii = 0
        for pixel in test.flatten():
            if pixel >= avg:
                test_image[ii] = 1
            ii += 1
        test_image = test_image.reshape(dims)
        if show:
            plt.imshow(test_image, 'gray_r')
            plt.show()
        return test


class EdgeDetection:
    scanning_agents = {}
    image_input = [[]]
    # Debug will show everything
    debug = True

    def __init__(self, subject_image):
        self.image_input = subject_image

    def convolutional_automata_(self):
        areal = [[1,1,1],[1,1,1],[1,1,1]]  # Counting Area
        lefty = [[1,1,1],[0,0,0],[0,0,0]]  # Counting UP edge
        right = [[0,0,0],[0,0,0],[1,1,1]]
        upper = [[1,0,0],[1,0,0],[1,0,0]]
        lower = [[0,0,1],[0,0,1],[0,0,1]]
        # do a 2D convolution using the kernels above
        areal_conv = ndi.convolve(self.image_input, areal)
        upper_conv = ndi.convolve(self.image_input, upper)
        lower_conv = ndi.convolve(self.image_input, lower)
        lefty_conv = ndi.convolve(self.image_input, lefty)
        right_conv = ndi.convolve(self.image_input, right)
        # save these into single convolutions structure
        convolutions = {'areal':areal_conv,
                        'upper':upper_conv,
                        'lower':lower_conv,
                        'lefty':lefty_conv,
                        'right':right_conv}
        if self.debug:      # If debugging, show the results of these filters
            utility.ImageProcessing.filter_preview(convolutions)
        # Look at the distribution and variation among/within the
        # various filter-applied image outputs
        aMax = np.max(areal_conv)
        uMax = np.max(upper_conv)
        dMax = np.max(lower_conv)
        lMax = np.max(lefty_conv)
        rMax = np.max(right_conv)
        if self.debug:
            print "Areal Max: " + str(aMax)
            print "Upper Max: " + str(uMax)
            print "Lower Max: " + str(dMax)
            print "Left  Max: " + str(lMax)
            print "Right Max: " + str(rMax)
        # Method 1
        # self.divide_and_conquer(areal_conv)
        # Method 2
        ii = 0
        test1 = np.zeros((areal_conv.shape[0]*areal_conv.shape[1]))
        SolidPoints = []
        EdgePoints = []
        for cell in areal_conv.flatten():
            if cell == 9:
                test1[ii] = -1
                SolidPoints.append(utility.ind2sub(ii,[self.image_input.shape[0], self.image_input.shape[1]]))
            if cell == 6:
                test1[ii] = 1
                EdgePoints.append(utility.ind2sub(ii,[self.image_input.shape[0], self.image_input.shape[1]]))
            ii += 1
        print str(len(SolidPoints)) + " Points in Image are 'solid' "
        print str(len(EdgePoints)) + " Points in Image look like edges"
        # Preview the Automata's work
        if self.debug:
            f, ax = plt.subplots(1, 2)
            ax[0].imshow(self.image_input, 'gray_r')
            ax[0].set_title('Test Image Input ')
            ax[1].imshow(test1.reshape(self.image_input.shape[0], self.image_input.shape[1]), 'gray_r')
            ax[1].set_title('<Edge Detection Output>')
            plt.show()
        return EdgePoints, SolidPoints

    def divide_and_conquer(self, image_in):
        dx = image_in.shape[0]
        dy = image_in.shape[1]
        div_x = np.arange(0, dx, 16)
        div_y = np.arange(0, dy, 16)
        print str(div_x.shape)+"\t"+str(div_y.shape)
        corners = {0: image_in[div_y[0]:div_y[1], div_x[0]:div_x[1]],
                   1: image_in[div_y[0]:div_y[1], div_x[1]:div_x[2]],
                   2: image_in[div_y[0]:div_y[1], div_x[2]:div_x[3]],
                   3: image_in[div_y[0]:div_y[1], div_x[3]:div_x[4]],
                   4: image_in[div_y[0]:div_y[1], div_x[4]:div_x[5]],
                   5: image_in[div_y[0]:div_y[1], div_x[5]:div_x[6]],
                   6: image_in[div_y[1]:div_y[2], div_x[0]:div_x[1]],
                   7: image_in[div_y[2]:div_y[3], div_x[0]:div_x[1]],
                   8: image_in[div_y[3]:div_y[4], div_x[0]:div_x[1]]}
        # Now Try and automate the rest
        c = 0
        for y in range(div_y.shape[0]):
            for x in range(div_x.shape[0]):
                if y != 0 and x != 0:   # Covers C9-C49 (out of 49)
                    corners[c] = image_in[div_x[y-1]:div_x[y],div_y[x-1]:div_y[x]]
                    print str(x)+','+str(y)
                c += 1
        print str(len(corners.keys())) + ' slices made'
        preview = {8:corners[8],2:corners[46]}
        utility.ImageProcessing.filter_preview(preview)
        return corners


def main():
    # Create some shapes to test edge detection on
    edge_detection_images = TestSuite(100,100)
    # Attempt some simple edge detection first
    test = EdgeDetection(edge_detection_images.basic)
    test.convolutional_automata_()
    # What about something more complex?
    test2 = EdgeDetection(edge_detection_images.medium)
    test2.convolutional_automata_()
    # How about something even more challenging?
    test3 = EdgeDetection(edge_detection_images.hard)
    test3.convolutional_automata_()
    # Ok Now for something really really challenging
    test4 = EdgeDetection(edge_detection_images.final)
    test4.convolutional_automata_()
    # Yeah so last case (full scale image) definitely wont work...
    # Seems like it's because the convolution kernel needs to grow
    # in relation to the size of the image!


if __name__ == '__main__':
    main()
