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
    cv::Mat img = cv::imread(argv[1], 0); // input image
    cv::Mat gt = cv::imread(argv[4], 0); // ground truth image
    if ( !img.data || !gt.data )
    {
        std::cout << "could not read image: " << argv[1] << " and/or " << argv[4] << std::endl;
        return -1;
    }
    cv::Mat bin = cv::Mat::zeros(img.size(), 0);

    // counting
    int tpos, tneg, fpos, fneg = 0;
    
    // do our computation for grayscale -> binary
    int rows = img.rows;
    int cols = img.cols;
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {
            uint8_t val;
            if(img.at<uint8_t>(r,c) < atoi(argv[3])) { val = 0; }
            else { val = 255; }
            bin.at<uint8_t>(r,c) = val;
            
            // true pos
            if(bin.at<uint8_t>(r,c) == 255 && bin.at<uint8_t>(r,c) == gt.at<uint8_t>(r,c)) {
                ++tpos;
            }
            // true neg
            else if(bin.at<uint8_t>(r,c) == 0 && bin.at<uint8_t>(r,c) == gt.at<uint8_t>(r,c)) {
                ++tneg;
            }
            // false pos
            else if(bin.at<uint8_t>(r,c) == 255 && bin.at<uint8_t>(r,c) != gt.at<uint8_t>(r,c)) {
                ++fpos;
            }
            // false neg
            else {
                ++fneg;
            }
        }
    }
    
    cv:imwrite(argv[2], bin);

    // report stats
    std::cout << "True Pos  : " << tpos << std::endl;
    std::cout << "True Neg  : " << tneg << std::endl;
    std::cout << "False Pos : " << fpos << std::endl;
    std::cout << "False Neg : " << fneg << std::endl;

    // cv::namedWindow("gray2binary", cv::WINDOW_AUTOSIZE );
    // cv::imshow("gray2binary", bin);
    // cv::waitKey(0);

    return 0;
}