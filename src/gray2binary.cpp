#include <stdio.h>
#include <opencv2/opencv.hpp>

int main(int argc, char** argv )
{
    if ( argc != 5 )
    {
        std::cout << "usage: ./gray2binary input_grayscale_image_filename output_binary_image_filename threshold_value input_ground_truth_image" << std::endl;
        return -1;
    }
    cv::Mat image;
    image = cv::imread( argv[1], 1 );
    if ( !image.data )
    {
        printf("No image data \n");
        return -1;
    }
    
    
    return 0;
}