#include <stdio.h>
#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "opencv2/objdetect/objdetect.hpp"

//#include <system>
//#include <math.h>
//#include <complex>

using namespace std;
using namespace cv;

int x_prev = 0; int y_prev = 0; int A_prev = 0; int delta_a = 0;


/** Global variables */
String face_cascade_name = "/home/lenovo/mallick_cascades-master/lbpcascades/mallick_lbpcascade_frontalface.xml";
String profile_face_cascade_name = "/home/lenovo/mallick_cascades-master/lbpcascades/mallick_lbpcascade_profileface.xml";

CascadeClassifier face_cascade;
CascadeClassifier profile_face_cascade;


bool scroll_mode=false;
int trenutni = 0;
int prethodni = 0;
int starty, startx, sredistey;
    
///Click function
void mouse_click(int Area)
{
    delta_a = A_prev - Area;
    A_prev = Area;
    cout<<delta_a<<"\n";
    if(delta_a < -500)
    {
        system("xdotool click 1");
    }
}

///New mousmove function
void movemouse(Point &Centroid)
{

}

///Function that accepts the coordinates of the centroid and
///moves the mouse to a corresponding position
void mousemove(int x_pos, int y_pos)
{
    ///Strings that will contain the conversions
    string xcord; string ycord;

    ///These are buffers or something? I don't really know... lol.
    stringstream sstr; stringstream sstr2;

    ///Conversion to regular string happens here
    sstr<<4*x_pos;
    xcord = sstr.str();
    sstr2<<4*y_pos;
    ycord = sstr2.str();

    ///Getting the command string
    string command = "xdotool mousemove " + xcord + " " + ycord;

    ///Converting command string to a form that system() accepts.
    const char *com = command.c_str();
    system(com);
}

///This is the functions that gets the centroid of the thresholded image
void getCentroid(Mat &thresholded_image, Point &Centroid, int &Area)
{
    ///The object that holds all the centroids.
    ///Pass in the image. The boolean true tells the function that the image is binary
    Moments m = moments(thresholded_image, true);
    ///Moment along x axis
    double M10 = m.m10;
    ///Moment along y-axis;
    double M01 = m.m01;
    ///Area
    double M00 = m.m00;
    Centroid.x  = int(M10/M00);
    Centroid.y  = int(M01/M00);
    Area        = int(M00);
}

///HSV for ball: 81-105, 53-74,
void HSV_threshold(Mat &image, Mat &output_image_gray, int H_upper, int H_lower, int S_upper, int S_lower, int V_upper, int V_lower)
{
    Mat HSV;///Temporary Mat to store HSV


    ///Converting input image to HSV
    cvtColor(image, HSV, CV_RGB2HSV);
    //cvtColor(output_image_gray, output_image_gray, CV_RGB2GRAY);

    ///Processing each pixel and thresholding the image.
    int i, j;
        for(i=0; i<image.rows; i++)
        {
            for(j=0; j<image.cols; j++)
            {
                if((HSV.at<Vec3b>(i,j)[0] > H_lower)&&(HSV.at<Vec3b>(i,j)[0] < H_upper)&&(HSV.at<Vec3b>(i,j)[1]>S_lower)&&(HSV.at<Vec3b>(i,j)[1]<S_upper)&&(HSV.at<Vec3b>(i,j)[2]<V_upper)&&(HSV.at<Vec3b>(i,j)[2]>V_lower)) output_image_gray.at<uchar>(i,j) = 255;
                else output_image_gray.at<uchar>(i,j) = 0;
            }
        }
}


///funkcija koja provjerava dali je detektirana crvena boja
int red_color(Mat &camera_frame){
		
	int HL = 92;
    int HU = 255;
    int SL = 186;  
    int SU = 255;
    int VL = 118; 
    int VU = 255;
	
	Mat thresh_frame_red(Size(camera_frame.cols, camera_frame.rows), CV_8U);
	
	HSV_threshold(camera_frame, thresh_frame_red, HU, HL, SU, SL, VU, VL);
    medianBlur(thresh_frame_red, thresh_frame_red, 5); ///Low Pass filter to remove noise

	//provjera dali pronalazi crvene objekte
	imshow("red_Color", thresh_frame_red); //show the thresholded image

	Point Centroid; int Area;
	getCentroid(thresh_frame_red, Centroid, Area);
	
	if (Area>500) return 1;
	else return 0;
}

