#include <stdio.h>
#include <opencv2/opencv.hpp>

#define WHITE 255
#define BLACK 0

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
    cv::Mat labeled = cv::Mat::zeros(img.size(), 0); // 2 = CV_16U

    // define size once & for all
    int rows = img.rows;
    int cols = img.cols;
    uint8_t thold = WHITE/4; // also threshold for some stuff
    
    // optionally invert 0's & 1's
    if(atoi(argv[1]) == 1) {
        cv::Mat inv = cv::Mat::zeros(img.size(), 0);
        for(int r = 0; r < rows; ++r) {
            for(int c = 0; c < cols; ++c) {
                // 1 -> 0
                if(img.at<uint8_t>(r,c) > thold) {
                    inv.at<uint8_t>(r,c) = BLACK;
                }
                // 0 -> 1
                else {
                    inv.at<uint8_t>(r,c) = WHITE;
                }
            }
        }
        img = inv;
    }

    // ensure image we handle is actually binary {0, 65535}, threshold at mid point
    cv::Mat bin = cv::Mat::zeros(img.size(), 0);
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {
            uint8_t val;
            if(img.at<uint8_t>(r,c) < thold) { val = BLACK; }
            else { val = WHITE; }
            bin.at<uint8_t>(r,c) = val;
        }
    }
    img = bin;

    int parent [2048];
    
    // 1st scan
    int cc = 0;
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {
            // if pix 1 & connected
            if(img.at<uint8_t>(r,c) == WHITE && (img.at<uint8_t>(r,c-1) == WHITE || img.at<uint8_t>(r-1,c-1) == WHITE || img.at<uint8_t>(r-1,c) == WHITE)) {
                // propogate label
                if(img.at<uint8_t>(r,c-1) == WHITE) {
                    labeled.at<uint8_t>(r,c) = labeled.at<uint8_t>(r,c-1);
                }
                else if(img.at<uint8_t>(r-1,c-1) == WHITE) {
                    labeled.at<uint8_t>(r,c) = labeled.at<uint8_t>(r-1,c-1);
                }
                else {
                    labeled.at<uint8_t>(r,c) = labeled.at<uint8_t>(r-1,c);
                }
            }
            // if pix 1 & not connected
            else if(img.at<uint8_t>(r,c) == WHITE && (img.at<uint8_t>(r,c-1) == BLACK && img.at<uint8_t>(r-1,c-1) == BLACK && img.at<uint8_t>(r-1,c) == BLACK)) {
                ++cc;
                labeled.at<uint8_t>(r,c) = cc;
                // labeled.at<uint8_t>(r,c) = WHITE/2; // TODO: remove this is just for testing
            }
            // if 0
            else if(img.at<uint8_t>(r,c) == BLACK) {
                labeled.at<uint8_t>(r,c) = BLACK;
            }
        }
    }
    
    cv:imwrite(argv[3], labeled);

    std::cout << "Statistics" << std::endl;
    std::cout << "Intermediate labels: " << cc << std::endl;

    // cv::namedWindow("CCL", cv::WINDOW_AUTOSIZE );
    // cv::imshow("CCL", gray);
    // cv::waitKey(0);

    return 0;
}