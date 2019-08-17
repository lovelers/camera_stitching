import math
def calcFov() :
    cam_fov             = 70
    cam_fov_detla       = 5;

    module_fov          = 23.5
    module_fov_detla    = 3

    a   = (cam_fov + cam_fov_detla) / 180.0 *  math.pi
    b   = (module_fov + module_fov_detla) / 180.0 * math.pi

    fov = math.sin(a / 2 - b) / (2 * math.cos(a/2) * math.sin(a/2))

    print("fov: ", fov)
    return fov

if __name__ == '__main__':
    calcFov()


