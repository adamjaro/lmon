
//_____________________________________________________________________________
//
// Example track finder for straight lines in 4 planes according Equation 9
// in Nuclear Instruments and Methods 203 (1982) 291-297
//
// Compiles as  g++ track_fit_NIM1982.cxx -o track_fit_NIM1982
// and runs by  ./track_fit_NIM1982
//
// Coordinate frame for detector planes is shown in the drawing below,
// shows correct in text editor with fixed-size font:
//
//                                    /\ x, y
//                                    |
//     plane 1            plane 2     |      plane 3             plane 4
//       :                  :         |         :                  :
//       :                  :         |         :                  :    __ detected track
//       :                  :         |         :                 (x)__/   (straight line)
//       :                  :         |         :              ___/:
//       :                  :         |         :         ___/     :
//       :                  :         |         :     ___/         :
//       :                  :         |        (x)___/  theta_x,y  :
// -------------------------------------------/-------------------------->
//       :                  :         |   ___/  :                  :      z
//       :                  :   ______|__/      :                  :
//       :                _(x)_/      | x0, y0  :                  :
//       :        _______/  :         |         :                  :
//    __(x)______/          :         |         :                  :
//  _/   :                  :         |         :                  :
//       :                  :         |         :                  :
//
//       <------- len -----><------- len ------><------ len ------->
//
//
//  Detector planes plane 1, 2, 3 and 4 are spaced equidistantly
//  with spacing len along the z axis. The planes are perpendicular
//  to the z axis and parallel to the x and y axes.
//
//  Origin of the coordinate frame is centered between planes 2 and 3.
//
//  Track points detected by individual planes are denoted as (x).
//
//  Reconstructed tracks are given in terms of track position x0 and y0
//  at z = 0 and by angles of the track relative to the z axis, theta_x
//  and theta_y.
//
//  Test data for the program are detected points (x) in simulation
//  of tagger 1 for one typical event.
//
//_____________________________________________________________________________

//C++
#include <iostream>
#include <vector>
#include <math.h>

//local functions
void MakeTrack(double len, double *x, double& pos, double& slope, double& theta);
double TrackChi2(double *zpos, double *x, double *y, double x0, double slope_x, double y0, double slope_y);

using namespace std;

//_____________________________________________________________________________
int main(int argc, char* argv[]) {

  //points on tagger 1 planes for one typical event, values are in mm

  //x and y of points on plane 1
  vector<double> plane_1_x{24.3396, 11.5396, 37.3396, 62.2396, 26.3396, 64.2396, 58.2396, 42.9396};
  vector<double> plane_1_y{-3.6500, 5.0500, 2.2500, 0.0500, 0.8500, 0.4500, 4.6500, -2.5500};

  //x and y of points on plane 2
  vector<double> plane_2_x{66.2396, 15.1396, 27.4396, 45.4396, 64.0396, 40.1396, 60.3396, 29.3396};
  vector<double> plane_2_y{0.4500, 4.9500, -3.5500, -2.5500, 0.0500, 2.2500, 4.5500, 0.8500};

  //x and y of points on plane 3
  vector<double> plane_3_x{18.8396, 32.3396, 62.4396, 68.1396, 65.9396, -73.4604, 42.9396, 30.4396, 47.9396};
  vector<double> plane_3_y{4.8500, 0.8500, 4.4500, 0.4500, 0.0500, -2.8500, 2.1500, -3.4500, -2.4500};

  //x and y of points on plane 4
  vector<double> plane_4_x{22.4396, 50.4396, 35.4396, 33.5396, 45.7396, 67.7396, -66.3604, 70.0396, 64.5396};
  vector<double> plane_4_y{4.7500, -2.3500, 0.7500, -3.3500, 2.0500, 0.0500, -2.7500, 0.4500, 4.2500};

  //maximal reduced chi^2 for tracks
  double max_chi2ndf = 0.01;

  //plane spacing along z (mm)
  double len = 300;

  //plane positions along z (mm)
  double zpos[] = {(-3./2)*len, (-1./2)*len, (1./2)*len, (3./2)*len};

  //loop over all points on all planes

  //plane 1
  for(size_t i1=0; i1<plane_1_x.size(); i1++) {

    //x and y of the given point on plane 1
    double p1_x = plane_1_x[i1];
    double p1_y = plane_1_y[i1];

    //plane 2
    for(size_t i2=0; i2<plane_2_x.size(); i2++) {

      //x and y of the given point on plane 2
      double p2_x = plane_2_x[i2];
      double p2_y = plane_2_y[i2];

      //plane 3
      for(size_t i3=0; i3<plane_3_x.size(); i3++) {

        //x and y of the given point on plane 3
        double p3_x = plane_3_x[i3];
        double p3_y = plane_3_y[i3];

        //plane 4
        for(size_t i4=0; i4<plane_4_x.size(); i4++) {

          //x and y of the given point on plane 4
          double p4_x = plane_4_x[i4];
          double p4_y = plane_4_y[i4];

          //array of all 4 track points in x and y
          double x[] = {p1_x, p2_x, p3_x, p4_x};
          double y[] = {p1_y, p2_y, p3_y, p4_y};

          //track candidate position, slope and angle
          double x0, y0, slope_x, slope_y, theta_x, theta_y;

          //calculate track candidate, pass by reference for candidate position, slope and angle
          MakeTrack(len, x, x0, slope_x, theta_x);
          MakeTrack(len, y, y0, slope_y, theta_y);

          //get chi^2 for the track candidate
          double chi2 = TrackChi2(zpos, x, y, x0, slope_x, y0, slope_y);

          //test the chi^2 for the track candidate, 4 degrees of freedom in the xy plane
          if( chi2 > max_chi2ndf*4 ) continue;

          //track candidate was accepted

          //print the found track parameters:
          cout << "Track, x0: " << x0 << ", y0: " << y0;
          cout << ", slope_x: " << slope_x << ", slope_y: " << slope_y;
          cout << ", theta_x: " << theta_x << ", theta_y: " << theta_y;
          cout << ", chi2: " << chi2 << endl;

        }//plane 4
      }//plane 2
    }//plane 2
  }//plane 1

  return 0;

}//main

//_____________________________________________________________________________
void MakeTrack(double len, double *x, double& pos, double& slope, double& theta) {

  //calculate track position, slope and angle from the points on the planes,
  //implements Eq. 9 in Nuclear Instruments and Methods 203 (1982) 291-297

  //track candidate position
  pos = (x[0]+x[1]+x[2]+x[3])/4.;

  //track candidate slope
  slope = (-3*x[0]-x[1]+x[2]+3*x[3])/(10*len);

  //track candidate angle
  theta = atan(slope);

}//MakeTrack

//_____________________________________________________________________________
double TrackChi2(double *zpos, double *x, double *y, double x0, double slope_x, double y0, double slope_y) {

  //calculate track candidate chi^2 for its points
  double chi2_xy = 0;

  //points loop
  for(int i=0; i<4; i++) {

    //track position on the plane in x and y
    double track_x_i = x0 + slope_x*zpos[i];
    double track_y_i = y0 + slope_y*zpos[i];

    //square distance between the track position and measured point along x and y
    double dx2 = (track_x_i-x[i])*(track_x_i-x[i]);
    double dy2 = (track_y_i-y[i])*(track_y_i-y[i]);

    //add the square distance in the xy plane to the chi^2
    chi2_xy += dx2 + dy2;

  }//points loop

  return chi2_xy;

}//TrackChi2




















