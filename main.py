import ctypes
import pygame
from platform import system
from math import log2

def getByteDistr(fname) -> list:
    """
    Get Byte Distribution is file

    Parametrs:
        - fname: str - path to file

    Return:
        - [[int, ...], float] - list, where list[0] contains counts of each bytes, and list[1] which contains information entropy
    """
    if system() == "Linux":
        f = ctypes.CDLL('./librefile.so').getfiledist
    elif system() == "Windows":
        f = ctypes.CDLL('./librefile.dll').getfiledist
    else:
        raise OSError("OS doesnt support")
    f.restype = ctypes.POINTER(ctypes.c_longlong * 256)
    f.argtypes = argtypes = [ctypes.POINTER(ctypes.c_char), ]
    a = f(fname.encode('utf-8')).contents
    b = [a[i] for i in range(256)]
    sum_b = sum(b)
    h = 0
    if sum_b > 0:
        for i in range(256): 
            if b[i] < 0: continue
            h += b[i]/sum_b * log2(sum_b/b[i])

    return b, h

def renderByteDistr(arr:list, scr:pygame.Surface):
    max_arr = max(arr)
    if max_arr == 0:
        pygame.draw.rect(scr, (40, 0, 0), (8, 8, 256, 256))
        return
    norm_arr = [i/max_arr*255 for i in arr]
    for i in range(16):
        for j in range(16):
            if 65 < j*16+i <= 122:
                pygame.draw.rect(scr, (norm_arr[j*16+i], norm_arr[j*16+i], 0), (i*16+8, j*16+8, 16, 16))
            else: 
                pygame.draw.rect(scr, (0, norm_arr[j*16+i], 0), (i*16+8, j*16+8, 16, 16))


scr = pygame.display.set_mode((272, 272))
running = True
clock = pygame.time.Clock()

print("drag-and-drop file to get image of distribution")
print("the rectangle became lighter if the number of those byte approached the maximum number of bytes")

while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.DROPFILE:
            distr = getByteDistr(ev.file)
            renderByteDistr(distr[0], scr)
            pygame.display.set_caption(f"File entropy h = {round(distr[1], 2)}")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
