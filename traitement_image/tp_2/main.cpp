#include "opencv2/imgproc.hpp"
#include <opencv2/highgui.hpp>
using namespace cv;

cv::Mat filtreM(cv::Mat input, cv::Mat M) {
    cv::Mat result;
    cv::filter2D(input, result, -1, M, Point(-1, -1), 0, cv::BORDER_DEFAULT);
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
      if ( asciicode == 'q' ) break;
      imshow( "Youpi", modified_image );            // l'affiche dans la fenêtre
  }
  imwrite( "result.png", input );          // sauvegarde le résultat
}