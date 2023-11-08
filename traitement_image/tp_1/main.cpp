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
    int V = 255;

    std::vector<double> h_I(V, 0);

    for (int i = 0; i < image.rows; i++)
    {
        for (int j = 0; j < image.cols; j++)
        {
            h_I[image.at<uchar>(i,j)]++;
        }
    }

    for(int i = 0; i < V; i++)
    {
        h_I[i] = h_I[i] / (image.rows * image.cols);
    }

    return h_I;
}

std::vector<double> histogramme_cumule( const std::vector<double>& h_I )
{
    int V = 255;
    std::vector<double> H_I(V, 0);
    H_I[0] = h_I[0];
    for(int i = 1; i < V; i++)
    {
        H_I[i] += h_I[i] + H_I[i-1];
    }
    return H_I;
}

cv::Mat afficheHistogrammes( const std::vector<double>& h_I,
                             const std::vector<double>& H_I )
{
    cv::Mat image( 256, 512, CV_8UC1 );
    image.setTo( 255 );

    // On recherche de la valeur maximale de l'histogramme
    double max = 0.0;
    print("coucou");
    for ( int i = 0; i < h_I.size(); i++ )
        if ( h_I[i] > max )
        //On stocke la valeur maximale
        max = h_I[i];

    print("coucou 2 ");
    // Tracé de l'histogramme h_I
    for ( int i = 0; i < h_I.size(); i++ )
    {
        int x = i;
        for ( int y = 255; y > 255 - (h_I[i] / max) * 255; y-- )
        image.at<uchar>(y,x) = 0;
    }
    print(" coucou3");
    // Tracé de l'histogramme H_I
    for ( int i = 0; i < H_I.size(); i++ )
    {
        int x = i + 256;
        // Colorier en bas du point
        for ( int y = 255; y > 255 - (H_I[i] / H_I.back()) * 255; y-- )
        image.at<uchar>(y,x) = 0;
    }
    print("done");

    return image;
}

// ---------------------------------
// ------------ MAIN ---------------
// ---------------------------------

int main(int argc, char *argv[])
{



    int old_value = 0;
    int value = 128;
    //read parameters from command line

    if (argc < 1)
    {
        //print "usage: prog_name <image_path>"
        print("usage: main <image_path>");
        return 1;
    }
    
    char* image_path = argv[1]; 

    namedWindow( "TP1");               // crée une fenêtre
    createTrackbar( "track", "TP1", &value, 255, NULL); // un slider
    Mat f = imread(image_path);        // lit l'image


    //check if image is in grayscale
    if (f.channels() != 1)
    {
        //convert to grayscale
        print("Image not in grayscale, converting to grayscale");
        cvtColor(f, f, COLOR_BGR2GRAY);
    }

    imshow( "TP1", f );                // l'affiche dans la fenêtre
    // std::vector<double> h = histogramme(f);
    //std::vector<double> H = histogramme_cumule(h);
    namedWindow( "Histogramme");
    Mat hist = afficheHistogrammes( histogramme(f), histogramme_cumule(histogramme(f)) );
    imshow( "Histogramme", hist );
    while ( waitKey(50) < 0 )          // attend une touche
    { // Affiche la valeur du slider
    if ( value != old_value )
    {
        old_value = value;
        std::cout << "value=" << value << std::endl;
    }
    }
} 