#include <cstdio>
#include <iostream>
#include <algorithm>
#include <opencv2/core/utility.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

using namespace cv;
using namespace std;

struct ColorDistribution {
  float data[ 8 ][ 8 ][ 8 ]; // l'histogramme
  int nb;                     // le nombre d'échantillons
    
  ColorDistribution() { reset(); }
  ColorDistribution& operator=( const ColorDistribution& other ) = default;
  // Met à zéro l'histogramme    
  void reset()
  {
      nb = 0;

      for (int i = 0; i < 8; ++i) {
          for (int j = 0; j < 8; ++j) {
              for (int k = 0; k < 8; ++k) {
                  data[i][j][k] = 0.0;
              }
          }
      }
  }

  void add(Vec3b color)
  {
      int i = color[0] / 32; // R channel
      int j = color[1] / 32; // G channel
      int k = color[2] / 32; // B channel

      // Ensure that indices are within bounds
      i = std::max(0, std::min(i, 7));
      j = std::max(0, std::min(j, 7));
      k = std::max(0, std::min(k, 7));

      data[i][j][k] += 1.0;
      nb += 1;
  }

  void finished()
  {
      if (nb == 0) {
          return; // Avoid division by zero
      }

      for (int i = 0; i < 8; ++i) {
          for (int j = 0; j < 8; ++j) {
              for (int k = 0; k < 8; ++k) {
                  data[i][j][k] /= static_cast<float>(nb);
              }
          }
      }
  }

  // Retourne la distance entre cet histogramme et l'histogramme other
  float distance(const ColorDistribution& other) const
  {
      float distance = 0.0;

      for (int i = 0; i < 8; ++i) {
          for (int j = 0; j < 8; ++j) {
              for (int k = 0; k < 8; ++k) {
                  float numerator = data[i][j][k] - other.data[i][j][k];
                  float denominator = data[i][j][k] + other.data[i][j][k];

                  // Avoid division by zero
                  if (denominator != 0.0) {
                      distance += (numerator * numerator) / denominator;
                  }
              }
          }
      }

      return distance;
  }

};

ColorDistribution getColorDistribution( Mat input, Point pt1, Point pt2 )
{
  ColorDistribution cd;
  for ( int y = pt1.y; y < pt2.y; y++ )
    for ( int x = pt1.x; x < pt2.x; x++ )
      cd.add( input.at<Vec3b>( y, x ) );
  cd.finished();
  return cd;
}

float minDistance(const ColorDistribution& h, const std::vector<ColorDistribution>& hists)
{
    if (hists.empty()) {
        // Handle the case when the vector is empty
        return std::numeric_limits<float>::infinity();
    }

    float minDist = std::numeric_limits<float>::infinity();

    for (const auto& hist : hists) {
        float dist = h.distance(hist);
        if (dist < minDist) {
            minDist = dist;
        }
    }

    return minDist;
}

Mat recoObject(Mat input, 
              std::vector<ColorDistribution>& col_hists,
              std::vector<ColorDistribution>& col_hists_object,
              const std::vector<Vec3b>& colors,
              int block_size
)
{
    Mat output = input.clone();

    for (int y = 0; y <= input.rows - block_size; y += block_size)
    {
        for (int x = 0; x <= input.cols - block_size; x += block_size)
        {
            Point pt1_block(x, y);
            Point pt2_block(x + block_size, y + block_size);

            // Calculate ColorDistribution on the block (x,y) -> (x+block_size, y+block_size)
            ColorDistribution cd_block = getColorDistribution(input, pt1_block, pt2_block);

            // Calculate distances
            float dist_background = minDistance(cd_block, col_hists);
            float dist_object = minDistance(cd_block, col_hists_object);

            // Determine the label based on the minimum distance
            string label = (dist_background < dist_object) ? "Background" : "Object";

            // Set color based on the label (apply a filter)

            Vec3b color = (label == "Background") ? colors[0] : colors[1];

            
            rectangle(output, pt1_block, pt2_block, Scalar(color[0], color[1], color[2]), -1);
            
        }
    }

    return output;
}



