  #include "opencv2/imgproc.hpp"
  #include <opencv2/highgui.hpp>
  #include <iostream>
  using namespace cv;



  cv::Mat filtreM(cv::Mat input, cv::Mat M, int delta = 0) {
      cv::Mat result;
      cv::flip(M, M, 1);
      // input.convertTo(result, CV_32FC1);
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

  cv::Mat laplacien(cv::Mat input,int nb_iteration,float coef, int delta = 0)
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
      modified_image = filtreM(modified_image, filter, delta);
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

  bool contour(cv::Mat lap, int i, int j)
  {
    //verifie si il y a des + et des - dans le voisinage (3x3) de i,j du lap
    int nb_pos = 0;
    int nb_neg = 0;
    // std::cout << "enter func" << std::endl;
    for(int k = i-1; k <= i+1; k++)
    {
      // std::cout << "loop k " << k << std::endl;
      for(int l = j-1; l <= j+1; l++)
      {
        // std::cout << "loop l " << l << std::endl;
        if (k >= 0 && k < lap.rows && l >= 0 && l < lap.cols)
        {
          if(lap.at<uchar>(k,l) >128)
          {
            nb_pos++;
          }
          else if(lap.at<uchar>(k,l) < 128)
          {
            nb_neg++;
          }
        }
        // else{
        //   std::cout<<"out of bounds - "<< k << " - " << l << std::endl;
        // }
      }
    }
    // std::cout << nb_pos << "+ " << nb_neg <<"-" << std::endl;
    return (nb_pos > 0 && nb_neg > 0);
  }

  cv::Mat laplacianThreshold(const cv::Mat input, int tr) {
      // Appliquer le filtre Laplacien
      cv::Mat res = cv::Mat::zeros(input.rows, input.cols, input.type());
      cv::Mat lap = laplacien(input, 1, 3, 128);
      cv::Mat grad = gradient(sobel_x(input), sobel_y(input));

      // Trouver les points où le Laplacien change de signe
      for (int i = 0; i < lap.rows; i++) {
          for (int j = 0; j < lap.cols; j++) {
              if(contour(lap, i, j) && grad.at<uchar>(i,j) >= tr)
              {
                res.at<uchar>(i,j) = 0;
              }
              else{
                res.at<uchar>(i,j) = 255;
              }
          }
      }

      return res;
  }

  #include <cmath>

cv::Mat artisticRendering(cv::Mat input, cv::Mat colors, int threshold, int proportion, int length) {
    cv::Mat lap = laplacien(input, 1, 3, 128);
    cv::Mat sob_x = sobel_x(input);
    cv::Mat sob_y = sobel_y(input);
    cv::Mat grad = gradient(sob_x, sob_y);

    cv::Mat output = input.clone();
    cv::cvtColor(input, output, COLOR_GRAY2RGB);

    for (int i = 0; i < input.rows; i++) {
        for (int j = 0; j < input.cols; j++) {
            output.at<cv::Vec3b>(i, j)[0] = 255;
            output.at<cv::Vec3b>(i, j)[1] = 255;
            output.at<cv::Vec3b>(i, j)[2] = 255;
            if (contour(lap, i, j) && grad.at<uchar>(i, j) >= threshold) {
                if (rand() / (double)RAND_MAX < proportion / 100.0) {
                    double theta = atan2(sob_y.at<uchar>(i, j) - 128, sob_x.at<uchar>(i, j) - 128) + CV_PI / 2 + 0.02 * (rand() / (double)RAND_MAX - 0.5);
                    double grayLevel = input.at<uchar>(i, j) / 255.0 * length / 100.0;
                    cv::line(output,
                        cv::Point(j + grayLevel * cos(theta), i + grayLevel * sin(theta)),
                        cv::Point(j - grayLevel * cos(theta), i - grayLevel * sin(theta)),
                        //color is color of pixel at (i,j) 
                        cv::Scalar((int)colors.at<cv::Vec3b>(i, j)[0],
                                  (int)colors.at<cv::Vec3b>(i, j)[1],
                                  (int)colors.at<cv::Vec3b>(i, j)[2]),1);
                }
            }
        }
    }

    return output;
}


  int main( int argc, char* argv[])
  {
    namedWindow( "Youpi");               // crée une fenêtre
    Mat input = imread( argv[ 1 ] );     // lit l'image donnée en paramètre

    cv::Mat colors = input.clone();
    //convert color to rgb
    cv::cvtColor(colors, colors, COLOR_BGR2RGB);

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
        if(asciicode == 't')
        {
          modified_image = laplacianThreshold(modified_image, 20);
        }
        if(asciicode =='r')
        {
          modified_image = input.clone();
        }
        if (asciicode == 'e') {
          modified_image = artisticRendering(modified_image,colors, 20, 20, 1000);
        }
        if ( asciicode == 'q' ) break;
        imshow( "Youpi", modified_image );            // l'affiche dans la fenêtre
    }
    imwrite( "result.png", input );          // sauvegarde le résultat
  }