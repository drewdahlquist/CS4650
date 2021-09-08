#include <stdio.h>
#include <opencv2/opencv.hpp>

int main(int argc, char** argv )
{
    if ( argc != 5 )
    {
        std::cout << "usage: ./gray2binary input_grayscale_image_filename output_binary_image_filename threshold_value input_ground_truth_image" << std::endl;
        return -1;
    }
    
    // read input image & create 0 image for output
    cv::Mat img = cv::imread(argv[1], 0);
    if ( !img.data )
    {
        std::cout << "could not read image: " << argv[1] << std::endl;
        return -1;
    }
    cv::Mat bin = cv::Mat::zeros(img.size(), 0);
    
    // do our computation for grayscale -> binary
    int rows = img.rows;
    int cols = img.cols;
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {
            uint8_t val;
            if(img.at<uint8_t>(r,c) < atoi(argv[3])) { val = 0; }
            else { val = 255; }
            bin.at<uint8_t>(r,c) = val;
        }
    }
    
    cv:imwrite(argv[2], bin);

    // cv::namedWindow("gray2binary", cv::WINDOW_AUTOSIZE );
    // cv::imshow("gray2binary", bin);
    // cv::waitKey(0);

    return 0;
}