import cv2
import numpy as np

LEFT_DIRECTION  = 0
RIGHT_DIRECTION = 1
def getCornerPoints(imgPath, fov_ratio, direction):
    img     = cv2.imread(imgPath)
#rect[0] <---> rect left
#rect[1] <---> rect top
#rect[2] <---> rect right
#rect[3] <---> rect bottom
    rect    = np.zeros(4, dtype=np.int32)
    width   = np.size(img, 1)
    height  = np.size(img, 0)

    if direction == LEFT_DIRECTION:
        rect[0] = width * (1 - fov_ratio)
        rect[1] = 1000
        rect[2] = width-1
        rect[3] = height-1 - 1000
    else:
        rect[0] = 0
        rect[1] = 700
        rect[2] = width * fov_ratio
        rect[3] = height-1 - 1000


    print('rect:', rect[0], rect[1], rect[2], rect[3])
    hsplit0, crop_img, hsplit2 = np.hsplit(img, [rect[0], rect[2]])
    vsplit0, crop_img, vsplit2 = np.vsplit(crop_img, [rect[1], rect[3]])


    res     = calcConerPointsByPixel(crop_img)

    print('res', res)
    size    = len(res)
    w,h     = crop_img.shape[0:2]
    print('size:', np.size(crop_img, 1), np.size(crop_img, 0))

    #draw and save the corner point
    for item in res:
        for x in range(-2, 3):
            for y in range(-2, 3):
                if (item[1] + x) < w and (item[1] + x) > 0 and (item[0] + y) < h and (item[0] + y) > 0:
                    crop_img[item[1]+x][item[0]+y] = [0, 0, 255]


    #img[res[:,1], res[:,0]] = [0, 0, 255]
    cv2.imwrite('crop_img' + '%d'%direction + '.jpg', crop_img)

    #translate the res with rect
    for index in range(size):
        res[index][0] = res[index][0] + rect[0]
        res[index][1] = res[index][1] + rect[1]
    return res


def calcConerPointsByPixel(img):
    gray                = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray                = cv2.medianBlur(gray, 3)
    gray                = np.uint8(gray)
    retval, gray_img    = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    gray_img            = np.float32(gray_img)

    # find Harris corners
    dst                 = cv2.cornerHarris(gray,10,3,0.2)
    dst                 = cv2.erode(dst,None)
    ret, dst            = cv2.threshold(dst,0.02*dst.max(),255,0)
    dst                 = np.uint8(dst)

    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    #new_stats = np.zeros((1, len(stats[0])), dtype=type(stats[0][0]))
    new_centroids = np.zeros((1, len(centroids[0])), dtype=type(centroids[0][0]))

    idx = 0
    # here we remove the corner that not avaiable
    for stat in stats:
        if stat[4] < 200 and stat[4] > 20:
            new_centroids   = np.append(new_centroids, [centroids[idx]], 0)
        idx = idx + 1

    # define the criteria to stop and refine the corners
    criteria    = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners     = cv2.cornerSubPix(gray,np.float32(new_centroids),(5,5),(-1,-1),criteria)
    res         = np.hstack((new_centroids,corners))
    res         = np.int0(res)
    size        = len(res)

    #print('res', res)
    #here remove the first res point
    point_res   = np.zeros((size-1, 2), dtype = type(res[0][0]))

    for index in range(1, size):
        point_res[index-1][0] = (res[index][0] + res[index][2]) / 2
        point_res[index-1][1] = (res[index][1] + res[index][3]) / 2

    #arg0 is width direction, arg1 is height dirction
    final_res   = np.zeros((4, 2), dtype = type(res[0][0]))
    #get left_top/right_top points
    argsort = np.argsort(point_res, axis = 0)
    tmp_res   = np.zeros((4, 2), dtype = type(res[0][0]))

    #here we get the vertical 4 min value(at the 1st index)
    tmp_res[0]  = point_res[argsort[0][1]]
    tmp_res[1]  = point_res[argsort[1][1]]
    tmp_res[2]  = point_res[argsort[2][1]]
    tmp_res[3]  = point_res[argsort[3][1]]
    print('tmp_res', tmp_res)
    argmin = np.argmin(tmp_res, axis = 0)
    argmax = np.argmax(tmp_res, axis = 0)

    #left_top
    final_res[0]    = tmp_res[argmin[0]]
    #right_top
    final_res[1]    = tmp_res[argmax[0]]

    #get left_bottom/right_bootm points
    argsort = np.argsort(-point_res, axis = 0)
    tmp_res   = np.zeros((4, 2), dtype = type(res[0][0]))
    tmp_res[0]  = point_res[argsort[0][1]]
    tmp_res[1]  = point_res[argsort[1][1]]
    tmp_res[2]  = point_res[argsort[2][1]]
    tmp_res[3]  = point_res[argsort[3][1]]
    print('tmp_res1', tmp_res)
    argmin = np.argmin(tmp_res, axis = 0)
    argmax = np.argmax(tmp_res, axis = 0)
    #left_bottom
    final_res[2]    = tmp_res[argmin[0]]
    #right_bottom
    final_res[3]    = tmp_res[argmax[0]]

    #print(final_res)
    print("size", size)
    print("the corner size =", len(final_res))
    return final_res

def getCornerPointsTest():
    filename    = 'chart.jpg'
    img         = cv2.imread(filename)
    res         = calcConerPointsByPixel(img)
    w,h         = img.shape[0:2]

    img[res[:,1], res[:,0]] = [0, 0, 255]
    for item in res:
        for x in range(-2, 3):
            for y in range(-2, 3):
                if (item[1] + x) < w and (item[1] + x) > 0 and (item[0] + y) < h and (item[0] + y) > 0:
                    img[item[1]+x][item[0]+y] = [0, 0, 255]

    print(res)
    print(len(res))
    print('w', w, 'h', h)
    cv2.imwrite('corners.jpg',img)

    return res

if __name__ == '__main__':
    getCornerPointsTest()
