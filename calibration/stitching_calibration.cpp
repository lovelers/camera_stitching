#include "stitching_calibration.hpp"
#include <opencv2/core/cvdef.h>
#include <iostream>
#include "opencv2/stitching/detail/matchers.hpp"
#include <opencv2/calib3d.hpp>
using namespace cv;
using namespace std;
using namespace cv::detail;
#define LOGLN(msg) std::cout << msg << std::endl

namespace stitching
{
    StitchingCalibration * StitchingCalibration::GetInstance()
    {
        static StitchingCalibration gSC;
        return &gSC;
    }

    StitchingCalibration::StitchingCalibration()
    {
        //TODO
    }

    void StitchingCalibration::Init(Size full, Size image, Size video)
    {
        mImageMap.full_size   = full;
        mImageMap.size        = image;

        mVideoMap.full_size   = full;
        mVideoMap.size        = video;

    }

    bool StitchingCalibration::ProcessCalibration(
            const Mat &image_left,
            const Mat &image_right,
            const Mat &video_left,
            const Mat &video_right,
            int degrees)
    {
        // check input arguments.
        bool argValid = true;
        if ((image_left.empty() ||image_right.empty()) ||
                (degrees < 0 || degrees > 360))
        {
            argValid = false;
            cout << "bad input arguments" << endl;
        }

        if (image_left.size() != image_right.size() ||
            video_left.size() != video_right.size())
        {
            argValid = false;
            cout << "image size are mismatch !" << endl;
        }

        if (false == argValid)
        {
            return false;
        }

        mImageMap.perspectiveTransformL = getHorizontalFlipMatrix(mImageMap.size, getRadian(degrees));
        mImageMap.perspectiveTransformR = getHorizontalFlipMatrix(mImageMap.size, getRadian(360 -degrees - 10));

#if 0
        // do image left optical center shift.
        Mat warpLeft;
        Size size = mImageMap.size;
        warpPerspective(image_left, warpLeft, mImageMap.perspectiveTransformL, size);

        vector<Point2f> src_corners(2);
        vector<Point2f> dst_corners(2);
        src_corners[0]  = Point2f(size.width-1, 0);
        src_corners[1]  = Point2f(size.width-1, size.height-1);

        perspectiveTransform(src_corners, dst_corners, mImageMap.perspectiveTransformL);

        Rect cropRect   = Rect(0, 0, static_cast<int>(dst_corners[0].x), size.height);
        Mat cropLeft;
        warpLeft(cropRect).copyTo(cropLeft);

        cout << "left:dst_corners: " << dst_corners[0] << dst_corners[1] << endl;
        cout << "left:cropRect: " << cropRect << endl;
        cout << "rect" << cropRect.x << " x " << cropRect.width << endl;

        Mat warpRight;
        warpPerspective(image_right, warpRight, mImageMap.perspectiveTransformR, size);
        src_corners[0]  = Point2f(0, 0);
        src_corners[1]  = Point2f(0, size.height-1);

        perspectiveTransform(src_corners, dst_corners, mImageMap.perspectiveTransformR);
        cout << "right:dst_corners: " << dst_corners[0] << dst_corners[1] << endl;

        cropRect        = Rect(static_cast<int>(dst_corners[0].x), 0, size.width - dst_corners[0].x, size.height);
        cout << "right:cropRect: " << cropRect << endl;
        Mat cropRight;
        warpRight(cropRect).copyTo(cropRight);


        float detla     = 0.3f;
        Size tmp        = cropLeft.size();
        Rect leftRect(tmp.width * (1-detla), 0, tmp.width * detla, tmp.height);
        Rect rightRect(0, 0, tmp.width * detla, tmp.height);
        std::vector<Rect> roiLeft(1), roiRight(1);
        roiLeft[0] = leftRect;
        roiRight[0] = rightRect;

#endif
        Ptr<FeaturesFinder> finder  = makePtr<AKAZEFeaturesFinder>();
        int64   t                   = getTickCount();

        vector<ImageFeatures> features(2);
        (*finder)(image_left, features[0]);
        (*finder)(image_right, features[1]);
        features[0].img_idx = 0;
        features[1].img_idx = 1;
        finder->collectGarbage();

        cout << "Finding features, time:" << ((getTickCount() - t) /getTickFrequency()) << "sec" << endl;
        t   = getTickCount();

        float match_conf                = 0.4f;
        Ptr<FeaturesMatcher> matcher    = makePtr<BestOf2NearestMatcher>(false, match_conf);
        vector<MatchesInfo> pairwise_matches;
        Mat matchMask(2, 2, CV_8U, Scalar(0));
        matchMask.at<uchar>(0, 1)             = 1;
        cout << "mat: " << matchMask << endl;

        (*matcher)(features, pairwise_matches, matchMask.getUMat(ACCESS_RW));
        matcher->collectGarbage();

        cout << "Pairwise matching, time:" << ((getTickCount() -t) /getTickFrequency()) << "sec" << endl;
        t   = getTickCount();

        float conf_thresh   = 1.f;
        vector<int> indices = leaveBiggestComponent(features, pairwise_matches, conf_thresh);

        for (int i = 0; i < pairwise_matches.size(); i++)
        {
            MatchesInfo* pMatch = &pairwise_matches[i];
            cout << pMatch->src_img_idx << "," << pMatch->dst_img_idx << "," << pMatch->confidence << endl;
            cout << "H" << endl << pMatch->H << endl;

#if 0
            // per testing, the ORB + Matcher output Matrix is not good enougth.
            if (pMatch->src_img_idx == 1 && pMatch->dst_img_idx == 0)
            {
                cout << "get the expected perspectiveTransform." << endl;
                cout << " H " << endl << pMatch->H << endl;
                cout << " confidence: " << pMatch->confidence << endl;
                cout << " inliers: " << pMatch->num_inliers << endl;
                Mat src_points(1, static_cast<int>(10), CV_32FC2);
                Mat dst_points(1, static_cast<int>(10), CV_32FC2);

                sort(pMatch->matches.begin(),pMatch->matches.end());
                int inlier_idx = 0;
                for (int j = 0; j <  pMatch->matches.size(); j++)
                {
                    const DMatch& m = pMatch->matches[j];
                    cout << "queryIdx : " << m.queryIdx;
                    cout << "trainIdx : " << m.trainIdx;
                    cout << "imgIdx: " << m.imgIdx;
                    cout << "distance: " << m.distance;
                    cout << endl;
                    if (pMatch->inliers_mask[j] && pMatch->matches[j].imgIdx == 0)
                    {

                        mImageMap.matchInfo.push_back(m);
#if 0
                        Point2f p = features[1].keypoints[m.queryIdx].pt;
                        p.x -= features[1].img_size.width * 0.5f;
                        p.y -= features[1].img_size.height * 0.5f;
                        src_points.at<Point2f>(0, inlier_idx) = p;

                        p = features[0].keypoints[m.trainIdx].pt;
                        p.x -= features[0].img_size.width * 0.5f;
                        p.y -= features[0].img_size.height * 0.5f;
                        dst_points.at<Point2f>(0, inlier_idx) = p;
#endif

                        inlier_idx++;

                        if (inlier_idx == 10)
                        {
                            break;
                        }
                    }
                }
                cout << "inlier_num :" << inlier_idx << endl;

                //pMatch->H = findHomography(src_points, dst_points);
                mImageMap.keypointsL    = features[0].keypoints;
                mImageMap.keypointsR    = features[1].keypoints;
                break;
            }
#endif

        }
        Ptr<Estimator> estimator = makePtr<HomographyBasedEstimator>();
        vector<CameraParams> cameras;
        (*estimator)(features, pairwise_matches, cameras);

        for (size_t i = 0; i < cameras.size(); ++i)
        {
            Mat R;
            cameras[i].R.convertTo(R, CV_32F);
            cameras[i].R = R;
        }


        Ptr<detail::BundleAdjusterBase> adjuster =
            makePtr<detail::BundleAdjusterRay>();

        cout << "end" <<endl;

        adjuster->setConfThresh(conf_thresh);
        Mat_<uchar> refine_mask = Mat::zeros(3, 3, CV_8U);
        refine_mask(0,0) = 1;
        refine_mask(0,1) = 1;
        refine_mask(0,2) = 1;
        refine_mask(1,1) = 1;
        refine_mask(1,2) = 1;
        adjuster->setRefinementMask(refine_mask);
        if (!(*adjuster)(features, pairwise_matches, cameras))
        {
            cout << "Camera parameters adjusting failed.\n";
            return -1;
        }


        vector<Mat> rmats;
        WaveCorrectKind wave_correct = detail::WAVE_CORRECT_HORIZ;
        for (size_t i = 0; i < cameras.size(); ++i)
            rmats.push_back(cameras[i].R.clone());
        waveCorrect(rmats, wave_correct);
        for (size_t i = 0; i < cameras.size(); ++i)
            cameras[i].R = rmats[i];

        mImageMap.cameras   = cameras;
        for(int i = 0; i < cameras.size(); i++)
        {
            cout << "camera: " << i << endl;
            cout << "focal : " << cameras[i].focal <<endl;
            cout << "R: " << "\n" << cameras[i].R <<endl;
            cout << "K: " << "\n" << cameras[i].K() << endl;
        }
    }

