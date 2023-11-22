import board
import neopixel
import time

num_pixels = 12  # 예시로 30개의 LED를 사용
ORDER = neopixel.GRB  # LED의 색상 순서
pixels = neopixel.NeoPixel(board.D18 , num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER)
increasing = True
brightness = 0

def wheel(pos):
    # 색상 휠을 생성하여 무지개 색상을 반환합니다.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait, bright):
    # 레인보우 사이클 패턴을 실행합니다.
    pixels.brightness = bright
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)
def breathe(wait, bright):
    global brightness, increasing
    pixels.brightness = brightness
    
    pixels.fill((255, 255, 255))
    pixels.show()
    
    if increasing:
        brightness += 0.01
        if brightness >= bright:
            increasing = False
    else:
        brightness -= 0.01
        if brightness <= 0:
            increasing = True
    time.sleep(wait)
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

