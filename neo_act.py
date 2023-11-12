import board
import neopixel

num_pixels = 12  # 예시로 30개의 LED를 사용

def on():
    pixels = neopixel.NeoPixel(board.D18, num_pixels)

# 모든 픽셀을 흰색으로 설정
    for i in range(num_pixels):
        pixels[i] = (100, 100, 100)
    pixels.show()

def off():
    pixels = neopixel.NeoPixel(board.D18, num_pixels)

# 모든 픽셀을 흰색으로 설정
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)
    pixels.show()
