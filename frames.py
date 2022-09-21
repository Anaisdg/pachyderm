# Python
import argparse
import os, sys
import shutil
import subprocess
import json


# Opencv
import cv2


def main(videos):

    # if args.verbose:
    #     print( "Input arguments : ", args)

    cap = cv2.VideoCapture()
    cap.open(videos)
    if not cap.isOpened():
        parser.error("Failed to open input video")
        return 1

    frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frameId = 0
    skipDelta = 0
    exif_model=None

    while frameId < frameCount:
        ret, frame = cap.read()
        # print frameId, ret, frame.shape
        if not ret:
            print( "Failed to get the frame {f}".format(f=frameId))
            continue

        fname = "frame_" + str(frameId) + ".jpg"
        ofname = os.path.join("/pfs/out", fname)
        ret = cv2.imwrite(ofname, frame)
        if not ret:
            print( "Failed to write the frame {f}".format(f=frameId))
            continue

        frameId += int(1 + skipDelta)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameId)

    if exif_model:
        fields = ['Model', 'Make', 'FocalLength']
        if not write_exif_model(os.path.abspath("/pfs/out"), exif_model, fields):
            print( "Failed to write tags to the frames")
        # check on the first file
        fname = os.path.join(os.path.abspath("/pfs/out"), 'frame_0.jpg')
        cmd = ['exiftool', '-j', fname]
        for field in fields:
            cmd.append('-' + field)
        ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = ret.communicate()
        if args.verbose:
            print( "exiftool stdout : ", out)
        try:
            result = json.loads(out)[0]
            for field in fields:
                if field not in result:
                    parser.error("Exif model is not written to the output frames")
                    return 3
        except ValueError:
            parser.error("Output frame exif info can not be decoded")
            return 2

    return 0


def write_exif_model(folder_path, model, fields=None):
    cmd = ['exiftool', '-overwrite_original', '-r']
    for field in fields:
        if field in model:
            cmd.append('-' + field + "=" + model[field])
    cmd.append(folder_path)
    ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = ret.communicate()
    return ret.returncode == 0 and len(err) == 0


if __name__ == "__main__":

    print( "Start frames script ...")
    for dirpath, dirs, files in os.walk("/pfs/videos"):
        for file in files:
            main(os.path.join(dirpath, file))
            ret = main(os.path.join(dirpath, file))
            parser = argparse.ArgumentParser(description="Video2Frames converter")
            exit(ret)