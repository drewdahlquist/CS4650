#include <stdio.h>
#include <opencv2/opencv.hpp>

int main(int argc, char** argv )
{
    if ( argc != 4 )
    {
        std::cout << "usage: ./brightness intensity_value input_image_filename output_image_filename" << std::endl;
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