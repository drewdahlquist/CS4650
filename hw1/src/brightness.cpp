#include <stdio.h>
#include <opencv2/opencv.hpp>

int main(int argc, char** argv )
{
    if ( argc != 4 )
    {
        std::cout << "usage: ./brightness intensity_value input_image_filename output_image_filename" << std::endl;
        return -1;
    }

    // read input image & create 0 image for output
    cv::Mat img = cv::imread(argv[2], 0);
    if ( !img.data )
    {
        std::cout << "could not read image: " << argv[2] << std::endl;
        return -1;
    }
    cv::Mat bright = cv::Mat::zeros(img.size(), 0);

    int brightness = atoi(argv[1]);

    // do our computation for brightness
    int rows = img.rows;
    int cols = img.cols;
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {
            int val = img.at<uint8_t>(r,c) + brightness;
            if(val < 0) {
                val = 0;
            }
            else if(val > 255) {
                val = 255;
            }
            bright.at<uint8_t>(r,c) = val;
        }
    }
    
    cv:imwrite(argv[3], bright);
    
    return 0;
}