int main( int argc, char** argv )
{
  Mat img_input, img_seg, img_d_bgr, img_d_hsv, img_d_lab;
  VideoCapture* pCap = nullptr;
  const int width = 640;
  const int height= 480;
  const int size  = 50;
  // Ouvre la camera
  pCap = new VideoCapture( 0 );
  if( ! pCap->isOpened() ) {
    cout << "Couldn't open image / camera ";
    return 1;
  }
  // Force une camera 640x480 (pas trop grande).
  pCap->set( CAP_PROP_FRAME_WIDTH, 640 );
  pCap->set( CAP_PROP_FRAME_HEIGHT, 480 );
  (*pCap) >> img_input;
  if( img_input.empty() ) return 1; // probleme avec la camera
  Point pt1( width/2-size/2, height/2-size/2 );
  Point pt2( width/2+size/2, height/2+size/2 );
  namedWindow( "input", 1 );
  imshow( "input", img_input );
  bool freeze = false;
  std::vector<ColorDistribution> col_hists;
  std::vector<ColorDistribution> col_hists_object;
  bool recognitionMode = false;

  while ( true )
    {
      char c = (char)waitKey(50); // attend 50ms -> 20 images/s
      if ( pCap != nullptr && ! freeze )
        (*pCap) >> img_input;     // récupère l'image de la caméra
      if ( c == 27 || c == 'q' )  // permet de quitter l'application
        break;
      if ( c == 'f' ) // permet de geler l'image
        freeze = ! freeze;
      if (c == 'v')
      {
          // Calculate color distribution for the left and right parts of the screen
          Point pt1_left(0, 0);
          Point pt2_left(width / 2, height);
          ColorDistribution cd_left = getColorDistribution(img_input, pt1_left, pt2_left);

          Point pt1_right(width / 2, 0);
          Point pt2_right(width, height);
          ColorDistribution cd_right = getColorDistribution(img_input, pt1_right, pt2_right);

          // Calculate and display the distance between the two distributions
          float distance = cd_left.distance(cd_right);
          cout << "Distance between left and right color distributions: " << distance << endl;
      }
      if (c == 'b')
      {
        const int bbloc = 128;
        col_hists.clear(); // Clear previous background color distributions

        for (int y = 0; y <= height - bbloc; y += bbloc)
        {
            for (int x = 0; x <= width - bbloc; x += bbloc)
            {
                Point pt1(x, y);
                Point pt2(x + bbloc, y + bbloc);

                // Calculate ColorDistribution on the block (x,y) -> (x+bbloc, y+bbloc)
                ColorDistribution cd_block = getColorDistribution(img_input, pt1, pt2);

                // Memorize the color distribution in col_hists
                col_hists.push_back(cd_block);
            }
        }

        int nb_hists_background = col_hists.size();
        cout << "Number of background color distributions: " << nb_hists_background << endl;
      }
      if (c == 'a')
      {
          // Calculate color distribution for the region inside the white rectangle
          ColorDistribution cd_object = getColorDistribution(img_input, pt1, pt2);

          // Add the color distribution to col_hists_object
          col_hists_object.push_back(cd_object);

          int nb_hists_object = col_hists_object.size();
          cout << "Number of object color distributions: " << nb_hists_object << endl;
      }
      if (c == 'r')
      {
          if (!col_hists.empty() && !col_hists_object.empty()) {
              recognitionMode = true;
              cout << "Switched to recognition mode" << endl;
          } else {
              cout << "Cannot switch to recognition mode, both histograms vectors must not be empty" << endl;
          }
      }

      if (recognitionMode)
      {
          // Recognition mode logic
          const int block_size = 8; // You can adjust this value (8x8 or 16x16)
          for (int y = 0; y <= height - block_size; y += block_size)
          {
              for (int x = 0; x <= width - block_size; x += block_size)
              {
                  Point pt1_block(x, y);
                  Point pt2_block(x + block_size, y + block_size);

                  // Calculate ColorDistribution on the block (x,y) -> (x+block_size, y+block_size)
                  ColorDistribution cd_block = getColorDistribution(img_input, pt1_block, pt2_block);

                  // Calculate distances
                  float dist_background = minDistance(cd_block, col_hists);
                  float dist_object = minDistance(cd_block, col_hists_object);

                  // Determine the label based on the minimum distance
                  string label = (dist_background < dist_object) ? "Background" : "Object";

                  // Draw label on the image
                  putText(img_input, label, Point(x, y), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(255, 255, 255), 1, LINE_AA);
              }
          }
      }


      Mat output = img_input;
      if ( recognitionMode ) 
      { // mode reconnaissance
        Mat gray;
        cvtColor(img_input, gray, COLOR_BGR2GRAY);
        Mat reco = recoObject( img_input, col_hists, col_hists_object, {Vec3b(0, 0, 0), Vec3b(0, 0, 255)}, 8 );
        cvtColor(gray, img_input, COLOR_GRAY2BGR);
        output = 0.5 * reco + 0.5 * img_input; //!FIX ME mélange reco + caméra
      }
      else
        cv::rectangle( img_input, pt1, pt2, Scalar( { 255.0, 255.0, 255.0 } ), 1 );
      imshow( "input", output );

    }
  return 0;
}