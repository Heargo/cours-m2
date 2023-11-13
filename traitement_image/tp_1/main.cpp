#include <iostream>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <vector>

using namespace cv;

// ---------------------------------
// ------------ UTILS --------------
// ---------------------------------

void print(char str[])
{
    std::cout << str << std::endl;
}


// ---------------------------------
// ----------- HISTOGRAM -----------
// ---------------------------------


std::vector<double> histogramme( Mat image )
{
  int nbPixel = image.rows * image.cols;
  std::vector<double> histo( 256, 0.0 );

  for ( int y = 0; y < image.rows; y++ )
    for ( int x = 0; x < image.cols; x++ )
      histo[ image.at<uchar>(y,x) ] += 1.0/nbPixel;

  return histo;
} 

std::vector<double> histogramme_cumule( const std::vector<double>& h_I )
{
    int V = h_I.size();
    std::vector<double> H_I(V, 0);
    H_I[0] = h_I[0];

    for(int i = 1; i < V; i++)
        H_I[i] += h_I[i] + H_I[i-1];

    return H_I;
}

cv::Mat afficheHistogrammes( const std::vector<double>& h_I,
                             const std::vector<double>& H_I )
{
    cv::Mat image( 256, 512, CV_8UC1 );
    image.setTo( 255 );

    // On recherche de la valeur maximale de l'histogramme
    double max = 0.0;
    for ( int i = 0; i < h_I.size(); i++ )
        if ( h_I[i] > max )
        //On stocke la valeur maximale
        max = h_I[i];

    // Tracé de l'histogramme h_I
    for ( int i = 0; i < h_I.size(); i++ )
    {
        int x = i;
        for ( int y = 255; y > 255 - (h_I[i] / max) * 255; y-- )
        image.at<uchar>(y,x) = 0;
    }
    // Tracé de l'histogramme H_I
    for ( int i = 0; i < H_I.size(); i++ )
    {
        int x = i + 256;
        // Colorier en bas du point
        for ( int y = 255; y > 255 - (H_I[i] / H_I.back()) * 255; y-- )
        image.at<uchar>(y,x) = 0;
    }
    return image;
}


cv::Mat egalisation_histogramme( const cv::Mat& image )
{
    std::vector<double> h_I = histogramme(image);
    std::vector<double> H_I = histogramme_cumule(h_I);
    cv::Mat image_egalisee(image.rows, image.cols, CV_8UC1);
    for(int i = 0; i < image.rows; i++)
    {
        for(int j = 0; j < image.cols; j++) 
        {
            //colorier le pixel (i,j) de l'image egalisee avec la valeur de l'histogramme cumule
            int val = H_I[image.at<uchar>(i,j)] * H_I.size();
            image_egalisee.at<uchar>(i,j) = val;
        }   
    }
    return image_egalisee;
}

// ---------------------------------
// ----------- TRAMAGE -------------
// ---------------------------------

cv::Mat tramage_floyd_steinberg(const cv::Mat& input) {
    // Convert the input image to a floating-point type
    cv::Mat inputFloat;
    input.convertTo(inputFloat, CV_32FC1);

    // Clone the input image to store the result
    cv::Mat output = inputFloat.clone();

    for (int y = 0; y < inputFloat.rows; ++y) {
        for (int x = 0; x < inputFloat.cols; ++x) {
            // Get the current pixel value
            float oldPixel = output.at<float>(y, x);
            float newPixel = oldPixel > 128 ? 255 : 0;
            // Calculate the quantization error
            float error = oldPixel  - newPixel;

            // Update the current pixel value
            output.at<float>(y, x) = newPixel;

            // Propagate the error to neighbors
            if (x + 1 < inputFloat.cols) {
                output.at<float>(y, x + 1) += error * 7 / 16;
            }
            if (x - 1 >= 0 && y + 1 < inputFloat.rows) {
                output.at<float>(y + 1, x - 1) += error * 3 / 16;
            }
            if (y + 1 < inputFloat.rows) {
                output.at<float>(y + 1, x) += error * 5 / 16;
            }
            if (x + 1 < inputFloat.cols && y + 1 < inputFloat.rows) {
                output.at<float>(y + 1, x + 1) += error * 1 / 16;
            }
            
        }
    }

    // Convert the output image back to the uchar type
    cv::Mat outputUchar;
    output.convertTo(outputUchar, CV_8UC1, 255.0);

    return outputUchar;
}


// Function to calculate distance between two colors
float distance_color_l2(cv::Vec3f bgr1, cv::Vec3f bgr2) {
    return cv::norm(bgr1, bgr2, cv::NORM_L2);
}

// Function to find the index of the color closest to the given color in the vector of colors
int best_color(cv::Vec3f bgr, std::vector<cv::Vec3f> colors) {
    int bestIndex = 0;
    float minDistance = distance_color_l2(bgr, colors[0]);

    for (int i = 1; i < colors.size(); ++i) {
        float distance = distance_color_l2(bgr, colors[i]);
        if (distance < minDistance) {
            minDistance = distance;
            bestIndex = i;
        }
    }

    return bestIndex;
}

