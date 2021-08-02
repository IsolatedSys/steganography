import cv2


def load_image(name):
    image = cv2.imread(filename=name)
    cv2.imshow("Img", image)
    # cv2.waitKey(0)
    return image


def manipulate_pixels_rand(img):
    w, h, _ = img.shape
    print("Size of Image: ", w, h, ". Possible characters = ", w * h * 3 / 8, "Words with average length of 6: ",
          w * h * 3 / 8 / 6)

    for x in range(w):
        for y in range(h):
            (b, g, r) = img[x, y]
            img[x, y] = (255, 0, r)
    return img


def hide_bin_text_in_img(img, text):
    w, h, _ = img.shape
    print("Size of Image: ", w, h, ". Possible characters = ", w * h * 3 / 8, "Words with average length of 6: ",
          w * h * 3 / 8 / 6)
    end = len(text)
    i = 0
    break_loop = 0
    for x in range(w):
        for y in range(h):
            (b, g, r) = img[x, y]
            b_bin = list(format(b, 'b'))
            g_bin = list(format(g, 'b'))
            r_bin = list(format(r, 'b'))
            try:
                b_bin[len(b_bin) - 1] = text[i]
            except:
                break_loop = 1
            if break_loop != 1:
                try:
                    g_bin[len(g_bin) - 1] = text[i + 1]
                except:
                    break_loop = 1
            if break_loop != 1:
                try:
                    r_bin[len(r_bin) - 1] = text[i + 2]
                except:
                    break_loop = 1

            b = bin_to_dec(b_bin)
            g = bin_to_dec(g_bin)
            r = bin_to_dec(r_bin)
            img[x, y] = (b, g, r)
            i = i + 3

        if break_loop == 1:
            break
    return img


def text_to_bits(text):
    bin_text = ''.join(format(ord(i), '08b') for i in text)
    return bin_text


def bin_to_dec(bin_text_slice):
    decimal = 0
    for i in range(len(bin_text_slice)):
        if bin_text_slice[i] != '0':
            # 8-1 = 7 highest bit index - index -> when beginning
            # at the highest bit
            decimal = decimal + pow(2, len(bin_text_slice) - i - 1)
    return decimal


def bits_to_text(bin_text):
    str_data = ' '
    for i in range(0, len(bin_text), 8):
        temp_data = bin_text[i:i + 8]
        decimal_data = bin_to_dec(temp_data)
        str_data = str_data + chr(decimal_data)
    # print(str_data)
    return str_data


def extract_text_from_image(img, len):
    w, h, _ = img.shape
    i = 0
    break_loop = 0
    len = len * 8
    text_bin = ''
    for x in range(w):
        for y in range(h):
            (b, g, r) = img[x, y]
            b_bin = test_channel_and_fix_length_to_list(b)
            g_bin = test_channel_and_fix_length_to_list(g)
            r_bin = test_channel_and_fix_length_to_list(r)

            if i >= len:
                break_loop = 1
                break
            text_bin = text_bin + b_bin[7]
            i = i + 1
            if i >= len:
                break_loop = 1
                break
            text_bin = text_bin + g_bin[7]
            i = i + 1
            if i >= len:
                break_loop = 1
                break
            text_bin = text_bin + r_bin[7]
            i = i + 1
            if i >= len:
                break_loop = 1
                break
        if break_loop:
            break
    print(text_bin)
    return bits_to_text(text_bin)


def load_text(path):
    with open(path) as f:
        text = f.read()
    f.close()
    return text


path = "/home/haraldk/Desktop/doge.jpg"
img = load_image(path)


def test_channel_and_fix_length_to_list(c):
    c_bin = list(format(c, 'b'))

    if len(c_bin) < 8:
        append = '0' * (8 - len(c_bin))
        c_bin = list(append + ''.join(c_bin))

    return c_bin

text = load_text('/home/haraldk/Desktop/lorem_ipsum.txt')
print(len(text))
bin_text = text_to_bits(text)
bits_to_text(bin_text)
img = hide_bin_text_in_img(img, bin_text)
cv2.imshow("New", img)
cv2.waitKey(0)
print(extract_text_from_image(img, len(text)))


