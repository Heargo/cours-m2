#include "opencv2/imgproc.hpp"
#include <opencv2/highgui.hpp>
#include <iostream>
using namespace cv;

cv::Mat filtreM(cv::Mat input, cv::Mat M, int delta = 0) {
    cv::Mat result;
    cv::flip(M, M, 1);
    cv::filter2D(input, result, -1, M, Point(-1, -1), delta, cv::BORDER_DEFAULT);
    return result;
}

cv::Mat blur(cv::Mat input,int nb_iteration)
{
  // Définition du filtre moyenneur M
  cv::Mat M = (cv::Mat_<float>(3, 3) << 
              1/9.0, 1/9.0, 1/9.0, 
              1/9.0, 1/9.0, 1/9.0, 
              1/9.0, 1/9.0, 1/9.0
              );

  Mat modified_image = input.clone();

  for (int i=0;i<nb_iteration;i++){
    modified_image = filtreM(modified_image, M);
  }

  return modified_image;
}

cv::Mat laplacien(cv::Mat input,int nb_iteration,float coef)
{
  // Définition du filtre moyenneur M
  cv::Mat M = (cv::Mat_<float>(3, 3) << 
              0.0, 1.0, 0.0, 
              1.0, -4.0, 1.0, 
              0.0, 1.0, 0.0
              );
              
  cv::Mat dirac =(cv::Mat_<float>(3, 3) << 
              0.0, 0.0, 0.0, 
              0.0, 1.0, 0.0, 
              0.0, 0.0, 0.0
              );

  Mat modified_image = input.clone();

  cv::Mat filter = dirac - coef*M;

  for ( int i=0; i < nb_iteration; i++ )
  {
    modified_image = filtreM(modified_image, filter);
  }

  return modified_image;
}

cv::Mat sobel_x(cv::Mat input)
{
  cv::Mat M = (cv::Mat_<float>(3, 3) << 
              1.0, 0.0, -1.0, 
              2.0, 0.0, -2.0, 
              1.0, 0.0, -1.0
              )/4.0;

  return filtreM(input, M, 128);

}


cv::Mat sobel_y(cv::Mat input)
{
  cv::Mat M = (cv::Mat_<float>(3, 3) << 
              -1.0, -2.0, -1.0, 
              0.0, 0.0, 0.0, 
              1.0, 2.0, 1.0
              )/4.0;


  return filtreM(input, M, 128);
}

cv::Mat gradient(cv::Mat i_x, cv::Mat i_y)
{
  cv::Mat result = cv::Mat::zeros(i_x.rows, i_x.cols, i_x.type());
  for (int i = 0; i < i_x.rows; i++)
  {
    for (int j = 0; j < i_x.cols; j++)
    {
      result.at<uchar>(i,j) = cv::saturate_cast<uchar>(sqrt(pow(i_x.at<uchar>(i,j) - 128 ,2) + pow(i_y.at<uchar>(i,j) - 128,2)));
    }
  }
  return result;
}


int main( int argc, char* argv[])
{
  namedWindow( "Youpi");               // crée une fenêtre
  Mat input = imread( argv[ 1 ] );     // lit l'image donnée en paramètre

  
  if ( input.channels() == 3 )
    cv::cvtColor( input, input, COLOR_BGR2GRAY );

  Mat modified_image = input.clone();

  while ( true ) {
      int keycode = waitKey( 50 );
      int asciicode = keycode & 0xff;
      if ( asciicode == 'a')
      {
        modified_image = blur(modified_image, 1);
      }
      if ( asciicode == 'm' )
      {
        medianBlur(modified_image, modified_image, 3);
      }
      if ( asciicode == 'l' )
      {
        modified_image = laplacien(modified_image, 1, 0.6);
      }
      if( asciicode == 'x' )
      {
        modified_image = sobel_x(modified_image);
      }
      if( asciicode == 'y' )
      {
        modified_image = sobel_y(modified_image);
      }
      if(asciicode == 'g')
      {
        modified_image = gradient(sobel_x(modified_image), sobel_y(modified_image));
      }
      if(asciicode =='r')
      {
        modified_image = input.clone();
      }
      if ( asciicode == 'q' ) break;
      imshow( "Youpi", modified_image );            // l'affiche dans la fenêtre
  }
  imwrite( "result.png", input );          // sauvegarde le résultat
}