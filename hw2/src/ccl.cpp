#include <stdio.h>
#include <opencv2/opencv.hpp>

int ccl_find(int parent[], int i)
{
    if (parent[i] == -1)
        return i;
    return ccl_find(parent, parent[i]);
}

void ccl_union(int parent[], int x, int y)
{
    int xset = ccl_find(parent, x);
    int yset = ccl_find(parent, y);
    parent[xset] = yset;
}

int main(int argc, char** argv )
{
    if ( argc != 4 )
    {
        std::cout << "usage: ./ccl invert input_image output_image" << std::endl;
        return -1;
    }

    // read input image & create 0 image for output
    cv::Mat img = cv::imread(argv[2], 0);
    if ( !img.data )
    {
        std::cout << "could not read image: " << argv[2] << std::endl;
        return -1;
    }
    cv::Mat labeled = cv::Mat::zeros(img.size(), 0);
    
    // invert 0's & 1's
    if(atoi(argv[1]) == 1) {
        cv::Mat inv = cv::Mat::zeros(img.size(), 0);
        int rows = img.rows;
        int cols = img.cols;
        for(int r = 0; r < rows; ++r) {
            for(int c = 0; c < cols; ++c) {
                // 1 -> 0
                if(img.at<uint8_t>(r,c) == 255) {
                    inv.at<uint8_t>(r,c) = 0;
                }
                // 0 -> 1
                else {
                    inv.at<uint8_t>(r,c) = 255;
                }
            }
        }
        img = inv;
    }

    int parent [2048];
    
    // 1st scan
    int rows = img.rows;
    int cols = img.cols;
    int cc = 0;
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {
            // if pix 1 & connected
            if(img.at<uint8_t>(r,c) == 255 && (img.at<uint8_t>(r,c-1) != 0 || img.at<uint8_t>(r-1,c-1) != 0 || img.at<uint8_t>(r-1,c) != 0)) {
                labeled.at<uint8_t>(r,c) = std::min(std::min(img.at<uint8_t>(r,c-1), img.at<uint8_t>(r-1,c-1)), img.at<uint8_t>(r-1,c)); // propogate min label
            }
            // if pix 1 & not connected
            else if(img.at<uint8_t>(r,c) == 255 && (img.at<uint8_t>(r,c-1) == 0 || img.at<uint8_t>(r-1,c-1) == 0 || img.at<uint8_t>(r-1,c) == 0)) {
                ++cc;
                labeled.at<uint8_t>(r,c) = cc;
            }
            // if 0
            else if(img.at<uint8_t>(r,c) == 0) {
                labeled.at<uint8_t>(r,c) = 0;
            }
        }
    }
    
    cv:imwrite(argv[3], img);

    // cv::namedWindow("CCL", cv::WINDOW_AUTOSIZE );
    // cv::imshow("CCL", gray);
    // cv::waitKey(0);

    return 0;
}