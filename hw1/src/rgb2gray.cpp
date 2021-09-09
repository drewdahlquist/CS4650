#include <stdio.h>
#include <opencv2/opencv.hpp>

int main(int argc, char** argv )
{
    if ( argc != 3 )
    {
        std::cout << "usage: ./rgb2gray input_color_image_filename output_grayscale_image_filename" << std::endl;
        return -1;
    }

    // read input image & create 0 image for output
    cv::Mat img = cv::imread(argv[1], 1);
    if ( !img.data )
    {
        std::cout << "could not read image: " << argv[1] << std::endl;
        return -1;
    }
    cv::Mat gray = cv::Mat::zeros(img.size(), 0);
    
    // do our computation for rbg (really it's bgr) -> grayscale
    int rows = img.rows;
    int cols = img.cols;
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {
            float val = 0.1140*img.at<cv::Vec3b>(r,c)[0] + 0.5871*img.at<cv::Vec3b>(r,c)[1] + 0.2989*img.at<cv::Vec3b>(r,c)[2];
            if(val < 0) { val = 0; }
            else if(val > 255) { val = 255; }
            gray.at<uint8_t>(r,c) = val;
        }
    }
    
    cv:imwrite(argv[2], gray);

    // cv::namedWindow("rgb2gray", cv::WINDOW_AUTOSIZE );
    // cv::imshow("rgb2gray", gray);
    // cv::waitKey(0);

    return 0;
}