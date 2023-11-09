#include <iostream>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
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
        print("Image in color, converting to HSV");
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


    
    while ( waitKey(50) < 0 )          // attend une touche
    { // Affiche la valeur du slider
    if ( value != old_value )
    {
        old_value = value;
        std::cout << "value=" << value << std::endl;
    }
    }
} 