///funkcija koja provjerava dali je detektirana plava boja
int blue_color(Mat &camera_frame){
		
	int BHL = 0;
    int BHU = 35;
    int BSL = 91;  
    int BSU = 255;
    int BVL = 62; 
    int BVU = 255;
	
	Mat thresh_frame_blue(Size(camera_frame.cols, camera_frame.rows), CV_8U);
	
	HSV_threshold(camera_frame, thresh_frame_blue, BHU, BHL, BSU, BSL, BVU, BVL);
    medianBlur(thresh_frame_blue, thresh_frame_blue, 5); ///Low Pass filter to remove noise

	//provjera dali pronalazi crvene objekte
	imshow("Blue_Color", thresh_frame_blue); //show the thresholded image

	Point Centroid; int Area;
	getCentroid(thresh_frame_blue, Centroid, Area);
	
	if (Area>500) return 1;
	else return 0;
}

///funkcija koja provjerava datekciju profila
void detectAndDisplay( Mat &frame )
{
  std::vector<Rect> faces, right_profile, left_profile;
  Mat frame_gray, frame_gray_left;

  cvtColor( frame, frame_gray, CV_BGR2GRAY );
  equalizeHist( frame_gray, frame_gray );
  
  Mat frame_left;
  frame_left=frame;
  
  flip(frame_left, frame_left, 1);
  
  cvtColor( frame_left, frame_gray_left, CV_BGR2GRAY );
  equalizeHist( frame_gray_left, frame_gray_left );
  

  //-- Detect faces and profile
  face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(30, 30) );
  profile_face_cascade.detectMultiScale( frame_gray, right_profile, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(60, 60) );
  profile_face_cascade.detectMultiScale( frame_gray_left, left_profile, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(60, 60) );


 // flip(camera_frame, camera_frame, 1);

  for( size_t i = 0; i < faces.size(); i++ )
  {
    Point center( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );
    ellipse( frame, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 4, 8, 0 );
	
	trenutni+=1;
	
	if(trenutni==1){
		starty=center.y;
	}
	sredistey=center.y;
  }
  
  
  if(prethodni < trenutni){
	  prethodni=trenutni;
	  if((sredistey < starty) && (sredistey < starty-10)){
		//cout<<"scroll gore";
			
			  ///Getting the command string
			string command = "xdotool click --clearmodifiers 4" ;

			///Converting command string to a form that system() accepts.
			const char *com = command.c_str();
			system(com);
			
	  }
	  else if((sredistey> starty) && (sredistey > starty+10)){
		//cout<<"scroll dolje";
		  ///Getting the command string
			string command = "xdotool click --clearmodifiers 5" ;

			///Converting command string to a form that system() accepts.
			const char *com = command.c_str();
			system(com);
			
	  }
	}
	
	
  for( size_t i = 0; i < right_profile.size(); i++ )
  {
    Point center( right_profile[i].x + right_profile[i].width*0.5, right_profile[i].y + right_profile[i].height*0.5 );
    ellipse( frame, center, Size( right_profile[i].width*0.5, right_profile[i].height*0.5), 0, 0, 360, Scalar( 0, 0, 255 ), 4, 8, 0 );
	
	//Browsers["Item"](btChrome)["Run"]("http://smartbear.com");
//	system("firefox http://mysite.com");
	system("xdg-open http://google.com/");
//firefox -remote 'openurl(http://stackoverflow.com)';

  }
  
    for( size_t i = 0; i < left_profile.size(); i++ )
  {
    Point center( left_profile[i].x + left_profile[i].width*0.5, left_profile[i].y + left_profile[i].height*0.5 );
    ellipse( frame, center, Size( left_profile[i].width*0.5, left_profile[i].height*0.5), 0, 0, 360, Scalar( 0, 255, 255 ), 4, 8, 0 );
	
	//switch between tabs
  }

	
  //-- Show what you got
  imshow( "profile", frame );
 }

