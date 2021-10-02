#include <stdio.h>
#include <opencv2/opencv.hpp>

#define WHITE_8 255
#define WHITE_16 65535
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

int main(int argc, char** argv)
{
    if ( argc != 4 )
    {
        std::cout << "usage: ./ccl invert input_image output_image" << std::endl;
        return -1;
    }

    // read input image & create output matrix of type 16-bit unsigned
    cv::Mat img = cv::imread(argv[2], 0);
    cv::imwrite("img.png", img); // TODO: remove
    if ( !img.data )
    {
        std::cout << "could not read image: " << argv[2] << std::endl;
        return -1;
    }
    cv::Mat labeled = cv::Mat::zeros(img.size(), 2);

    // define size once & for all
    int rows = img.rows;
    int cols = img.cols;
    uint8_t thold = WHITE_8/4;
    
    // optionally invert 0's & 1's
    if(atoi(argv[1]) == 1) {
        cv::Mat inv = img.clone();
        for(int r = 0; r < rows; ++r) {
            for(int c = 0; c < cols; ++c) {
                // 1 -> 0
                if(img.at<uint8_t>(r,c) > thold) {
                    inv.at<uint8_t>(r,c) = BLACK;
                }
                // 0 -> 1
                else {
                    inv.at<uint8_t>(r,c) = WHITE_8;
                }
            }
        }
        img = inv;
        cv::imwrite("inv.png", inv); // TODO: remove
    }

    // ensure image we handle is actually binary {0, 255}
    cv::Mat bin = img.clone();
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {
            uint8_t val;
            if(img.at<uint8_t>(r,c) < thold) { val = BLACK; }
            else { val = WHITE_8; }
            bin.at<uint8_t>(r,c) = val;
        }
    }
    img = bin;
    cv::imwrite("bin.png", bin); // TODO: remove

    int parent [65535];
    
    // 1st scan
    int cc = 0; // intermediate labels
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {
            // if pix 1 & connected
            if(img.at<uint8_t>(r,c) == WHITE_8 && (img.at<uint8_t>(r,c-1) == WHITE_8 || img.at<uint8_t>(r-1,c-1) == WHITE_8 || img.at<uint8_t>(r-1,c) == WHITE_8)) {
                // propogate label w precedence left, top-left, top
                if(img.at<uint8_t>(r,c-1) == WHITE_8) {
                    labeled.at<uint16_t>(r,c) = labeled.at<uint16_t>(r,c-1);
                }
                else if(img.at<uint8_t>(r-1,c-1) == WHITE_8) {
                    labeled.at<uint16_t>(r,c) = labeled.at<uint16_t>(r-1,c-1);
                }
                else {
                    labeled.at<uint16_t>(r,c) = labeled.at<uint16_t>(r-1,c);
                }
                // remember conflicting labels
                // left & top-left
                if(labeled.at<uint16_t>(r,c-1) != labeled.at<uint16_t>(r-1,c-1)) {
                    int p = std::min(labeled.at<uint16_t>(r,c-1),labeled.at<uint16_t>(r-1,c-1));
                    int c = std::max(labeled.at<uint16_t>(r,c-1),labeled.at<uint16_t>(r-1,c-1));
                    parent[c] = p;
                }
                // left & top
                if(labeled.at<uint16_t>(r,c-1) != labeled.at<uint16_t>(r-1,c)) {
                    int p = std::min(labeled.at<uint16_t>(r,c-1),labeled.at<uint16_t>(r-1,c));
                    int c = std::max(labeled.at<uint16_t>(r,c-1),labeled.at<uint16_t>(r-1,c));
                    parent[c] = p;
                }
                // top-left & top
                if(labeled.at<uint16_t>(r-1,c-1) != labeled.at<uint16_t>(r-1,c)) {
                    int p = std::min(labeled.at<uint16_t>(r-1,c-1),labeled.at<uint16_t>(r-1,c));
                    int c = std::max(labeled.at<uint16_t>(r-1,c-1),labeled.at<uint16_t>(r-1,c));
                    parent[c] = p;
                }
            }
            // if pix 1 & not connected
            else if(img.at<uint8_t>(r,c) == WHITE_8 && (img.at<uint8_t>(r,c-1) == BLACK && img.at<uint8_t>(r-1,c-1) == BLACK && img.at<uint8_t>(r-1,c) == BLACK)) {
                ++cc;
                labeled.at<uint16_t>(r,c) = cc;
            }
            // if 0
            else if(img.at<uint8_t>(r,c) == BLACK) {
                labeled.at<uint16_t>(r,c) = BLACK;
            }
        }
    }

    // 2nd scan
    for(int r = 0; r < rows; ++r) {
        for(int c = 0; c < cols; ++c) {

        }
    }
    
    cv::imwrite(argv[3], labeled);

    std::cout << "Statistics" << std::endl;
    std::cout << "Intermediate labels: " << cc << std::endl;

    // cv::namedWindow("CCL", cv::WINDOW_AUTOSIZE );
    // cv::imshow("CCL", gray);
    // cv::waitKey(0);

    return 0;
}