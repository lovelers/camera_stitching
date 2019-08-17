#ifndef _STITCHING_CALIBRATION__H
#define _STITCHING_CALIBRATION__H
#include <opencv2/core.hpp>
#include "opencv2/stitching.hpp"

using namespace cv;
using namespace cv::detail;

namespace stitching
{

// here do the lef image /right image optical center calibration first.
typedef struct _calibration_map_t
{
    Size                        size;
    Size                        full_size;
    Matx33f                     perspectiveTransformL;
    Matx33f                     perspectiveTransformR;
    std::vector<DMatch>         matchInfo; 
    std::vector<KeyPoint>       keypointsL;
    std::vector<KeyPoint>       keypointsR;
    std::vector<CameraParams>   cameras;
} calibration_map_t;

class StitchingCalibration
{
public:
    static StitchingCalibration *           GetInstance();
    void                                    Init(Size full, Size image, Size video);
    bool                                    ProcessCalibration(
                                                const Mat &image_left,
                                                const Mat &image_right,
                                                const Mat &video_left = Mat(),
                                                const Mat &video_right = Mat(),
                                                int degrees = 35);
    calibration_map_t *                     GetImageCalibrationMap();
    calibration_map_t *                     GetVideoCalibrationMap();

    void                                    Destory();
private:
    StitchingCalibration();
    StitchingCalibration & operator = (const StitchingCalibration &);
    void    processVideoCaliFromImageData(
                const Mat& left,
                const Mat& right,
                int degrees);


    inline double   getRadian(int degrees);
    Matx33f         getHorizontalFlipMatrix(Size size, float rad);

    calibration_map_t   mVideoMap;
    calibration_map_t   mImageMap;
};
}
#endif//__STITCHING_CALIBRATION_