int main(int argc, char** argv)
{
	bool hand=false;
	
    
    ///variable declarations
    int camera_number    = 0;   
    int max_thresh       = 255; 
    
    int Hue_lower_thresh = 53;
    int Hue_upper_thresh = 97;
    int Sat_lower_thresh = 74;  
    int Sat_upper_thresh = 147;
    int Val_lower_thresh = 160; 
    int Val_upper_thresh = 255;
    Mat camera_frame; Mat displayed_frame; Mat gray_frame; //Mat thresh_frame;
    Mat darkfield = imread("~/Documents/OpenCV/eyetrack/darkfield.png");
    //vector<Mat> bgr_planes;

    ///creating the output window and trackbars
    namedWindow("camfeed");
    //namedWindow("RED"); namedWindow("BLUE"); namedWindow("GREEN");
    createTrackbar("Hue lower", "camfeed", &Hue_lower_thresh, max_thresh, NULL);
    createTrackbar("Hue upper", "camfeed", &Hue_upper_thresh, max_thresh, NULL);
    createTrackbar("Sat lower", "camfeed", &Sat_lower_thresh, max_thresh, NULL);
    createTrackbar("Sat upper", "camfeed", &Sat_upper_thresh, max_thresh, NULL);
    createTrackbar("Val lower", "camfeed", &Val_lower_thresh, max_thresh, NULL);
    createTrackbar("Val upper", "camfeed", &Val_upper_thresh, max_thresh, NULL);
  
    ///Camera setup
    VideoCapture camera;
    camera.open(camera_number);
    if(! camera.isOpened())
    {
        cerr<<"ERROR: COULD NOT ACCESS THE CAMERA!"<<endl;
        exit(1);
    }

    ///Setting the camera resolution.
    ///Lower resuolution for easier processing.
    camera.set(CV_CAP_PROP_FRAME_WIDTH, 396);
    camera.set(CV_CAP_PROP_FRAME_HEIGHT, 216);


	
    ///Infinite loop which gets each frame from webcam and processes
    ///it. Shows the processing output as a video.
    while(true)
    {
        ///Getting the next frame from the camera
        camera >> camera_frame;
        if(camera_frame.empty())
        {
            cerr<<"ERROR: COULD NOT GRAB A FRAME!"<<endl;
            exit(1);
        }
        flip(camera_frame, camera_frame, 1);
        
    
        if (scroll_mode==true){
			if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };
			if( !profile_face_cascade.load( profile_face_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };

			detectAndDisplay(camera_frame);
		}
        //provjeri dali je detektirana crvena boja
        if(red_color(camera_frame)==1){
			scroll_mode=true;
			
		//	cout<<"crvena boja\n";
			
			trenutni = 0;
			prethodni = 0;		
		}
		if(blue_color(camera_frame)==1){
			scroll_mode=false;
		//	cout<<"plava boja\n";
			//cout<<scroll_mode;
		}
		
		
		//detectAndDisplay(camera_frame);
        ///Declaring a thresholded image of same size as the camera frame but grayscale.
        Mat thresh_frame(Size(camera_frame.cols, camera_frame.rows), CV_8U);
        ///converting the image to grayscale
        ///Or any other colorspace conversions
     

        HSV_threshold(camera_frame, thresh_frame, Hue_upper_thresh, Hue_lower_thresh, Sat_upper_thresh, Sat_lower_thresh, Val_upper_thresh, Val_lower_thresh);
        medianBlur(thresh_frame, thresh_frame, 5); ///Low Pass filter to remove noise
        
        Point Centroid; int Area;
        getCentroid(thresh_frame, Centroid, Area);

        ///Sending final processed image to display
        imshow("camfeed", thresh_frame);
       // cout<<Area;
        ///I need a new mouse move function.
        if((Centroid.x<thresh_frame.cols)&&(Centroid.x>0)&&(Centroid.y>0)&&(Centroid.y<thresh_frame.rows))
        {
            if(Area > 300)
            {
                ///Comment out this function, then compile and run program for calibration
                ///For more details see README file.
                mousemove(Centroid.x, Centroid.y);
            }
        }
      //  mouse_click(Area);
        //imshow("BLUE", bgr_planes[0]);
        //imshow("GREEN", bgr_planes[1]);
        //imshow("RED", bgr_planes[2]);



    
        ///Listening for the user to press a key on the keyboard
        char keypress = waitKey(10);

  
        ///If user pressed escape key stop program.
        if(keypress == 27)
        {
            break;
        }

    }

    return 0;
}