    double StitchingCalibration::getRadian(int degrees)
    {
        return degrees * CV_PI /180.0;
    }

    Matx33f StitchingCalibration::getHorizontalFlipMatrix(Size size, float rad)
    {

        double focal   = sqrt(size.width * size.width + size.height * size.height);
        cout << "rad" << rad << endl;
        // Projection 2D - > 3D matrix
        Matx43d A1(1, 0, -size.width / 2,
                0, 1, -size.height /2,
                0, 0, 1,
                0, 0, 1);

        Matx44d YFlip(cos(rad), 0, -sin(rad), 0,
                0, 1, 0, 0,
                sin(rad), 0, cos(rad), 0,
                0, 0, 0, 1);

        Matx34d A2(focal, 0, size.width/2, 0,
                0, focal, size.height/2, 0,
                0, 0, 1, 0);

        Matx44d T(1, 0, 0, 5,
                0, 1, 0, 0,
                0, 0, 1, focal,
                0, 0, 0, 1);
        Matx33f M = A2 * (T * (YFlip * A1));

        cout << "width: " << size.width << ", height:" << size.height << ", focal " << focal << endl;
        cout << "Matrix: " << endl << M << endl;
        return M;
    }

    calibration_map_t* StitchingCalibration::GetImageCalibrationMap()
    {
        return &mImageMap;
    }

    calibration_map_t* StitchingCalibration::GetVideoCalibrationMap()
    {
        return &mVideoMap;
    }
}

