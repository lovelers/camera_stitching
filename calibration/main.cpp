#include "stitching_calibration.hpp"
#include <opencv2/core.hpp>
#include <iostream>
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/stitching.hpp"

// Linux
#include <libgen.h>

using namespace cv;
using namespace std;
using namespace cv::detail;
using namespace stitching;


const char* dname           = NULL;
const char* image_output    = "image_calibration.bin";
const char* video_output    = "video_calibration.bin";

int num_images  = 2;
vector<Mat> images(num_images);
vector<UMat> img_warped_s(num_images);
vector<UMat> img_warped_f(num_images);
int blend_width = 100;

//curently, the GraphCutSeamFinder use the three channels rgb for calculate.
//need consider whether should we optmize it or not
static cv::ImreadModes s_mode = cv::IMREAD_COLOR;

// blend type will increatese blending time.
// no < feather < multiband
int blend_type  = Blender::MULTI_BAND;

void printUsage();
int parseCmdArgs(int argc, char** argv);

int main(int argc, char* argv[])
{
    int retval = parseCmdArgs(argc, argv);
    if (retval) return -1;
    StitchingCalibration *calibration = StitchingCalibration::GetInstance();

    Size imgSize    = images[0].size();
    cout << "left size" << imgSize.width << "x" << imgSize.height << endl;
    imgSize         = images[1].size();
    cout << "right size" << imgSize.width << "x" << imgSize.height << endl;

    calibration->Init(imgSize, imgSize, imgSize);
    calibration->ProcessCalibration(images[0], images[1]);

    const calibration_map_t *imageMap = calibration->GetImageCalibrationMap();

#if 0
    Mat warpLeft;
    Mat warpRight;
    Size size       = imageMap->size;

    warpPerspective(images[0], warpLeft, imageMap->perspectiveTransformL, size);
    imwrite("./result_left.jpg", warpLeft);

    warpPerspective(images[1], warpRight, imageMap->perspectiveTransformR, size);
    imwrite("./result_right.jpg", warpRight);
    
    // Do basice transform testing.

    Mat cropLeft, cropRight;
    vector<Point2f> src_corners(2), dst_corners(2);
    Rect cropRect;

    src_corners[0]  = Point2f(size.width-1, 0);
    src_corners[1]  = Point2f(size.width-1, size.height-1);
    perspectiveTransform(src_corners, dst_corners, imageMap->perspectiveTransformL);

    cropRect        = Rect(0, 0, static_cast<int>(dst_corners[0].x),size.height);
    warpLeft(cropRect).copyTo(cropLeft);
    imwrite("./cropLeft.jpg", cropLeft);

    src_corners[0]  = Point2f(0, 0);
    src_corners[1]  = Point2f(0, size.height-1);
    perspectiveTransform(src_corners, dst_corners, imageMap->perspectiveTransformR);

    cropRect        = Rect(static_cast<int>(dst_corners[0].x), 0, size.width - dst_corners[0].x , size.height);
    warpRight(cropRect).copyTo(cropRight);
    imwrite("./cropRight.jpg", cropRight);

    Mat imageOutput;
    drawMatches(cropLeft, imageMap->keypointsL, cropRight, imageMap->keypointsR, imageMap->matchInfo, imageOutput, Scalar::all(-1), Scalar::all(-1), vector<char>(), DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS);
    imwrite("./matches.jpg", imageOutput);
    Size warpSize   = cropLeft.size();
    warpSize.width  = warpSize.width * 2;

    Mat warpResult;
    Mat_<float> K;
    imageMap->matchInfo.H.convertTo(K, CV_32F);
    warpPerspective(cropRight, warpResult, K, warpSize);
    Rect rect   = Rect(0, 0, cropLeft.cols, cropLeft.rows);
    cout << warpSize << endl;
    cout << rect << endl;
    Mat warpResult1 = warpResult(rect);
    cropLeft.copyTo(warpResult1);
    imwrite("./result.jpg", warpResult);
#endif

    vector<Point> corners(num_images);
    vector<UMat> masks_warped(num_images);
    vector<UMat> images_warped(num_images);
    vector<Size> sizes(num_images);
    vector<UMat> masks(num_images);

    // Preapre images masks
    for (int i = 0; i < num_images; ++i)
    {
        masks[i].create(images[i].size(), CV_8U);
        masks[i].setTo(Scalar::all(255));
        cout << "create mask:" << masks[i].size() << endl;
    }

    Ptr<WarperCreator> warper_creator   = makePtr<cv::PlaneWarper>();
    vector<CameraParams> cameras       = imageMap->cameras;
    if (cameras.size() !=  2)
    {
        cout << "bad calibration data" <<endl;
        return 0;
    }

    float warped_image_scale            = (cameras[0].focal + cameras[1].focal)  * 0.5f;
    float seam_work_aspect              = 1.f;

    // it's tuneable, when it small, the warp size will be small;
    float warpper_scale_ratio           = 0.6f;
    Ptr<RotationWarper> warper = warper_creator->create(static_cast<float>(warped_image_scale * seam_work_aspect * warpper_scale_ratio));


    for (int i = 0; i < num_images; ++i)
    {
        Mat_<float> K;
        cameras[i].K().convertTo(K, CV_32F);
        K(0,0) *= seam_work_aspect;
        K(0,2) *= seam_work_aspect;
        K(1,1) *= seam_work_aspect;
        K(1,2) *= seam_work_aspect;
        corners[i] = warper->warp(images[i], K, cameras[i].R, INTER_LINEAR, BORDER_REFLECT, images_warped[i]);
        sizes[i] = images_warped[i].size();
        cout << "corners: " << corners[i] << endl;
        cout << "size: " << sizes[i] << endl;

        warper->warp(masks[i], K, cameras[i].R, INTER_NEAREST, BORDER_CONSTANT, masks_warped[i]);
        if (i == 0)
        {
            imwrite("./calb_images.jpg", images[i]);
            imwrite("./calib_images_warped.jpg", images_warped[i]);
            imwrite("./calib_masks_warped.jpg", masks_warped[i]);
        }
        else
        {
            imwrite("./calib_images1.jpg", images[i]);
            imwrite("./calib_images_warped1.jpg", images_warped[i]);
            imwrite("./calib_masks_warped1.jpg", masks_warped[i]);
        }

        images_warped[i].convertTo(img_warped_f[i], CV_32F);
        images_warped[i].convertTo(img_warped_s[i], CV_16S);
    }


    // begin Compositing.
    cout << "start Compositing:" << endl;
    int64 t = getTickCount();
    // seam finder
    // seems can be optmize // first scalc the size .320x180.
    Size seam_finder_scale      = Size(320, 180);
    bool isSeamFinderScaled     = false;
    vector<UMat> seam_finder_image(num_images);
    vector<Point> seam_finder_corners(num_images);
    if (images_warped[0].size().area() < seam_finder_scale.area())
    {
        // should not goto here.
        images_warped[0].convertTo(seam_finder_image[0], CV_32F);
        images_warped[1].convertTo(seam_finder_image[1], CV_32F);
        //seam_finder_corners[i] = corners[i];
        isSeamFinderScaled = false;
    }
    else
    {
        Mat resize_image_warped;
        resize(images_warped[0], resize_image_warped, seam_finder_scale);
        cout << resize_image_warped.size() << endl;
        resize_image_warped.convertTo(seam_finder_image[0], CV_32F);

        resize(images_warped[1], resize_image_warped, seam_finder_scale);
        resize_image_warped.convertTo(seam_finder_image[1], CV_32F);


        float width_ratio = 
        isSeamFinderScaled = true;
    }

    Ptr<SeamFinder> seam_finder = makePtr<detail::GraphCutSeamFinder>(GraphCutSeamFinderBase::COST_COLOR);
    seam_finder->find(img_warped_f, corners, masks_warped);
    imwrite("./calc_seam_masks_warped1.jpg", masks_warped[0]);
    imwrite("./calc_seam_masks_warped2.jpg", masks_warped[1]);
    cout << "seam find time " << ((getTickCount() - t) / getTickFrequency()) << " sec" << endl;
    t   = getTickCount();

    // blender
    Ptr<Blender> blender = Blender::createDefault(blend_type, true);

    if ( blend_type == Blender::MULTI_BAND)
    {
        MultiBandBlender * mb = dynamic_cast<MultiBandBlender*>(blender.get());
        // here can be tuned
        mb->setNumBands(static_cast<int>(ceil(log(blend_width) / log(2.)) - 1.0));
    }
    else if ( blend_type == Blender::FEATHER)
    {
        FeatherBlender * fb = dynamic_cast<FeatherBlender*>(blender.get());
        fb->setSharpness(1.f /blend_width);
    }
    else
    {
        //TODO
    }
    blender->prepare(corners, sizes);

    //cout << "blend sizes: " << sizes << endl;
    cout << "mask_warped_size:" << masks_warped[0].size() << endl;

    Mat mask_warped;
    if (isSeamFinderScaled == true)
    {
    }
    //resize(masks_warped[0], mask_warped, img_warped_s[0].size());
    blender->feed(img_warped_s[0], masks_warped[0], corners[0]);
    //resize(masks_warped[1], mask_warped, img_warped_s[1].size());
    blender->feed(img_warped_s[1], masks_warped[1], corners[1]);

    Mat result, result_mask;
    blender->blend(result, result_mask);

    cout << "Compositing time " << ((getTickCount() - t) / getTickFrequency()) << " sec" << endl;

    imwrite("calibration_result.jpg", result);
    imwrite("calibration_result_mask.jpg", result_mask);

    return 0;
}

void printUsage()
{
    cout <<
        "StitchingCalibration \n\n"
        "calibration --left left.jpg --right right.jpg \n\n";
}


int parseCmdArgs(int argc, char** argv)
{
    if (argc == 1)
    {
        printUsage();
        return -1;
    }
    dname = dirname(argv[0]);
    cout << "dirname: " << dname << endl;
    for (int i = 1; i < argc; ++i)
    {
        if (string(argv[i]) == "--help" || string(argv[i]) == "/?")
        {
            printUsage();
            return -1;
        }
        else if (string(argv[i]) == "--left")
        {
            images[0] = imread(argv[i+1], s_mode);
            if (images[0].empty())
            {
                cout << "Can't read image '" << argv[i+1] << "'\n";
                return -1;
            }
            i++;
        }
        else if (string(argv[i]) == "--right")
        {
            images[1] = imread(argv[i+1], s_mode);
            if (images[1].empty())
            {
                cout << "Can't read image '" << argv[i+1] << "'\n";
                return -1;
            }
            i++;
        }
        else
        {
            cout << "should not goto here" << endl;
        }
    }
    return 0;
}
