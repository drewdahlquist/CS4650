#include <stdio.h>
#include <opencv2/opencv.hpp>

int main(int argc, char** argv )
{
    if ( argc != 5 )
    {
        std::cout << "usage: ./contrast min_value max_value input_image_filename output_image_filename" << std::endl;
        return -1;
    }
    
    // read input image & create 0 image for output
    cv::Mat img = cv::imread(argv[3], 0);
    if ( !img.data )
    {
        std::cout << "could not read image: " << argv[2] << std::endl;
        return -1;
    }
    cv::Mat cont = cv::Mat::zeros(img.size(), 0);

    int min = atoi(argv[1]);
    int max = atoi(argv[2]);
    float slope = max - min; // ???

    // do our computation for contrast
    int rows = img.rows;
    int cols = img.cols;
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {
            int val = img.at<uint8_t>(r,c) * slope;
            if(val < 0) {
                val = 0;
            }
            else if(val > 255) {
                val = 255;
            }
            cont.at<uint8_t>(r,c) = val;
        }
    }
    
    cv:imwrite(argv[4], cont);
    
    return 0;
}