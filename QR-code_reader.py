import sys
import time
import cv2


def printLog(str_log):  # лог в формате: время и информация
    print(time.strftime("%X\t", time.localtime()) + str_log)


if __name__ == "__main__":
    printLog('Starting "QR-code reader"')
    if len(sys.argv) != 2:
        printLog('---Err argv---')
        sys.exit(1)
    else:
        img_path = sys.argv[1]
        printLog(f'Selected file: "{img_path}".')

    printLog(f'Open file: "{img_path}".')
    img = cv2.imread(img_path)

    # detect QR-code
    printLog(f'Detect QR-code...')
    qcd = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(
        img)
    result = 'None'  # result operation
    if retval:
        for s, p in zip(decoded_info, points):
            if s:
                color = (0, 255, 0)
                result = f'OK. QR-code decoded_info string: "{s}"'
            else:
                color = (0, 0, 255)
                result = 'ERROR! QR code found but not decrypted.'
            img = cv2.polylines(
                img, [p.astype(int)], True, color, 30)
    else:
        result = 'ERROR! QR code not found.'

    printLog(result)  # print result
    resultf_len = 42  # len one line
    # split string into strings by length
    for i in range(resultf_len, len(result)+resultf_len, resultf_len):
        img = cv2.putText(img, result[i-resultf_len:i], (20, 30*(i//resultf_len)),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)  # print on img

    # get filename
    name = '.'.join(img_path.split("\\")[-1].split('.')[:-1])

    # write
    printLog(f'Write new file: "{name}_DQRC.png".')
    # img_out = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    cv2.imwrite('.\\' + name + '_DQRC.png', img)

    printLog('Exit')