// Function to calculate the error vector between two colors
cv::Vec3f error_color(cv::Vec3f bgr1, cv::Vec3f bgr2) {
    return bgr1 - bgr2;
}

// Function for CMYK halftoning using Floyd-Steinberg algorithm
cv::Mat tramage_floyd_steinberg_cmyk(const cv::Mat& input, std::vector<cv::Vec3f> colors) {
    // Convert input image to a matrix of 3-channel floating-point values
    cv::Mat fs;
    input.convertTo(fs, CV_32FC3, 1 / 255.0);

    // Floyd-Steinberg algorithm
    for (int y = 0; y < fs.rows; ++y) {
        for (int x = 0; x < fs.cols; ++x) {
            cv::Vec3f currentColor = fs.at<cv::Vec3f>(y, x);
            int index = best_color(currentColor, colors);
            cv::Vec3f error = error_color(currentColor, colors[index]);
            fs.at<cv::Vec3f>(y, x) = colors[index];

            // Propagate the error to neighbors
            if (x + 1 < fs.cols) {
                fs.at<cv::Vec3f>(y, x + 1) += error * (7.0 / 16.0);
            }
            if (x - 1 >= 0 && y + 1 < fs.rows) {
                fs.at<cv::Vec3f>(y + 1, x - 1) += error * (3.0 / 16.0);
            }
            if (y + 1 < fs.rows) {
                fs.at<cv::Vec3f>(y + 1, x) += error * (5.0 / 16.0);
            }
            if (x + 1 < fs.cols && y + 1 < fs.rows) {
                fs.at<cv::Vec3f>(y + 1, x + 1) += error * (1.0 / 16.0);
            }
        }
    }
    // Convert the matrix of 3-channel floating-point values back to BGR
    cv::Mat output;
    fs.convertTo(output, CV_8UC3, 255.0);
    return output;
}

// ---------------------------------
// ------------ MAIN ---------------
// ---------------------------------

int main(int argc, char *argv[])
{



    int old_value = 0;
    int value = 128;
    int mode = 0; //0, gray, 1, color

    if (argc < 1)
    {
        //print "usage: prog_name <image_path>"
        print("usage: main <image_path> <color (boolean) (optional)>");
        return 1;
    }
    if(argc == 3) 
    {
        mode = 1;
    }
    
    char* image_path = argv[1]; 

    namedWindow( "TP1");               // crée une fenêtre
    createTrackbar( "track", "TP1", &value, 255, NULL); // un slider
    Mat image = imread(image_path);        // lit l'image
    Mat f = image.clone(); //copy image to f
    std::vector<Mat> channels;

    //check if image is in grayscale
    if (image.channels() != 1 && mode == 0)
    {
        //convert to grayscale
        print("Image not in grayscale, converting to grayscale");
        cvtColor(image, image, COLOR_BGR2GRAY);
        cvtColor(f, f, COLOR_BGR2GRAY);
    }

    if(mode==1){
        //convert to HSV
        cvtColor(f, f, COLOR_BGR2HSV);
        //get V channel from image
        split(f, channels);
        f = channels[2];
    }
    //base image
    imshow( "TP1", image );
    //histogramme of base image
    namedWindow( "Histogramme");

    Mat hist = afficheHistogrammes( histogramme(f) , histogramme_cumule(histogramme(f)) );
    imshow( "Histogramme", hist );

    //modified image
    Mat img = egalisation_histogramme(f);
    
    //histogramme of modified image
    Mat hist_modif = afficheHistogrammes( histogramme(img), histogramme_cumule(histogramme(img)) );
    namedWindow( "Histogramme egalise" );
    imshow( "Histogramme egalise", hist_modif );

    namedWindow( "Image egalise");
    if(mode==1){
        //merge channels
        channels[2] = img;
        merge(channels, img);
        //convert to HSV
        cvtColor(img, img, COLOR_HSV2BGR);
    }

    imshow( "Image egalise", img );

    // tramage
    
    Mat tramage;

    if(mode==1){
        //split channels
        // split(image, channels);

        // for(int i = 0; i < channels.size(); i++)
        //     channels[i] = tramage_floyd_steinberg(channels[i]);

        // merge(channels, tramage);

        //WITH CMYK
        // Define CMYK colors (from BGR)
        std::vector<cv::Vec3f> cmykColors = {
            cv::Vec3f(0.0, 0.0, 0.0),  // Black 
            cv::Vec3f(1.0, 1.0, 1.0),  // white
            cv::Vec3f(1.0, 0.0, 1.0),  // Majenta
            cv::Vec3f(0.0, 1.0, 1.0),  // Yellow
            cv::Vec3f(1.0, 1.0, 0.0)   // Cyan
        };
        // Apply CMYK halftoning
        tramage = tramage_floyd_steinberg_cmyk(image, cmykColors);
    }else{
        tramage = tramage_floyd_steinberg(image);
    }

    namedWindow( "Tramage");
    imshow( "Tramage", tramage );



    
    while ( waitKey(50) < 0 )          // attend une touche
    { // Affiche la valeur du slider
    if ( value != old_value )
    {
        old_value = value;
        std::cout << "value=" << value << std::endl;
    }
    }
} 