#include <stdio.h>
#include <opencv2/opencv.hpp>

int main(int argc, char** argv )
{
    if ( argc != 3 )
    {
        std::cout << "usage: ./rgb2gray input_color_image_filename output_grayscale_image_filename" << std::endl;
        return -1;
    }

    cv::Mat img = cv::imread( argv[1], 1 );
    if ( !img.data )
    {
        std::cout << "could not read image: " << argv[1] << std::endl;
        return -1;
    }
    
    uint8_t rows = img.rows;
    uint8_t cols = img.cols;
    for(uint8_t r = 0; r < rows; ++r) {
        for(uint8_t c = 0; c < cols; ++c) {
            img.at<uchar>(r, c) = 0;
        }
    }
    
    cv::namedWindow("rgb2gray", cv::WINDOW_AUTOSIZE );
    cv::imshow("rgb2gray", img);
    cv::waitKey(0);

    return 0;
}