#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 20230423   修改去掉文件名用来排序的前面的3个字符

import sys
import os
import json
import struct
import shutil
import time
import random
# import xlrd
# import xlwt
import uuid
import re
# from xlutils.copy import copy
# from pydub import AudioSegment
# from pydub.silence import split_on_silence

BOOK_SUFFIX_NAME = ".wst"
BOOK_ENCODER_TYPE = 0x00  # 取值范围是0-15#

SOFT_VERSION = 0

BOOK_DEBUG_LOG = 0

# 取值为4的倍数
BOOK_TIME_LEN = 0x10
BOOK_CHECK_LEN_LEN = 0x4
BOOK_CHECK_VALUE_LEN = 0x4
BOOK_ENCODER_TYPE_LEN = 0x2
BOOK_ENCODER_TAG_LEN = 0x2
SOFT_VERSION_LEN = 0x4
BOOK_VERSION_LEN = 0x4
BOOK_UUID_LEN = 0x20
BOOK_NAME_LEN = 0x60
BOOK_RES_NO_LEN = 0x4

BOOK_MP3_NAME_LEN = 0x40
BOOK_DICT_LEN = 0x20
BOOK_DICT_TRANS_LEN = 0x60
BOOK_TEST_QUESTION_LEN = 0x100
BOOK_TEST_CHOICE_LEN = 0x80

BOOK_TIME_POS = 0
BOOK_CHECK_LEN_POS = BOOK_TIME_POS + BOOK_TIME_LEN
BOOK_CHECK_VALUE_POS = BOOK_CHECK_LEN_POS + BOOK_CHECK_LEN_LEN
BOOK_ENCODER_TYPE_POS = BOOK_CHECK_VALUE_POS + BOOK_CHECK_VALUE_LEN
BOOK_ENCODER_TAG_POS = BOOK_ENCODER_TYPE_POS + BOOK_ENCODER_TYPE_LEN
SOFT_VERSION_POS = BOOK_ENCODER_TAG_POS + BOOK_ENCODER_TAG_LEN
BOOK_VERSION_POS = SOFT_VERSION_POS + SOFT_VERSION_LEN
BOOK_UUID_POS = BOOK_VERSION_POS + BOOK_VERSION_LEN
BOOK_NAME_POS = BOOK_UUID_POS + BOOK_UUID_LEN
BOOK_MP3_NO_POS = BOOK_NAME_POS + BOOK_NAME_LEN

g_sep = os.path.sep

g_book_aie_tags = [
    0xf4a19dec, 0xff4c1c1c, 0x14a19dec, 0xff4c1c1a, 0x9ebd1d1b, 0xf8991c15, 0xf802173d, 0xf8d92c1a,
    0x6c390574, 0x67d48484, 0x8c390574, 0x67d48482, 0x06258583, 0x6001848d, 0x609a8fa5, 0x6041b482,
    0x9bee5e4e, 0x9fde7e7b, 0x9fde6e7a, 0x9fde9e71, 0x9edf8f7d, 0x9edf6fff, 0x9afb6e73, 0x9dff6f73,
    0x61208084, 0x6b7f7b5c, 0x63208080, 0x6320b080, 0x6654a181, 0x66559181, 0x60d38180, 0x8b81819a,
    0x6122828a, 0x62059282, 0x67d39283, 0x61d382a2, 0x99838380, 0x61c38382, 0x6193837c, 0x997c7c7b,
    0xcc99a5d4, 0xc7742424, 0x2c99a5d4, 0xc7742422, 0xa6852523, 0xc0a1242d, 0xc03a2f05, 0xc0e11422,
    0x94c1fd8c, 0x9f2c7c7c, 0x74c1fd8c, 0x9f2c7c7a, 0xfedd7d7b, 0x98f97c75, 0x9862775d, 0x98b94c7a,
    0xe1a2020a, 0xe2851202, 0xe7531203, 0xe1530222, 0x19030300, 0xe1430302, 0xe11303fc, 0x19fcfcfb,
    0xe1a00004, 0xebfffbdc, 0xe3a00000, 0xe3a03000, 0xe6d42101, 0xe6d51101, 0xe0530100, 0x0b01011a,
    0xecb985f4, 0xe7540404, 0x0cb985f4, 0xe7540402, 0x86a50503, 0xe081040d, 0xe01a0f25, 0xe0c13402,
    0xeb9e2e3e, 0xefae0e0b, 0xefae1e0a, 0xefaeee01, 0xeeafff0d, 0xeeaf1f8f, 0xea8b1e03, 0xed8f1f03,
    0x1150f0f4, 0x1b0f0b2c, 0x1350f0f0, 0x1350c0f0, 0x1624d1f1, 0x1625e1f1, 0x10a3f1f0, 0xfbf1f1ea,
    0xd192323a, 0xd2b52232, 0xd7632233, 0xd1633212, 0x29333330, 0xd1733332, 0xd12333cc, 0x29cccccb,
    0xdc89b5c4, 0xd7643434, 0x3c89b5c4, 0xd7643432, 0xb6953533, 0xd0b1343d, 0xd02a3f15, 0xd0f10432,
    0xe3962636, 0xe7a60603, 0xe7a61602, 0xe7a6e609, 0xe6a7f705, 0xe6a71787, 0xe283160b, 0xe587170b,
    0xe9a8080c, 0xe3f7f3d4, 0xeba80808, 0xeba83808, 0xeedc2909, 0xeedd1909, 0xe85b0908, 0x03090912,
    0xe9aa0a02, 0xea8d1a0a, 0xef5b1a0b, 0xe95b0a2a, 0x110b0b08, 0xe94b0b0a, 0xe91b0bf4, 0x11f4f4f3,
    0xe4b18dfc, 0xef5c0c0c, 0x04b18dfc, 0xef5c0c0a, 0x8ead0d0b, 0xe8890c05, 0xe812072d, 0xe8c93c0a,
    0xa1e2424a, 0xa2c55242, 0xa7135243, 0xa1134262, 0x59434340, 0xa1034342, 0xa15343bc, 0x59bcbcbb,
    0xacf9c5b4, 0xa7144444, 0x4cf9c5b4, 0xa7144442, 0xc6e54543, 0xa0c1444d, 0xa05a4f65, 0xa0817442,
    0xfb8e3e2e, 0xffbe1e1b, 0xffbe0e1a, 0xffbefe11, 0xfebfef1d, 0xfebf0f9f, 0xfa9b0e13, 0xfd9f0f13,
    0xc1802024, 0xcbdfdbfc, 0xc3802020, 0xc3801020, 0xc6f40121, 0xc6f53121, 0xc0732120, 0x2b21213a,
    0xc3b60616, 0xc7862623, 0xc7863622, 0xc786c629, 0xc687d725, 0xc68737a7, 0xc2a3362b, 0xc5a7372b,
    0x94c1fd8c, 0x9f2c7c7c, 0x74c1fd8c, 0x9f2c7c7a, 0xfedd7d7b, 0x98f97c75, 0x9862775d, 0x98b94c7a,
    0xe1a2020a, 0xe2851202, 0xe7531203, 0xe1530222, 0x19030300, 0xe1430302, 0xe11303fc, 0x19fcfcfb,
    0xe1a00004, 0xebfffbdc, 0xe3a00000, 0xe3a03000, 0xe6d42101, 0xe6d51101, 0xe0530100, 0x0b01011a,
    0xecb985f4, 0xe7540404, 0x0cb985f4, 0xe7540402, 0x86a50503, 0xe081040d, 0xe01a0f25, 0xe0c13402,
    0xeb9e2e3e, 0xefae0e0b, 0xefae1e0a, 0xefaeee01, 0xeeafff0d, 0xeeaf1f8f, 0xea8b1e03, 0xed8f1f03,
    0x04516d1c, 0x0fbcecec, 0xe4516d1c, 0x0fbcecea, 0x6e4dedeb, 0x0869ece5, 0x08f2e7cd, 0x0829dcea,
    0x3346f6e6, 0x3776d6d3, 0x3776c6d2, 0x377636d9, 0x367727d5, 0x3677c757, 0x3253c6db, 0x3557c7db,
    0x3978d8dc, 0x33272304, 0x3b78d8d8, 0x3b78e8d8, 0x3e0cf9d9, 0x3e0dc9d9, 0x388bd9d8, 0xd3d9d9c2,
    0x397adad2, 0x3a5dcada, 0x3f8bcadb, 0x398bdafa, 0xc1dbdbd8, 0x399bdbda, 0x39cbdb24, 0xc1242423,
    0xc3b60616, 0xc7862623, 0xc7863622, 0xc786c629, 0xc687d725, 0xc68737a7, 0xc2a3362b, 0xc5a7372b,
    0x1152f2fa, 0x1275e2f2, 0x17a3e2f3, 0x11a3f2d2, 0xe9f3f3f0, 0x11b3f3f2, 0x11e3f30c, 0xe90c0c0b,
    0x1c497504, 0x17a4f4f4, 0xfc497504, 0x17a4f4f2, 0x7655f5f3, 0x1071f4fd, 0x10eaffd5, 0x1031c4f2,
    0x14417d0c, 0x1facfcfc, 0xf4417d0c, 0x1facfcfa, 0x7e5dfdfb, 0x1879fcf5, 0x18e2f7dd, 0x1839ccfa,
    0x1b6edece, 0x1f5efefb, 0x1f5eeefa, 0x1f5e1ef1, 0x1e5f0ffd, 0x1e5fef7f, 0x1a7beef3, 0x1d7feff3,
    0xf9b8181c, 0xf3e7e3c4, 0xfbb81818, 0xfbb82818, 0xfecc3919, 0xfecd0919, 0xf84b1918, 0x13191902,
    0xc988282c, 0xc3d7d3f4, 0xcb882828, 0xcb881828, 0xcefc0929, 0xcefd3929, 0xc87b2928, 0x23292932,
    0xc98a2a22, 0xcaad3a2a, 0xcf7b3a2b, 0xc97b2a0a, 0x312b2b28, 0xc96b2b2a, 0xc93b2bd4, 0x31d4d4d3,
    0xc491addc, 0xcf7c2c2c, 0x2491addc, 0xcf7c2c2a, 0xae8d2d2b, 0xc8a92c25, 0xc832270d, 0xc8e91c2a,
    0xf1b01014, 0xfbefebcc, 0xf3b01010, 0xf3b02010, 0xf6c43111, 0xf6c50111, 0xf0431110, 0x1b11110a,
    0xf1b2121a, 0xf2950212, 0xf7430213, 0xf1431232, 0x09131310, 0xf1531312, 0xf10313ec, 0x09ececeb,
    0xfca995e4, 0xf7441414, 0x1ca995e4, 0xf7441412, 0x96b51513, 0xf091141d, 0xf00a1f35, 0xf0d12412,
    0xf3863626, 0xf7b61613, 0xf7b60612, 0xf7b6f619, 0xf6b7e715, 0xf6b70797, 0xf293061b, 0xf597071b,
    0xc182222a, 0xc2a53222, 0xc7733223, 0xc1732202, 0x39232320, 0xc1632322, 0xc13323dc, 0x39dcdcdb,
    0xa1e04044, 0xabbfbb9c, 0xa3e04040, 0xa3e07040, 0xa6946141, 0xa6955141, 0xa0134140, 0x4b41415a,
    0xa1e2424a, 0xa2c55242, 0xa7135243, 0xa1134262, 0x59434340, 0xa1034342, 0xa15343bc, 0x59bcbcbb,
    0xacf9c5b4, 0xa7144444, 0x4cf9c5b4, 0xa7144442, 0xc6e54543, 0xa0c1444d, 0xa05a4f65, 0xa0817442,
    0xcc99a5d4, 0xc7742424, 0x2c99a5d4, 0xc7742422, 0xa6852523, 0xc0a1242d, 0xc03a2f05, 0xc0e11422,
    0xc3b60616, 0xc7862623, 0xc7863622, 0xc786c629, 0xc687d725, 0xc68737a7, 0xc2a3362b, 0xc5a7372b,
    0xc988282c, 0xc3d7d3f4, 0xcb882828, 0xcb881828, 0xcefc0929, 0xcefd3929, 0xc87b2928, 0x23292932,
    0xc98a2a22, 0xcaad3a2a, 0xcf7b3a2b, 0xc97b2a0a, 0x312b2b28, 0xc96b2b2a, 0xc93b2bd4, 0x31d4d4d3,
    0xc491addc, 0xcf7c2c2c, 0x2491addc, 0xcf7c2c2a, 0xae8d2d2b, 0xc8a92c25, 0xc832270d, 0xc8e91c2a,
    0xcbbe0e1e, 0xcf8e2e2b, 0xcf8e3e2a, 0xcf8ece21, 0xce8fdf2d, 0xce8f3faf, 0xcaab3e23, 0xcdaf3f23,
    0xb9f8585c, 0xb3a7a384, 0xbbf85858, 0xbbf86858, 0xbe8c7959, 0xbe8d4959, 0xb80b5958, 0x53595942,
    0xb9fa5a52, 0xbadd4a5a, 0xbf0b4a5b, 0xb90b5a7a, 0x415b5b58, 0xb91b5b5a, 0xb94b5ba4, 0x41a4a4a3,
    0xb4e1ddac, 0xbf0c5c5c, 0x54e1ddac, 0xbf0c5c5a, 0xdefd5d5b, 0xb8d95c55, 0xb842577d, 0xb8996c5a,
    0xbbce7e6e, 0xbffe5e5b, 0xbffe4e5a, 0xbffebe51, 0xbeffaf5d, 0xbeff4fdf, 0xbadb4e53, 0xbddf4f53,
    0xd1903034, 0xdbcfcbec, 0xd3903030, 0xd3900030, 0xd6e41131, 0xd6e52131, 0xd0633130, 0x3b31312a,
    0xd3a61606, 0xd7963633, 0xd7962632, 0xd796d639, 0xd697c735, 0xd69727b7, 0xd2b3263b, 0xd5b7273b,
    0xd998383c, 0xd3c7c3e4, 0xdb983838, 0xdb980838, 0xdeec1939, 0xdeed2939, 0xd86b3938, 0x33393922,
    0xd99a3a32, 0xdabd2a3a, 0xdf6b2a3b, 0xd96b3a1a, 0x213b3b38, 0xd97b3b3a, 0xd92b3bc4, 0x21c4c4c3,
    0xd481bdcc, 0xdf6c3c3c, 0x3481bdcc, 0xdf6c3c3a, 0xbe9d3d3b, 0xd8b93c35, 0xd822371d, 0xd8f90c3a,
    0xdbae1e0e, 0xdf9e3e3b, 0xdf9e2e3a, 0xdf9ede31, 0xde9fcf3d, 0xde9f2fbf, 0xdabb2e33, 0xddbf2f33,
    0xa3d66676, 0xa7e64643, 0xa7e65642, 0xa7e6a649, 0xa6e7b745, 0xa6e757c7, 0xa2c3564b, 0xa5c7574b,
    0xa9e8484c, 0xa3b7b394, 0xabe84848, 0xabe87848, 0xae9c6949, 0xae9d5949, 0xa81b4948, 0x43494952,
    0xa9ea4a42, 0xaacd5a4a, 0xaf1b5a4b, 0xa91b4a6a, 0x514b4b48, 0xa90b4b4a, 0xa95b4bb4, 0x51b4b4b3,
    0xa4f1cdbc, 0xaf1c4c4c, 0x44f1cdbc, 0xaf1c4c4a, 0xceed4d4b, 0xa8c94c45, 0xa852476d, 0xa8897c4a,
    0xabde6e7e, 0xafee4e4b, 0xafee5e4a, 0xafeeae41, 0xaeefbf4d, 0xaeef5fcf, 0xaacb5e43, 0xadcf5f43,
    0xb1f05054, 0xbbafab8c, 0xb3f05050, 0xb3f06050, 0xb6847151, 0xb6854151, 0xb0035150, 0x5b51514a,
    0xb1f2525a, 0xb2d54252, 0xb7034253, 0xb1035272, 0x49535350, 0xb1135352, 0xb14353ac, 0x49acacab,
    0xbce9d5a4, 0xb7045454, 0x5ce9d5a4, 0xb7045452, 0xd6f55553, 0xb0d1545d, 0xb04a5f75, 0xb0916452,
    0xb3c67666, 0xb7f65653, 0xb7f64652, 0xb7f6b659, 0xb6f7a755, 0xb6f747d7, 0xb2d3465b, 0xb5d7475b,
    0xb9f8585c, 0xb3a7a384, 0xbbf85858, 0xbbf86858, 0xbe8c7959, 0xbe8d4959, 0xb80b5958, 0x53595942,
    0xb9fa5a52, 0xbadd4a5a, 0xbf0b4a5b, 0xb90b5a7a, 0x415b5b58, 0xb91b5b5a, 0xb94b5ba4, 0x41a4a4a3,
    0xb4e1ddac, 0xbf0c5c5c, 0x54e1ddac, 0xbf0c5c5a, 0xdefd5d5b, 0xb8d95c55, 0xb842577d, 0xb8996c5a,
    0xbbce7e6e, 0xbffe5e5b, 0xbffe4e5a, 0xbffebe51, 0xbeffaf5d, 0xbeff4fdf, 0xbadb4e53, 0xbddf4f53,
    0x81c06064, 0x8b9f9bbc, 0x83c06060, 0x83c05060, 0x86b44161, 0x86b57161, 0x80336160, 0x6b61617a,
    0x81c2626a, 0x82e57262, 0x87337263, 0x81336242, 0x79636360, 0x81236362, 0x8173639c, 0x799c9c9b,
    0x4100a0a4, 0x4b5f5b7c, 0x4300a0a0, 0x430090a0, 0x467481a1, 0x4675b1a1, 0x40f3a1a0, 0xaba1a1ba,
    0x1366d6c6, 0x1756f6f3, 0x1756e6f2, 0x175616f9, 0x165707f5, 0x1657e777, 0x1273e6fb, 0x1577e7fb,
    0x1958f8fc, 0x13070324, 0x1b58f8f8, 0x1b58c8f8, 0x1e2cd9f9, 0x1e2de9f9, 0x18abf9f8, 0xf3f9f9e2,
    0x195afaf2, 0x1a7deafa, 0x1fabeafb, 0x19abfada, 0xe1fbfbf8, 0x19bbfbfa, 0x19ebfb04, 0xe1040403,
    0x9cc9f584, 0x97247474, 0x7cc9f584, 0x97247472, 0xf6d57573, 0x90f1747d, 0x906a7f55, 0x90b14472,
    0x8cd9e594, 0x87346464, 0x6cd9e594, 0x87346462, 0xe6c56563, 0x80e1646d, 0x807a6f45, 0x80a15462,
    0x83f64656, 0x87c66663, 0x87c67662, 0x87c68669, 0x86c79765, 0x86c777e7, 0x82e3766b, 0x85e7776b,
    0x89c8686c, 0x839793b4, 0x8bc86868, 0x8bc85868, 0x8ebc4969, 0x8ebd7969, 0x883b6968, 0x63696972,
    0x89ca6a62, 0x8aed7a6a, 0x8f3b7a6b, 0x893b6a4a, 0x716b6b68, 0x892b6b6a, 0x897b6b94, 0x71949493,
    0x84d1ed9c, 0x8f3c6c6c, 0x64d1ed9c, 0x8f3c6c6a, 0xeecd6d6b, 0x88e96c65, 0x8872674d, 0x88a95c6a,
    0x8bfe4e5e, 0x8fce6e6b, 0x8fce7e6a, 0x8fce8e61, 0x8ecf9f6d, 0x8ecf7fef, 0x8aeb7e63, 0x8def7f63,
    0x91d07074, 0x9b8f8bac, 0x93d07070, 0x93d04070, 0x96a45171, 0x96a56171, 0x90237170, 0x7b71716a,
    0x91d2727a, 0x92f56272, 0x97236273, 0x91237252, 0x69737370, 0x91337372, 0x9163738c, 0x698c8c8b,
    0x74211d6c, 0x7fcc9c9c, 0x94211d6c, 0x7fcc9c9a, 0x1e3d9d9b, 0x78199c95, 0x788297bd, 0x7859ac9a,
    0x7b0ebeae, 0x7f3e9e9b, 0x7f3e8e9a, 0x7f3e7e91, 0x7e3f6f9d, 0x7e3f8f1f, 0x7a1b8e93, 0x7d1f8f93,
    0x4100a0a4, 0x4b5f5b7c, 0x4300a0a0, 0x430090a0, 0x467481a1, 0x4675b1a1, 0x40f3a1a0, 0xaba1a1ba,
    0x1366d6c6, 0x1756f6f3, 0x1756e6f2, 0x175616f9, 0x165707f5, 0x1657e777, 0x1273e6fb, 0x1577e7fb,
    0x1958f8fc, 0x13070324, 0x1b58f8f8, 0x1b58c8f8, 0x1e2cd9f9, 0x1e2de9f9, 0x18abf9f8, 0xf3f9f9e2,
    0x195afaf2, 0x1a7deafa, 0x1fabeafb, 0x19abfada, 0xe1fbfbf8, 0x19bbfbfa, 0x19ebfb04, 0xe1040403,
    0x1366d6c6, 0x1756f6f3, 0x1756e6f2, 0x175616f9, 0x165707f5, 0x1657e777, 0x1273e6fb, 0x1577e7fb,
    0x58798cba
]


def gen_uuid_value():
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    random_list = random.sample('ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrstuvwxyz0123456789', 10)
    random_str = "".join(random_list)
    result = mac + str(int(time.time())) + random_str
    return result


def sort_file_dir(data):
    regex = re.compile(r'(\d+|\s+)')
    list = regex.split(data)
    ret = ""
    index = 0;
    while index < len(list):
        if (list[index].isdigit()):
            ret = ret + list[index].zfill(6)
        else:
            ret = ret + list[index]
        index = index + 1
    return ret
    '''
    try:
        digital_list = re.findall('\d+', data)
        digital = int(digital_list[0])
        return digital
    except BaseException:
        return 1000000
    '''


def compute_real_tag(tag_param, tag):
    # return 0#debug

    # encoder type
    l_encoder_type = tag_param & 0x0f

    # encoder parameter
    tag_add = tag + tag_param
    if (tag_add > 65535):
        tag_add = tag_add - 65536
    tag_sub = 0
    if (tag < tag_param):
        tag_sub = 65536 + tag - tag_param
    else:
        tag_sub = tag - tag_param
    tag_yihuo = (tag ^ tag_param)

    if (0 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag * 65536 + tag_yihuo
        elif 2 == l_encoder_type:
            return tag_add * 65536 + tag_sub
        elif 3 == l_encoder_type:
            return tag_sub * 65536 + tag_add
    elif (1 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag * 65536 + tag_yihuo
        elif 2 == l_encoder_type:
            return tag_sub * 65536 + tag_add
        elif 3 == l_encoder_type:
            return tag_add * 65536 + tag_sub
    elif (2 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag_add * 65536 + tag_sub
        elif 2 == l_encoder_type:
            return tag_sub * 65536 + tag_add
        elif 3 == l_encoder_type:
            return tag * 65536 + tag_yihuo
    elif (3 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag_add * 65536 + tag_sub
        elif 2 == l_encoder_type:
            return tag * 65536 + tag_yihuo
        elif 3 == l_encoder_type:
            return tag_sub * 65536 + tag_add
    elif (4 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag_sub * 65536 + tag_add
        elif 2 == l_encoder_type:
            return tag * 65536 + tag_yihuo
        elif 3 == l_encoder_type:
            return tag_add * 65536 + tag_sub
    elif (5 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag_sub * 65536 + tag_add
        elif 2 == l_encoder_type:
            return tag_add * 65536 + tag_sub
        elif 3 == l_encoder_type:
            return tag * 65536 + tag_yihuo
    elif (6 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag * 65536 + tag_yihuo
        elif 2 == l_encoder_type:
            return tag * 65536 + tag_add
        elif 3 == l_encoder_type:
            return tag * 65536 + tag_sub
    elif (7 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag * 65536 + tag_yihuo
        elif 2 == l_encoder_type:
            return tag * 65536 + tag_sub
        elif 3 == l_encoder_type:
            return tag * 65536 + tag_add
    elif (8 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag_yihuo * 65536 + tag_yihuo
        elif 2 == l_encoder_type:
            return tag_yihuo * 65536 + tag_sub
        elif 3 == l_encoder_type:
            return tag_yihuo * 65536 + tag_add
    elif (9 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag_yihuo * 65536 + tag_yihuo
        elif 2 == l_encoder_type:
            return tag_yihuo * 65536 + tag_sub
        elif 3 == l_encoder_type:
            return tag_yihuo * 65536 + tag_add
    elif (10 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag_yihuo * 65536 + tag_sub
        elif 2 == l_encoder_type:
            return tag_yihuo * 65536 + tag_yihuo
        elif 3 == l_encoder_type:
            return tag_yihuo * 65536 + tag_add
    elif (11 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag_yihuo * 65536 + tag_sub
        elif 2 == l_encoder_type:
            return tag_yihuo * 65536 + tag_add
        elif 3 == l_encoder_type:
            return tag_yihuo * 65536 + tag_yihuo
    elif (12 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag_yihuo * 65536 + tag_add
        elif 2 == l_encoder_type:
            return tag_yihuo * 65536 + tag_sub
        elif 3 == l_encoder_type:
            return tag_yihuo * 65536 + tag_yihuo
    elif (13 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag_yihuo * 65536 + tag_add
        elif 2 == l_encoder_type:
            return tag_yihuo * 65536 + tag_yihuo
        elif 3 == l_encoder_type:
            return tag_yihuo * 65536 + tag_sub
    elif (14 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag * 65536 + tag_yihuo
        elif 2 == l_encoder_type:
            return tag * 65536 + tag_sub
        elif 3 == l_encoder_type:
            return tag * 65536 + tag_add
    elif (15 == BOOK_ENCODER_TYPE):
        if 1 == l_encoder_type:
            return tag * 65536 + tag_sub
        elif 2 == l_encoder_type:
            return tag * 65536 + tag_add
        elif 3 == l_encoder_type:
            return tag * 65536 + tag_yihuo


# write data and compute checksum also
def write_data_to_file(handle, data, write_total_len, encoder_tag):
    #check data info
    checksum = 0
    if 0 != write_total_len % 4:
        return checksum, -1
    data_utf8 = data.encode('utf-8')
    data_len = len(data_utf8)
    if data_len > write_total_len:
        return checksum, 2
    index = 0
    while index < write_total_len:
        value = int.from_bytes(bytes(data_utf8[index:index+4]), byteorder='little', signed=False)
        value = value ^ encoder_tag
        checksum += (value & 0xffff)
        checksum += ((value & 0xffff0000) >> 16)
        handle.write(value.to_bytes(length=4, byteorder='little', signed=False))
        index += 4
    return checksum, 0

def read_data_from_file(handle, read_total_len, encoder_tag):
    index = 0
    bytes_data = b""
    while index < read_total_len:
        data = struct.unpack('<I', handle.read(4))[0]
        data ^= encoder_tag
        bytes_data += data.to_bytes(4, byteorder='little', signed=False)
        index += 4
    return bytes_data.decode().strip(b'\x00'.decode())

def write_filedata_to_file(handle, filename, write_total_len, encoder_tag):
    tags_no = len(g_book_aie_tags)
    data_file = open(filename, "rb")
    writed_len = 0
    while writed_len < write_total_len:
        left_data_len = write_total_len - writed_len
        wrire_data = 0
        if (left_data_len >= 4):
            wrire_data = struct.unpack('<I', data_file.read(4))[0]
        elif (left_data_len == 1):
            wrire_data = struct.unpack('<B', data_file.read(1))[0]
        elif (left_data_len == 2):
            wrire_data = struct.unpack('<H', data_file.read(2))[0]
        elif (left_data_len == 3):
            wrire_data = struct.unpack('<H', data_file.read(2))[0] + struct.unpack('<B', data_file.read(1))[0] * 65536
        wrire_data ^= encoder_tag
        wrire_data ^= g_book_aie_tags[(writed_len >> 2) % tags_no]
        if (left_data_len >= 4):
            handle.write(wrire_data.to_bytes(length=4, byteorder='little', signed=False))
        else:
            last_data_index = 1
            if last_data_index <= left_data_len:
                handle.write((wrire_data & 0xff).to_bytes(length=1, byteorder='little', signed=False))
                last_data_index += 1
            if last_data_index <= left_data_len:
                handle.write(((wrire_data & 0xff00) >> 8).to_bytes(length=1, byteorder='little', signed=False))
                last_data_index += 1
            if last_data_index <= left_data_len:
                handle.write(((wrire_data & 0xff0000) >> 16).to_bytes(length=1, byteorder='little', signed=False))
                last_data_index += 1
        writed_len += 4
    data_file.close()


def wst_check(param):
    file_size = os.path.getsize(param)
    file_p = open(param, "rb")
    file_p.seek(BOOK_CHECK_LEN_POS, 0)
    check_total_len = struct.unpack('<I', file_p.read(4))[0]
    if (check_total_len > file_size):
        print("checksum len error :%x" % (check_total_len))
        return 1
    check_sum_value = struct.unpack('<I', file_p.read(4))[0]

    check_cur_len = 0
    compute_sum_value = 0
    while check_cur_len < check_total_len:
        check_cur_len += 2
        compute_sum_value += struct.unpack('<H', file_p.read(2))[0]
    file_p.close()

    if check_sum_value != (compute_sum_value & 0xffffffff):
        print("checksum error :%x:%x" % (compute_sum_value, check_sum_value))
        return 2
    return 0


def wst_get_uuid_from_file(param, check):
    uuid = ""
    try:
        file_p = open(param, "rb")
        file_p.seek(BOOK_UUID_POS, 0)
        old_uuid = file_p.read(BOOK_UUID_LEN)
        file_p.close()
        uuid = old_uuid.decode()
    except BaseException:
        print("[E]旧包%s读取UUID错误" % (param))
    return uuid


def wst_get_verno_from_file(param, check):
    old_version = -1
    try:
        if ((1 == check) and wst_check(param)):
            return old_version
        file_p = open(param, "rb")
        file_p.seek(BOOK_ENCODER_TYPE_POS, 0)
        encoder_type = struct.unpack('<H', file_p.read(2))[0]
        encoder_tag = struct.unpack('<H', file_p.read(2))[0]
        encoder_real = compute_real_tag(encoder_type, encoder_tag)
        file_p.seek(BOOK_VERSION_POS, 0)
        old_version = struct.unpack('<I', file_p.read(4))[0]
        file_p.close()
        old_version = old_version ^ encoder_real
        old_version = old_version & 0xffff
    except BaseException:
        print("[E]旧包%s读取版本错误" % (param))
    return old_version


def raz_analyse_words_json(dir, subdir, filename):
    error_no = 0
    word_list = []
    file = open(dir + g_sep + subdir + g_sep + filename, "rb")
    if (file):
        listJson = json.load(file)
        index = 0
        while (index < len(listJson)):

            word_res_filename = ""
            word_res_len = 0
            item = listJson[index]
            # 单词内容处理
            try:
                word_name = item["name"].strip()
                if (len(word_name.encode('utf-8')) > BOOK_DICT_LEN):
                    print("[数据警告]%s中word:%s 长度太长 0x%x" % (subdir, word_name, len(word_name.encode('utf-8'))))
                    index += 1
                    continue
            except BaseException:
                print("[数据错误]%s的%s第%d项没有name项" % (subdir, filename, index))
                error_no += 1
                index += 1
                continue
            # 音频处理
            try:
                audio_path = item["audio_path"].strip()
                if (len(audio_path) > 0):
                    audio_list = audio_path.split("/")
                    word_res_filename = dir + g_sep + subdir + g_sep + "quiz" + g_sep + audio_list[-1]
                    if os.path.isfile(word_res_filename):
                        word_res_len = os.path.getsize(word_res_filename)
                    else:
                        print("[数据警告]%s中%s音频不存在" % (subdir, word_name))
                        index += 1
                        continue
                else:
                    print("[数据警告]%s中%s没有音频" % (subdir, word_name))
                    index += 1
                    continue
            except BaseException:
                print("[数据错误]%s的%s第%d项没有audio_path项" % (subdir, filename, index))
                error_no += 1
                index += 1
                continue
            # 翻译处理
            try:
                translate_list = item["translate"]
                if (len(translate_list) > 0):
                    translate_info = translate_list[0]
                    translate_means = translate_info["means"][0]
                    first_translate_means_list = re.split(r'[,，;；：:：]', translate_means)
                    show_translate_mean = ""
                    if (first_translate_means_list[0] == ""):
                        show_translate_mean = translate_means
                    else:
                        show_translate_mean = first_translate_means_list[0]
                    '''
                    second_translate_means_list = re.split(r'[（）()]', show_translate_mean)
                    chinese_means = ""
                    means_index = 0
                    means_total = len(second_translate_means_list)
                    while (means_index < means_total):
                        if "名词复数" in second_translate_means_list[means_index] or \
                            "的复数" in second_translate_means_list[means_index]:
                            chinese_means = chinese_means + "(复数)"
                            break

                        if "人称单数" in second_translate_means_list[means_index] or \
                            "的过去式" in second_translate_means_list[means_index]:
                            break
                        if means_index > 0 and means_index + 2 == means_total:
                            break
                        chinese_means = chinese_means + second_translate_means_list[means_index]
                        means_index += 1
                    #print("%s+++++%s+++++%s+++++%d"%(show_translate_mean, second_translate_means_list, chinese_means, means_total))
                    trans_content = translate_info["part"] + chinese_means
                    '''
                    trans_content = translate_info["part"] + translate_means
                    # trans_content = translate_info["part"] + show_translate_mean
                    if (len(trans_content.encode('utf-8')) > BOOK_DICT_TRANS_LEN):
                        print("[数据警告]%s的%s的translate项太长0x%x" % (subdir, filename, len(trans_content.encode('utf-8'))))
                        index += 1
                        continue
                else:
                    print("[数据警告]%s中%s没有翻译" % (subdir, word_name))
                    index += 1
                    continue
            except BaseException:
                print("[数据错误]%s的%s第%d项没有translate项" % (subdir, filename, index))
                error_no += 1
                index += 1
                continue
            word_list.append([word_name, word_res_filename, word_res_len, trans_content])
            index += 1
    return word_list, error_no


def raz_analyse_test_json(dir, subdir, filename):
    error_no = 0
    question_list = []
    file = open(dir + g_sep + subdir + g_sep + filename, "rb")
    if (file):
        listJson = json.load(file)
        index = 0
        question_sub_no = 0
        question_sub_list = []
        while (index < len(listJson)):
            item = listJson[index]
            question_title = item["import_title"].strip()
            if (len(question_title.encode('utf-8')) > BOOK_TEST_QUESTION_LEN):
                print("[数据警告]丢弃问题%s问题:%s 问题长度太长 0x%x" % (subdir, question_title, len(question_title.encode('utf-8'))))
                index += 1
                continue
            question_res_filename = dir + g_sep + subdir + g_sep + "quiz" + g_sep + "q" + str(index) + ".mp3"
            question_res_len = 0
            if os.path.isfile(question_res_filename):
                question_res_len = os.path.getsize(question_res_filename)
            answer_right = -1
            answer_selects = item["tdata"]
            answer_index = 0
            answer_array = []
            if (len(answer_selects) > 4) or (len(answer_selects) <= 1):
                print("[数据警告]%s的%s问题支持2-4个选项,目前有%d选项,丢弃" % (subdir, question_title, len(answer_selects)))
                index += 1
                continue
            answer_effect = 1
            while (answer_index < len(answer_selects)):
                answer_title = answer_selects[answer_index]["title"].strip()
                if (len(answer_title.encode('utf-8')) > BOOK_TEST_CHOICE_LEN):
                    print("[数据警告]%s丢弃问题%s:答案长度太长 0x%x" % (subdir, question_title, len(answer_title.encode('utf-8'))))
                    answer_effect = 0
                    break
                answer_res_filename = dir + g_sep + subdir + g_sep + "quiz" + g_sep + "q" + str(index) + "_" + str(
                    answer_index) + ".mp3"
                answer_res_len = 0
                if os.path.isfile(answer_res_filename):
                    answer_res_len = os.path.getsize(answer_res_filename)
                answer_array.append([answer_title, answer_res_filename, answer_res_len])
                answer_select_result = answer_selects[answer_index]["is_answer"]
                if (answer_select_result):
                    answer_right = answer_index
                answer_index += 1
            if (0 == answer_effect):
                index += 1
                continue
            if (-1 == answer_right):
                index += 1
                print("[数据警告]丢弃问题%s,没有正确答案选项" % (answer_title))
                continue
            question_sub_list.append(
                [question_title, question_res_filename, question_res_len, answer_right, answer_array, 0])
            index += 1
            question_sub_no += 1
        question_list.append(["no url", 0, question_sub_no, question_sub_list])  # 内容资源为空
    return question_list, error_no


def raz_print_data(res_array):
    index = 0
    print("[")
    while index < len(res_array):
        print("  {")
        print("    res_show_name: %s," % (res_array[index][0]))
        print("    res_mp3_url  : %s," % (res_array[index][1]))
        print("    res_mp3_len  : %d," % (res_array[index][2]))
        print("    res_lrc_url  : %s," % (res_array[index][3]))
        print("    res_lrc_len  : %d," % (res_array[index][4]))
        # word info
        print("    word_no      : %d," % (res_array[index][5]))
        print("    word_info    : [")
        word_index = 0
        word_array = res_array[index][6]
        while (word_index < len(word_array)):
            print("      {")
            print("        index  : %d," % (word_index))
            print("        name   : %s," % (word_array[word_index][0]))
            print("        mp3_url: %s," % (word_array[word_index][1]))
            print("        mp3_len: %d" % (word_array[word_index][2]))
            print("        trans  : %s," % (word_array[word_index][3]))
            print("      }")
            word_index += 1
        print("    ],")
        # test info
        print("    test_main_no  : %d," % (res_array[index][7]))
        print("    test_info    : [")
        test_main_index = 0
        test_all_info = res_array[index][8]
        while (test_main_index < len(test_all_info)):
            print("    test_main%d:[" % (test_main_index))
            print("      content_url: %s" % (test_all_info[test_main_index][0]))
            print("      content_res_len: %s" % (test_all_info[test_main_index][1]))
            print("      deatil_question: [")
            test_index = 0
            test_array = test_all_info[test_main_index][3]
            while (test_index < len(test_array)):
                print("        {")
                print("          index        : %d," % (test_index))
                print("          question     : %s," % (test_array[test_index][0]))
                print("          mp3_url      : %s," % (test_array[test_index][1]))
                print("          mp3_len      : %d," % (test_array[test_index][2]))
                print("          right_answer : %d" % (test_array[test_index][3]))
                print("          answer_info  : [")
                answer_index = 0
                answer_array = test_array[test_index][4]
                while (answer_index < len(answer_array)):
                    print("            {")
                    print("              choice_index    : %d," % (answer_index))
                    print("              choice_content  : %s," % (answer_array[answer_index][0]))
                    print("              choice_mp3_url  : %s," % (answer_array[answer_index][1]))
                    print("              choice_mp3_len  : %s," % (answer_array[answer_index][2]))
                    print("            },")
                    answer_index += 1
                print("          ]")
                print("        },")
                test_index += 1
            print("      ]")
            test_main_index += 1
        print("    ]")
        print("  },")
        index += 1
    print("]")


class Chapter:
    def __init__(self, name, audio_dir):
        self.chapter_name = name
        self.audio_dir = audio_dir
        self.newWord = []
        self.newPhase = []
        self.newSentence = []
        self.recite = []
        print(f'========Chapter {name}==============')

    def get_chapter_name(self):
        return self.chapter_name

    def get_audio_dir(self):
        return self.audio_dir

    def insert_newWord(self, newWord):
        self.newWord.append(newWord)

    def get_newWord(self):
        return self.newWord

    def insert_newPhase(self, newPhase):
        self.newPhase.append(newPhase)

    def get_newPhase(self):
        return self.newPhase

    def insert_newSentence(self, newSentence):
        self.newSentence.append(newSentence)

    def get_newSentence(self):
        return self.newSentence

    def insert_recite(self, recite):
        self.recite.append(recite)

    def get_recite(self):
        return self.recite

    def dump_chapter_info(self):
        print('name:', self.chapter_name)
        print('newWord:', self.newWord)
        print('newPhase:', self.newPhase)
        print('newSentence:', self.newSentence)
        print('dictation:', self.dictation)
        print('recite:', self.recite)

def wst_decode(param):
    file_size = os.path.getsize(param)
    with open(param, 'rb') as file_p:
        file_p.seek(BOOK_CHECK_LEN_POS, 0)
        check_total_len = struct.unpack('<I', file_p.read(4))[0]
        if (check_total_len > file_size):
            print("checksum len error :%x" % (check_total_len))
            return 1
        check_sum_value = struct.unpack('<I', file_p.read(4))[0]

        check_cur_len = 0
        compute_sum_value = 0
        while check_cur_len < check_total_len:
            check_cur_len += 2
            compute_sum_value += struct.unpack('<H', file_p.read(2))[0]
        if check_sum_value != (compute_sum_value & 0xffffffff):
            print("checksum [%d] error %x:%x" % (check_total_len, compute_sum_value, check_sum_value))
            return 2

        file_p.seek(BOOK_ENCODER_TYPE_POS, 0)
        encoder_type = struct.unpack('<H', file_p.read(2))[0]
        encoder_tag = struct.unpack('<H', file_p.read(2))[0]
        real_encoder_tag = compute_real_tag(encoder_type, encoder_tag)
        print('real_encoder_tag: %x, %x -> %x' % (encoder_type, encoder_tag, real_encoder_tag))

        # 版本号
        # file_p.seek(BOOK_VERSION_POS, 0)
        soft_version = struct.unpack('<I', file_p.read(4))[0]
        soft_version ^= real_encoder_tag
        print("soft_version:%x" % (soft_version))

        # 版本号
        # file_p.seek(BOOK_VERSION_POS, 0)
        package_no = struct.unpack('<I', file_p.read(4))[0]
        package_no ^= real_encoder_tag
        print("package_version:%x" % (package_no))

        # file_p.seek(BOOK_UUID_POS, 0)
        uuid = read_data_from_file(file_p, BOOK_UUID_LEN, 0)
        print(f"uuid: {uuid}")

        package_name = read_data_from_file(file_p, BOOK_NAME_LEN, real_encoder_tag)
        print(f'package name: {package_name}')

        chapters_data = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
        chapters_cnt = chapters_data & 0xFFFF
        chapters_lan = (chapters_data & 0xF0000) >> 16
        if chapters_lan == 1:
            language = '中文书籍'
        elif chapters_lan == 2:
            language = '英文书籍'
        else:
            print(f'未知书籍 {chapters_lan}')
            return
        print(f'{language} 章节数：{chapters_cnt}')

        head_pos = file_p.tell()
        for i in range(chapters_cnt):
            print(f'开始读取第{i+1}章节数据')
            file_p.seek(head_pos, 0)
            cname_h_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
            cname_h_len = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
            w_h_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
            p_h_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
            s_h_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
            r_h_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
            head_pos = file_p.tell()
            # print(f'第{i+1}章节 字 head pos: {w_h_pos}')
            # print(f'第{i+1}章节 词 head pos: {p_h_pos}')
            # print(f'第{i+1}章节 跟读 head pos: {s_h_pos}')
            # print(f'第{i+1}章节 背诵 head pos: {r_h_pos}')
            file_p.seek(cname_h_pos, 0)
            chapter_name = read_data_from_file(file_p, cname_h_len, real_encoder_tag)
            print(f'开始读取第{i+1}章节 {chapter_name} 字 数据')
            file_p.seek(w_h_pos, 0)
            word_num = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
            print(f'开始读取第{i+1}章节有{word_num}个字')
            for j in range(word_num):
                print(f'开始读取第{i + 1}章节第{j+1}个字')
                file_p.seek(w_h_pos + 4 + j * 4, 0)
                w_j_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                file_p.seek(w_j_pos, 0)

                w_j_txt_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                w_j_txt_len = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag

                w_j_pinyin_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                w_j_pinyin_len = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag

                w_j_audio_cnt = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                file_p.seek(w_j_audio_cnt * 8, 1)
                print(f'开始读取第{i + 1}章节第{j + 1}个字 音频个数：{w_j_audio_cnt}')

                w_j_daudio_cnt = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                file_p.seek(w_j_daudio_cnt * 8, 1)
                print(f'开始读取第{i + 1}章节第{j + 1}个字 听写音频个数：{w_j_daudio_cnt}')

                w_j_zuci_cnt = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                w_j_zuci_pos_list = []
                w_j_zuci_len_list = []
                print(f'开始读取第{i + 1}章节第{j + 1}个字 组词个数：{w_j_zuci_cnt}')
                for k in range(w_j_zuci_cnt):
                    w_j_zuci_pos_list.append(struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag)
                    w_j_zuci_len_list.append(struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag)

                if w_j_txt_len:
                    file_p.seek(w_j_txt_pos, 0)
                    word_txt = read_data_from_file(file_p, w_j_txt_len, real_encoder_tag)
                    print(f'第{i + 1}章节第{j+1}个字是：{word_txt}')

                if w_j_pinyin_len:
                    file_p.seek(w_j_pinyin_pos, 0)
                    pinyin_txt = read_data_from_file(file_p, w_j_pinyin_len, real_encoder_tag)
                    print(f'第{i + 1}章节第{j+1}个字的拼音是：{pinyin_txt}')

                for k in range(w_j_zuci_cnt):
                    file_p.seek(w_j_zuci_pos_list[k], 0)
                    zuci_txt = read_data_from_file(file_p, w_j_zuci_len_list[k], real_encoder_tag)
                    print(f'第{i + 1}章节第{j + 1}个字第{k+1}个组词是：{zuci_txt}')

            file_p.seek(p_h_pos, 0)
            phase_num = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
            print(f'开始读取第{i+1}章节有{phase_num}个词')
            for j in range(phase_num):
                print(f'开始读取第{i + 1}章节第{j+1}个词')
                file_p.seek(p_h_pos + 4 + j * 4, 0)
                p_j_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                file_p.seek(p_j_pos, 0)

                p_j_txt_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                p_j_txt_len = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag

                p_j_pinyin_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                p_j_pinyin_len = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag

                p_j_audio_cnt = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                file_p.seek(p_j_audio_cnt * 8, 1)
                print(f'开始读取第{i + 1}章节第{j + 1}个词 音频个数：{p_j_audio_cnt}')

                p_j_daudio_cnt = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                file_p.seek(p_j_daudio_cnt * 8, 1)
                print(f'开始读取第{i + 1}章节第{j + 1}个词 听写音频个数：{p_j_daudio_cnt}')

                p_j_shiyi_cnt = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                p_j_shiyi_pos_list = []
                p_j_shiyi_len_list = []
                print(f'开始读取第{i + 1}章节第{j + 1}个词 释义个数：{p_j_shiyi_cnt}')
                for k in range(p_j_shiyi_cnt):
                    p_j_shiyi_pos_list.append(struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag)
                    p_j_shiyi_len_list.append(struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag)

                if p_j_txt_len:
                    file_p.seek(p_j_txt_pos, 0)
                    phase_txt = read_data_from_file(file_p, p_j_txt_len, real_encoder_tag)
                    print(f'第{i + 1}章节第{j+1}个词是：{phase_txt}')

                if p_j_pinyin_len:
                    file_p.seek(p_j_pinyin_pos, 0)
                    pinyin_txt = read_data_from_file(file_p, p_j_pinyin_len, real_encoder_tag)
                    print(f'第{i + 1}章节第{j+1}个词的拼音是：{pinyin_txt}')

                for k in range(p_j_shiyi_cnt):
                    file_p.seek(p_j_shiyi_pos_list[k], 0)
                    shiyi_txt = read_data_from_file(file_p, p_j_shiyi_len_list[k], real_encoder_tag)
                    print(f'第{i + 1}章节第{j + 1}个词第{k+1}个释义是：{shiyi_txt}')

            file_p.seek(s_h_pos, 0)
            sentence_num = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
            print(f'开始读取第{i+1}章节有{sentence_num}个跟读')
            for j in range(sentence_num):
                print(f'开始读取第{i + 1}章节第{j+1}个跟读')
                file_p.seek(s_h_pos + 4 + j * 4, 0)
                s_j_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                file_p.seek(s_j_pos, 0)

                s_j_txt_pos = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                s_j_txt_len = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag

                startms = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                endms = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag

                if s_j_txt_len:
                    file_p.seek(s_j_txt_pos, 0)
                    sentence_txt = read_data_from_file(file_p, s_j_txt_len, real_encoder_tag)
                    print(f'第{i + 1}章节第{j+1}个跟读是：{sentence_txt} {startms} -> {endms}')

            file_p.seek(r_h_pos, 0)
            recite_num = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
            print(f'开始读取第{i+1}章节有{recite_num}个背诵')
            for j in range(recite_num):
                print(f'开始读取第{i + 1}章节第{j+1}个背诵')
                file_p.seek(r_h_pos + 4 + j * 8, 0)

                startms = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag
                endms = struct.unpack('<I', file_p.read(4))[0] ^ real_encoder_tag

                print(f'第{i + 1}章节第{j+1}个背诵是：{startms} -> {endms}')



def wst_gen(param, old_pack_name, try_no):
    book_version = 0
    lang_en = 0
    lang_cn = 1
    lang_null = -1
    language = lang_null
    warning_msg = ''
    warn_cnt = 0
    try:
        if (old_pack_name != "new"):
            print("开始校验旧包")
            if (0 != wst_check(old_pack_name)):
                print("[E]旧包%s检验错误" % (old_pack_name))
                return 1
            book_uuid = wst_get_uuid_from_file(old_pack_name, 0)
            if (book_uuid == ""):
                print("[E]旧包%s读取UUID错误" % (old_pack_name))
                return 1
            book_version = wst_get_verno_from_file(old_pack_name, 0)
            if (book_version == -1):
                print("[E]旧包%s读取版本错误" % (old_pack_name))
                return 1
            book_version += 1
            print("旧包校验完毕")
            # print('等待更新')
            # return
        else:
            book_uuid = gen_uuid_value()
    except BaseException:
        print("[数据错误]旧包校验出错")
        return 1

    try:
        # check资源
        print("开始校验数据")
        data_parm = param + g_sep + 'StudyPackage'
        all_dirs = os.listdir(data_parm)
        all_dirs.sort(key=sort_file_dir)
        res_errno = 0
        lrc_errno = 0
        dict_errno = 0
        test_errno = 0
        chapters = []
        for sub_dir in all_dirs:
            sub_dir_name = data_parm + g_sep + sub_dir + g_sep
            if os.path.isdir(sub_dir_name):
                config_no = 0
                json_name = ''
                for filename in os.listdir(sub_dir_name):
                    if not os.path.isdir((sub_dir_name + g_sep + filename)):
                        if (filename.endswith('.json')):
                            config_no += 1
                            json_name = filename
                # json_file = sub_dir_name + sub_dir + '.json'
                audio_dir = sub_dir_name + 'audio'
                if config_no != 1:
                    warn_info = f'{sub_dir_name} json配置个数不对'
                    print(warn_info)
                    warning_msg += warn_info
                    warning_msg += '\r\n'
                    warn_cnt += 1
                    continue

                json_file = sub_dir_name + g_sep + json_name
                if not os.path.exists(json_file):
                    # print(f'{sub_dir_name} 缺少json文件 {json_file}')
                    warn_info = f'{sub_dir_name} 缺少json文件 {json_file}'
                    print(warn_info)
                    warning_msg += warn_info
                    warning_msg += '\r\n'
                    warn_cnt += 1
                    continue

                if json_name[:3] != sub_dir[:3]:
                    # print(f'{sub_dir_name} json文件名和目录名成不匹配 {json_name} -> {sub_dir}')
                    warn_info = f'{sub_dir_name} json文件名和目录名成不匹配 {json_name} -> {sub_dir}'
                    print(warn_info)
                    warning_msg += warn_info
                    warning_msg += '\r\n'
                    warn_cnt += 1
                    continue

                chapter = Chapter(sub_dir[3:], audio_dir + g_sep)
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        json_data = json.loads(f.read())
                    newWords = json_data.get('newWord')
                    print(f'字个数({len(newWords)}): {newWords}')
                    for word in newWords:
                        word_item = {}
                        text = word.get('text')
                        if text:
                            if not isinstance(text, str):
                                print(f'Error {text} 不是一个合法的字')
                                res_errno += 1
                                break
                            # print(f'字: {text.strip()}')
                            word_item['text'] = text.strip()
                        else:
                            print(f'Error {json_file} 格式错误，缺失字')
                            res_errno += 1
                            break

                        audios = word.get('audio')
                        if audios:
                            word_item['audio'] = []
                            for audio in audios:
                                if not isinstance(audio, str):
                                    # print(f'{audio} 不是一个合法的音频文件名')
                                    continue
                                audio_path = audio_dir + g_sep + audio
                                if os.path.isdir(audio_path) or not audio_path.endswith('.mp3'):
                                    print(f'Error {audio_path} 不是mp3文件')
                                    res_errno += 1
                                    break
                                if not os.path.exists(audio_path):
                                    print(f'Error {audio_path} 文件不存在')
                                    res_errno += 1
                                    break
                                # print(f'{audio_path}音频文件检测OK')
                                word_item['audio'].append(audio)
                        else:
                            # print(f'字[{text}] 没有发音音频')
                            pass

                        daudios = word.get('dictation_audio')
                        if daudios:
                            if language == lang_null:
                                print('中文书籍')
                                language = lang_cn
                            if language == lang_en:
                                print('英文书籍不支持听写音频')
                                return
                            word_item['daudio'] = []
                            print(f'{text}听写音频个数{len(daudios)}')
                            for daudio in daudios:
                                if not isinstance(daudio, str):
                                    # print(f'{daudio} 不是一个合法的音频文件名')
                                    continue
                                daudio_path = audio_dir + g_sep + daudio
                                if os.path.isdir(daudio_path) or not daudio_path.endswith('.mp3'):
                                    print(f'Error {daudio_path} 不是mp3文件')
                                    res_errno += 1
                                    break
                                if not os.path.exists(daudio_path):
                                    print(f'Error {daudio_path} 文件不存在')
                                    res_errno += 1
                                    break
                                # print(f'{audio_path}音频文件检测OK')
                                word_item['daudio'].append(daudio)
                        else:
                            # print(f'字[{text}] 没有听写音频')
                            pass

                        pinyin = word.get('pinyin')
                        if pinyin:
                            if language == lang_null:
                                print('中文书籍')
                                language = lang_cn
                            if language == lang_en:
                                print('英文书籍不支持拼音')
                                return
                            if not isinstance(pinyin, str):
                                print(f'Error {pinyin} 不是一个合法的拼音')
                                res_errno += 1
                                break
                            # print(f'拼音: {pinyin}')
                            word_item['pinyin'] = pinyin.strip()
                        else:
                            # print(f'字[{text}] 没有拼音')
                            pass

                        zucis = word.get('zuci')
                        if zucis:
                            if language == lang_null:
                                print('中文书籍')
                                language = lang_cn
                            if language == lang_en:
                                print('英文书籍不支持组词')
                                return
                            word_item['zuci'] = []
                            for zuci in zucis:
                                if not isinstance(zuci, str):
                                    print(f'Error {zuci} 不是一个合法的组词')
                                    res_errno += 1
                                    break
                                # print(f'组词: {zuci.strip()}')
                                word_item['zuci'].append(zuci.strip())
                        else:
                            # print(f'字[{text}] 没有组词')
                            pass

                        trans = word.get('shiyi')
                        if trans:
                            if language == lang_null:
                                print('英文书籍')
                                language = lang_en
                            if language == lang_cn:
                                print('中文书籍不支持释义')
                                return
                            word_item['zuci'] = []
                            if not isinstance(trans, str):
                                print(f'Error {trans} 不是一个合法的释义')
                                res_errno += 1
                                break
                            word_item['zuci'].append(trans.strip())
                        else:
                            # print(f'字[{text}] 没有组词')
                            pass
                        chapter.insert_newWord(word_item)

                    newPhases = json_data.get('newPhase')
                    print(f'词个数({len(newPhases)}): {newPhases}')
                    for phase in newPhases:
                        if language == lang_null:
                            print('中文书籍')
                            language = lang_cn
                        if language == lang_en:
                            print('英文书籍不支持词组')
                            return
                        phase_item = {}
                        text = phase.get('text')
                        if text:
                            if not isinstance(text, str):
                                print(f'Error {text} 不是一个合法的词')
                                res_errno += 1
                                break
                            # print(f'词: {text.strip()}')
                            phase_item['text'] = text.strip()
                        else:
                            print(f'Error {json_file} 格式错误，缺失字')
                            res_errno += 1
                            break

                        audios = phase.get('audio')
                        if audios:
                            phase_item['audio'] = []
                            for audio in audios:
                                if not isinstance(audio, str):
                                    # print(f'{audio} 不是一个合法的音频文件名')
                                    continue
                                audio_path = audio_dir + g_sep + audio
                                if os.path.isdir(audio_path) or not audio_path.endswith('.mp3'):
                                    print(f'Error {audio_path} 不是mp3文件')
                                    res_errno += 1
                                    break
                                if not os.path.exists(audio_path):
                                    print(f'Error {audio_path} 文件不存在')
                                    res_errno += 1
                                    break
                                # print(f'{audio_path}音频文件检测OK')
                                phase_item['audio'].append(audio)
                        else:
                            # print(f'词[{text}] 没有发音音频')
                            pass

                        daudios = phase.get('dictation_audio')
                        if daudios:
                            phase_item['daudio'] = []
                            for daudio in daudios:
                                if not isinstance(daudio, str):
                                    # print(f'{daudio} 不是一个合法的音频文件名')
                                    continue
                                daudio_path = audio_dir + g_sep + daudio
                                if os.path.isdir(daudio_path) or not daudio_path.endswith('.mp3'):
                                    print(f'Error {daudio_path} 不是mp3文件')
                                    res_errno += 1
                                    break
                                if not os.path.exists(daudio_path):
                                    print(f'Error {daudio_path} 文件不存在')
                                    res_errno += 1
                                    break
                                # print(f'{audio_path}音频文件检测OK')
                                phase_item['daudio'].append(daudio)
                        else:
                            # print(f'词[{text}] 没有听写音频')
                            pass

                        pinyin = phase.get('pinyin')
                        if pinyin:
                            if not isinstance(pinyin, str):
                                print(f'Error {pinyin} 不是一个合法的拼音')
                                res_errno += 1
                                break
                            # print(f'拼音: {pinyin.strip()}')
                            phase_item['pinyin'] = pinyin.strip()
                        else:
                            # print(f'词[{text}] 没有拼音')
                            pass

                        shiyis = phase.get('shiyi')
                        if shiyis:
                            phase_item['shiyi'] = []
                            for shiyi in shiyis:
                                if not isinstance(shiyi, str):
                                    print(f'Error {shiyi} 不是一个合法的释义')
                                    res_errno += 1
                                    break
                                phase_item['shiyi'].append(shiyi.strip())
                        else:
                            # print(f'词[{text}] 没有释义')
                            pass
                        chapter.insert_newPhase(phase_item)

                    newSentences = json_data.get('newSentence')
                    print(f'跟读({len(newSentences)}): {newSentences}')
                    for newSentence in newSentences:
                        # print(newSentence)
                        sentence_item = {}
                        lrc = newSentence.get('content')
                        if lrc and isinstance(lrc, str):
                            sentence_item['lrc'] = lrc.strip()
                        timeStart = newSentence.get('timeStart')
                        timeEnd = newSentence.get('timeEnd')
                        if isinstance(timeStart, str) and isinstance(timeEnd, str):
                            try:
                                start_split = timeStart.split(':')
                                end_split = timeEnd.split(':')
                                # end_ms = 0
                                if len(start_split) != 2:
                                    print(f'Error 跟读起始时间格式不对{timeStart}')
                                    return
                                if len(end_split) != 2:
                                    end_ms = 0
                                else:
                                    end_m = int(end_split[0])
                                    end_ms = end_m * 60 * 1000 + int(float(end_split[1]) * 1000)

                                start_m = int(start_split[0])

                                start_ms = start_m * 60 * 1000 + int(float(start_split[1]) * 1000)

                                print(f'跟读 {start_ms} -> {end_ms}')
                                sentence_item['startms'] = start_ms
                                sentence_item['end_ms'] = end_ms
                                chapter.insert_newSentence(sentence_item)
                            except Exception as e:
                                print(e)
                                return

                    recites = json_data.get('recite')
                    print(f'背诵个数({len(recites)}): {recites}')
                    for recite in recites:
                        recite_item = {}
                        timeStart = recite.get('timeStart')
                        timeEnd = recite.get('timeEnd')
                        if isinstance(timeStart, str) and isinstance(timeEnd, str):
                            try:
                                start_split = timeStart.split(':')
                                end_split = timeEnd.split(':')
                                # end_ms = 0
                                if len(start_split) != 2:
                                    print(f'Error 背诵起始时间格式不对{timeStart}')
                                    return
                                if len(end_split) != 2:
                                    end_ms = 0
                                else:
                                    end_m = int(end_split[0])
                                    end_ms = end_m * 60 * 1000 + int(float(end_split[1]) * 1000)

                                start_m = int(start_split[0])

                                start_ms = start_m * 60 * 1000 + int(float(start_split[1]) * 1000)

                                print(f'背诵 {start_ms} -> {end_ms}')
                                recite_item['startms'] = start_ms
                                recite_item['end_ms'] = end_ms
                                chapter.insert_recite(recite_item)
                            except Exception as e:
                                print(e)
                                return

                    # chapter.dump_chapter_info()
                    chapters.append(chapter)
                except Exception as e:
                    print(e)
                    return


        if (0 != res_errno) or (0 != lrc_errno) or (0 != dict_errno) or (0 != test_errno):
            print("请修正以上错误")
            return
        print("数据校验完毕")
        # return
    except BaseException as e:
        print("[数据错误]校验资源出错" + e.message())
        return

    # try:
    if True:
        print("开始写入版本信息数据...")

        #############################
        ####below is gennerate ziyou format ####
        #############################
        params_list = param.split(g_sep)
        book_filename = params_list[-1]
        print(f'=======文件名： {book_filename} ============')
        if (1 == try_no):
            ziyou_file_name = param + g_sep + book_filename + "_try_v" + str(book_version) + BOOK_SUFFIX_NAME
        else:
            ziyou_file_name = param + g_sep + book_filename + "_v" + str(book_version) + BOOK_SUFFIX_NAME

        # 产生自有格式文件
        ziyou_file = open(ziyou_file_name, "wb")

        # 创建时间
        create_time = time.strftime("CT%Y%m%d%H%M%S", time.localtime())
        ziyou_file.write(bytes(create_time, encoding="utf8"))

        # 校验数据
        check_len = 0
        check_sum = 0
        # checksum_pos = ziyou_file.tell()
        ziyou_file.write(check_len.to_bytes(length=4, byteorder='little', signed=False))
        ziyou_file.write(check_sum.to_bytes(length=4, byteorder='little', signed=False))

        # print(f'校验段起始 {ziyou_file.tell()}')
        # 加密数据信息
        encoder_type = random.randint(1, 0xffe) * 16 + random.randint(1, 3)
        check_sum += encoder_type
        check_len += 2
        ziyou_file.write(encoder_type.to_bytes(length=2, byteorder='little', signed=False))
        encoder_tag = random.randint(1, 0xfffe)
        check_sum += encoder_tag
        check_len += 2
        ziyou_file.write(encoder_tag.to_bytes(length=2, byteorder='little', signed=False))

        real_encoder_tag = compute_real_tag(encoder_type, encoder_tag)

        # 工具版本号
        write_data = SOFT_VERSION ^ real_encoder_tag
        check_sum += (write_data & 0xffff)
        check_sum += ((write_data & 0xffff0000) >> 16)
        check_len += 4
        ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

        # 版本
        if (try_no == 1):
            book_version = book_version + 0x10000
        write_data = book_version ^ real_encoder_tag
        check_sum += (write_data & 0xffff)
        check_sum += ((write_data & 0xffff0000) >> 16)
        check_len += 4
        ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

        # uuid,不加密
        # print(f'real_encoder_tag: {encoder_type}, {encoder_tag} -> {real_encoder_tag} uuid({book_uuid}) pos: {ziyou_file.tell()}')
        checksum_new, checksum_error = write_data_to_file(ziyou_file, book_uuid, BOOK_UUID_LEN, 0)
        if (0 != checksum_error):
            print("string checksum len error")
            return
        check_sum += checksum_new
        check_len += BOOK_UUID_LEN

        # package name
        checksum_new, checksum_error = write_data_to_file(ziyou_file, book_filename, BOOK_NAME_LEN, real_encoder_tag)
        if (0 != checksum_error):
            print("string checksum len error")
            return
        check_sum += checksum_new
        check_len += BOOK_NAME_LEN

        # 章节数量统计
        res_total_no = len(chapters)
        if language == lang_cn:
            res_total_no += 0x10000
        else:
            res_total_no += 0x20000
        write_data = res_total_no ^ real_encoder_tag
        check_sum += (write_data & 0xffff)
        check_sum += ((write_data & 0xffff0000) >> 16)
        check_len += 4
        ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))
        print(f'章节数：{res_total_no}')

        print("开始写入头部数据...")
        zhanwei_list = []
        # 章节信息偏移
        chapter_head_list_pos = []
        chapter_words_addr = []
        chapter_phase_addr = []
        chapter_sentence_addr = []
        chapter_recite_addr = []
        for i in range(len(chapters)):
            cur_pos = ziyou_file.tell()
            chapter_head_list_pos.append(cur_pos)
            # print(f'预留第{i+1}章节头部信息位置: {cur_pos}')
            # 每个章节的信息: 该书有n个章节，每个章节信息存储在哪个位置
            zhanwei_list.append(cur_pos)
            zhanwei_list.append(cur_pos + 4)
            zhanwei_list.append(cur_pos + 4 * 2)
            zhanwei_list.append(cur_pos + 4 * 3)
            zhanwei_list.append(cur_pos + 4 * 4)
            zhanwei_list.append(cur_pos + 4 * 5)
            # 章节名
            ziyou_file.write(b"\xff" * (4))  # 占位
            ziyou_file.write(b"\xff" * (4))  # 占位
            # 字列表offset
            ziyou_file.write(b"\xff" * (4))  # 占位
            # 词列表offset
            ziyou_file.write(b"\xff" * (4))
            # 跟读列表offset
            ziyou_file.write(b"\xff" * (4))
            # 背诵列表offset
            ziyou_file.write(b"\xff" * (4))

        # 字信息
        words_num_pos_list = []  # 每个章节的字信息 字描述偏移位置     2层 章节->字
        words_addr_list = []    # 字信息实际描述地址，用于写入 words_num_pos_list，也是字地址，往这个地址填充字(文本)存储位置 2层 章节->字
        words_pinyin_addr_list = []    #拼音

        words_audio_addr_post_list = []  #音频位置，3层 章节->字->1个字可能有多个音频
        words_daudio_addr_post_list = []  #音频位置，3层 章节->字->1个字可能有多个音频
        words_zuci_addr_post_list = []  #组词位置，3层 章节->字->1个字可能有多个组词

        # 写字描述信息
        for i in range(len(chapters)):
            chapter = chapters[i]
            new_words = chapter.get_newWord()
            # print(new_words)
            chapter_words_addr.append(ziyou_file.tell())
            # print(f'第{i+1}章节字信息描述位置{ziyou_file.tell()}')
            # 字总个数
            word_num = len(new_words)
            write_data = word_num ^ real_encoder_tag
            check_sum += (write_data & 0xffff)
            check_sum += ((write_data & 0xffff0000) >> 16)
            check_len += 4
            ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))
            word_num_pos = []
            for ip in range(word_num): # 该章节有word_num个字，表示每个字的信息存储在哪个地址
                cur_pos = ziyou_file.tell()
                word_num_pos.append(cur_pos)
                # print(f'预留 第{i+1}章节 第{ip+1}个字信息在位置：{cur_pos}')
                ziyou_file.write(b"\xff" * (4))  # 占位
                zhanwei_list.append(cur_pos)
            words_num_pos_list.append(word_num_pos)
            word_addr_pos = []
            word_pinyin_addr_pos = []
            word_audio_list = []
            word_daudio_list = []
            word_zuci_list = []
            for iw in range(word_num):
                # print(f'预留 在位置：{ziyou_file.tell()} 写入第{i + 1}章节 第{iw + 1}个字信息')
                cur_pos = ziyou_file.tell()
                word_addr_pos.append(cur_pos)
                # 预留 地址，长度 字长度不做固定
                zhanwei_list.append(cur_pos)
                zhanwei_list.append(cur_pos + 4)
                zhanwei_list.append(cur_pos + 4 * 2)
                zhanwei_list.append(cur_pos + 4 * 3)

                ziyou_file.write(b"\xff" * (4))  # 占位
                ziyou_file.write(b"\xff" * (4))

                word_pinyin_addr_pos.append(ziyou_file.tell())
                # 预留 地址，长度 拼音长度不做固定
                ziyou_file.write(b"\xff" * (4))  # 占位
                ziyou_file.write(b"\xff" * (4))

                # 音频个数
                audios = new_words[iw].get('audio')
                audios_num = 0
                if audios:
                    audios_num = len(audios)
                write_data = audios_num ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))
                word_audio_pos = []
                for a in range(audios_num):
                    # 预留 地址，音频地址 长度
                    cur_pos = ziyou_file.tell()
                    word_audio_pos.append(cur_pos)
                    zhanwei_list.append(cur_pos)
                    zhanwei_list.append(cur_pos + 4)
                    # print(f'预留 第{i+1}章节 第{iw+1}个字 第{a+1} 个音频信息在位置：{cur_pos}')
                    ziyou_file.write(b"\xff" * (4))  # 占位
                    ziyou_file.write(b"\xff" * (4))
                word_audio_list.append(word_audio_pos)

                # 听写音频个数
                daudios = new_words[iw].get('daudio')
                daudios_num = 0
                if daudios:
                    daudios_num = len(daudios)
                write_data = daudios_num ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))
                word_daudio_pos = []
                for a in range(daudios_num):
                    # 预留 地址，音频地址 长度
                    cur_pos = ziyou_file.tell()
                    word_daudio_pos.append(cur_pos)
                    zhanwei_list.append(cur_pos)
                    zhanwei_list.append(cur_pos + 4)
                    # print(f'预留 第{i+1}章节 第{iw+1}个字 第{a+1} 个音频信息在位置：{cur_pos}')
                    ziyou_file.write(b"\xff" * (4))  # 占位
                    ziyou_file.write(b"\xff" * (4))
                word_daudio_list.append(word_daudio_pos)

                # 组词个数
                zucis = new_words[iw].get('zuci')
                zucis_num = 0
                if zucis:
                    zucis_num = len(zucis)
                write_data = zucis_num ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                word_zuci_pos = []
                for a in range(zucis_num):
                    # 预留 地址，组词地址 长度
                    cur_pos = ziyou_file.tell()
                    zhanwei_list.append(cur_pos)
                    zhanwei_list.append(cur_pos + 4)
                    word_zuci_pos.append(cur_pos)
                    # print(f'预留 第{i + 1}章节 第{iw + 1}个字 第{a + 1} 个组词信息在位置：{cur_pos}')
                    ziyou_file.write(b"\xff" * (4))  # 占位
                    ziyou_file.write(b"\xff" * (4))
                word_zuci_list.append(word_zuci_pos)

            words_addr_list.append(word_addr_pos)
            words_pinyin_addr_list.append(word_pinyin_addr_pos)
            words_audio_addr_post_list.append(word_audio_list)
            words_daudio_addr_post_list.append(word_daudio_list)
            words_zuci_addr_post_list.append(word_zuci_list)

        # 词信息
        phase_num_pos_list = []  # 每个章节的字信息 词描述偏移位置     2层 章节->词
        phase_addr_list = []    # 字信息实际描述地址，用于写入 phase_num_pos_list，也是词地址，往这个地址填充词(文本)存储位置 2层 章节->词
        phase_pinyin_addr_list = []    #拼音

        phase_audio_addr_post_list = []  #音频位置，3层 章节->词->1个词可能有多个音频
        phase_daudio_addr_post_list = []  #音频位置，3层 章节->词->1个词可能有多个音频
        phase_shiyi_addr_post_list = []  #组词位置，3层 章节->词->1个词可能有多个组词

        # 写词描述信息
        for i in range(len(chapters)):
            chapter = chapters[i]
            new_phase = chapter.get_newPhase()
            # print(new_phase)
            chapter_phase_addr.append(ziyou_file.tell())
            # print(f'第{i+1}章节词信息描述位置{ziyou_file.tell()}')
            # 词总个数
            phase_num = len(new_phase)
            write_data = phase_num ^ real_encoder_tag
            check_sum += (write_data & 0xffff)
            check_sum += ((write_data & 0xffff0000) >> 16)
            check_len += 4
            ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))
            phase_num_pos = []
            for ip in range(phase_num):  # 该章节有phase_num个词，表示每个词的信息存储在哪个地址
                cur_pos = ziyou_file.tell()
                zhanwei_list.append(cur_pos)
                phase_num_pos.append(ziyou_file.tell())
                # print(f'预留 第{i+1}章节 第{ip+1}个词信息在位置：{ziyou_file.tell()}')
                ziyou_file.write(b"\xff" * (4))  # 占位
            phase_num_pos_list.append(phase_num_pos)
            phase_addr_pos = []
            phase_pinyin_addr_pos = []
            phase_audio_list = []
            phase_daudio_list = []
            phase_shiyi_list = []
            for iw in range(phase_num):
                # print(f'预留 在位置：{ziyou_file.tell()} 写入第{i + 1}章节 第{iw + 1}个词信息')
                cur_pos = ziyou_file.tell()
                zhanwei_list.append(cur_pos)
                zhanwei_list.append(cur_pos + 4)
                zhanwei_list.append(cur_pos + 4 * 2)
                zhanwei_list.append(cur_pos + 4 * 3)
                phase_addr_pos.append(ziyou_file.tell())
                # 预留 地址，长度 字长度不做固定
                ziyou_file.write(b"\xff" * (4))  # 占位
                ziyou_file.write(b"\xff" * (4))

                phase_pinyin_addr_pos.append(ziyou_file.tell())
                # 预留 地址，长度 拼音长度不做固定
                ziyou_file.write(b"\xff" * (4))  # 占位
                ziyou_file.write(b"\xff" * (4))

                # 音频个数
                audios = new_phase[iw].get('audio')
                audios_num = 0
                if audios:
                    audios_num = len(audios)
                write_data = audios_num ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))
                phase_audio_pos = []
                for a in range(audios_num):
                    # 预留 地址，音频地址 长度
                    cur_pos = ziyou_file.tell()
                    zhanwei_list.append(cur_pos)
                    zhanwei_list.append(cur_pos + 4)
                    phase_audio_pos.append(ziyou_file.tell())
                    # print(f'预留 第{i+1}章节 第{iw+1}个词 第{a+1} 个音频信息在位置：{ziyou_file.tell()}')
                    ziyou_file.write(b"\xff" * (4))  # 占位
                    ziyou_file.write(b"\xff" * (4))
                phase_audio_list.append(phase_audio_pos)

                # 听写音频个数
                daudios = new_phase[iw].get('daudio')
                daudios_num = 0
                if daudios:
                    daudios_num = len(daudios)
                write_data = daudios_num ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))
                phase_daudio_pos = []
                for a in range(daudios_num):
                    # 预留 地址，音频地址 长度
                    cur_pos = ziyou_file.tell()
                    zhanwei_list.append(cur_pos)
                    zhanwei_list.append(cur_pos + 4)
                    phase_daudio_pos.append(ziyou_file.tell())
                    # print(f'预留 第{i+1}章节 第{iw+1}个词 第{a+1} 个音频信息在位置：{ziyou_file.tell()}')
                    ziyou_file.write(b"\xff" * (4))  # 占位
                    ziyou_file.write(b"\xff" * (4))
                phase_daudio_list.append(phase_daudio_pos)

                # 组词个数
                shiyis = new_phase[iw].get('shiyi')
                shiyis_num = 0
                if shiyis:
                    shiyis_num = len(shiyis)
                write_data = shiyis_num ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                phase_shiyi_pos = []
                for a in range(shiyis_num):
                    # 预留 地址，组词地址 长度
                    cur_pos = ziyou_file.tell()
                    zhanwei_list.append(cur_pos)
                    zhanwei_list.append(cur_pos + 4)
                    phase_shiyi_pos.append(ziyou_file.tell())
                    # print(f'预留 第{i + 1}章节 第{iw + 1}个词 第{a + 1} 个释义信息在位置：{ziyou_file.tell()}')
                    ziyou_file.write(b"\xff" * (4))  # 占位
                    ziyou_file.write(b"\xff" * (4))
                phase_shiyi_list.append(phase_shiyi_pos)

            phase_addr_list.append(phase_addr_pos)
            phase_pinyin_addr_list.append(phase_pinyin_addr_pos)
            phase_audio_addr_post_list.append(phase_audio_list)
            phase_daudio_addr_post_list.append(phase_daudio_list)
            phase_shiyi_addr_post_list.append(phase_shiyi_list)

        # 跟读信息
        sentence_num_pos_list = []  # 每个章节的听写信息 词描述偏移位置     2层 章节->跟读
        sentence_addr_list = []    # 听写信息实际描述地址，用于写入 sentence_num_pos_list，也是听写地址，往这个地址填充听写(文本)存储位置 2层 章节->跟读

        # 写跟读描述信息
        for i in range(len(chapters)):
            chapter = chapters[i]
            sentence = chapter.get_newSentence()
            # print(sentence)
            chapter_sentence_addr.append(ziyou_file.tell())
            # print(f'第{i+1}章节跟读信息描述位置{ziyou_file.tell()}')
            # 跟读总个数
            sentence_num = len(sentence)
            write_data = sentence_num ^ real_encoder_tag
            check_sum += (write_data & 0xffff)
            check_sum += ((write_data & 0xffff0000) >> 16)
            check_len += 4
            ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))
            sentence_num_pos = []
            for ip in range(sentence_num):  # 该章节有sentence_num个跟读，表示每个跟读的信息存储在哪个地址
                cur_pos = ziyou_file.tell()
                zhanwei_list.append(cur_pos)
                sentence_num_pos.append(ziyou_file.tell())
                # print(f'预留 第{i+1}章节 第{ip+1}个跟读信息在位置：{ziyou_file.tell()}')
                ziyou_file.write(b"\xff" * (4))  # 占位
            sentence_num_pos_list.append(sentence_num_pos)
            sentence_addr_pos = []
            for iw in range(sentence_num):
                # print(f'预留 在位置：{ziyou_file.tell()} 写入第{i + 1}章节 第{iw + 1}个跟读信息')
                cur_pos = ziyou_file.tell()
                zhanwei_list.append(cur_pos)
                zhanwei_list.append(cur_pos + 4)
                sentence_addr_pos.append(ziyou_file.tell())
                # 预留 地址，长度 跟读长度不做固定
                ziyou_file.write(b"\xff" * (4))  # 占位
                ziyou_file.write(b"\xff" * (4))

                # 跟读时间
                startms = sentence[iw].get('startms')
                write_data = startms ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                end_ms = sentence[iw].get('end_ms')
                write_data = end_ms ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

            sentence_addr_list.append(sentence_addr_pos)

        # 背诵信息
        recite_num_pos_list = []  # 每个章节的背诵信息 背诵描述偏移位置     2层 章节->背诵
        recite_addr_list = []    # 背诵信息实际描述地址

        # 写背诵描述信息
        for i in range(len(chapters)):
            chapter = chapters[i]
            recite = chapter.get_recite()
            # print(recite)
            chapter_recite_addr.append(ziyou_file.tell())
            # print(f'第{i+1}章节背诵信息描述位置{ziyou_file.tell()}')
            #  背诵总个数
            recite_num = len(recite)
            write_data = recite_num ^ real_encoder_tag
            check_sum += (write_data & 0xffff)
            check_sum += ((write_data & 0xffff0000) >> 16)
            check_len += 4
            ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))
            recite_num_pos = []
            # for ip in range(recite_num):  # 该章节有recite_num个背诵，表示每个背诵的信息存储在哪个地址
            #     cur_pos = ziyou_file.tell()
            #     zhanwei_list.append(cur_pos)
            #     recite_num_pos.append(ziyou_file.tell())
            #     print(f'预留 第{i+1}章节 第{ip+1}个背诵信息在位置：{ziyou_file.tell()}')
            #     ziyou_file.write(b"\xff" * (4))  # 占位
            recite_num_pos_list.append(recite_num_pos)
            recite_addr_pos = []
            for iw in range(recite_num):
                # print(f'在位置：{ziyou_file.tell()} 写入第{i + 1}章节 第{iw + 1}个背诵信息')
                recite_addr_pos.append(ziyou_file.tell())

                # 背诵时间
                startms = recite[iw].get('startms')
                write_data = startms ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                end_ms = recite[iw].get('end_ms')
                write_data = end_ms ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

            recite_addr_list.append(recite_addr_pos)

        print(f'开始写数据内容... {ziyou_file.tell()}')
        # print(f'占位符个数{len(zhanwei_list)} : {zhanwei_list}')
        # 写 章节名
        chapter_name_write_pos_list = []   # 对应
        chapter_name_write_len_list = []

        for i in range(len(chapters)):
            chapter = chapters[i]
            chapter_name = chapter.get_chapter_name()
            txt_utf_8_len = len(chapter_name.encode('utf-8'))
            txt_len = 4 * int((txt_utf_8_len + 3) / 4)
            chapter_name_write_pos_list.append(ziyou_file.tell())
            # print(f'第 {i+1} 章节名保存地址 {ziyou_file.tell()}')
            chapter_name_write_len_list.append(txt_len)
            checksum_new, checksum_error = write_data_to_file(ziyou_file, chapter_name, txt_len, real_encoder_tag)
            if 0 != checksum_error:
                print(f"[打包错误]写入字 {txt} 文本错误")
                return

        write_mp3_dict = {}
        # 写 字 内容
        word_txt_write_pos_list = []   # 对应 words_num_pos_list
        word_txt_write_len_list = []

        word_pinyin_write_pos_list = []
        word_pinyin_write_len_list = []

        word_zuci_write_pos_list = []
        word_zuci_write_len_list = []

        word_audio_write_pos_list = []
        word_audio_write_len_list = []

        word_daudio_write_pos_list = []
        word_daudio_write_len_list = []

        for i in range(len(chapters)):
            chapter = chapters[i]
            words = chapter.get_newWord()
            txt_write_pos = []
            txt_write_len = []

            pinyin_write_pos = []
            pinyin_write_len = []

            zuci_write_pos = []
            zuci_write_len = []

            audio_write_pos = []
            audio_write_len = []

            daudio_write_pos = []
            daudio_write_len = []

            for iw in range(len(words)):
                txt = words[iw].get('text')
                txt_utf_8_len = len(txt.encode('utf-8'))
                txt_len = 4 * int((txt_utf_8_len + 3) / 4)

                # 字 文本内容
                txt_write_pos.append(ziyou_file.tell())
                # print(f'第 {i+1} 章节 第 {iw+1} 字 文本保存地址 {ziyou_file.tell()}')
                txt_write_len.append(txt_len)
                checksum_new, checksum_error = write_data_to_file(ziyou_file, txt, txt_len, real_encoder_tag)
                if 0 != checksum_error:
                    print(f"[打包错误]写入字 {txt} 文本错误")
                    return

                # 字 拼音内容
                pinyin = words[iw].get('pinyin')
                if pinyin:
                    # pinyin_len = 4 * int((len(pinyin) * 2 + 2) / 4)
                    txt_utf_8_len = len(pinyin.encode('utf-8'))
                    pinyin_len = 4 * int((txt_utf_8_len + 3) / 4)

                    pinyin_write_pos.append(ziyou_file.tell())
                    pinyin_write_len.append(pinyin_len)
                    # print(f'第 {i + 1} 章节 第 {iw + 1} 字 拼音保存地址 {ziyou_file.tell()}')
                    checksum_new, checksum_error = write_data_to_file(ziyou_file, pinyin, pinyin_len, real_encoder_tag)
                    if 0 != checksum_error:
                        print(f"[打包错误]写入拼音 {pinyin} 文本错误")
                        return
                else:
                    pinyin_write_pos.append(0)
                    pinyin_write_len.append(0)

                # 字 组词内容
                zucis = words[iw].get('zuci')
                zuci_sub_w_pos = []
                zuci_sub_w_len = []
                if zucis:
                    zuci_cnt = len(zucis)
                    for iz in range(zuci_cnt):
                        zuci_txt = zucis[iz]
                        # zuci_txt_len = 4 * int((len(zuci_txt) * 2 + 2) / 4)
                        txt_utf_8_len = len(zuci_txt.encode('utf-8'))
                        zuci_txt_len = 4 * int((txt_utf_8_len + 3) / 4)

                        zuci_sub_w_pos.append(ziyou_file.tell())
                        zuci_sub_w_len.append(zuci_txt_len)
                        # print(f'第 {i + 1} 章节 第 {iw + 1} 字 第{iz+1}个组词保存地址 {ziyou_file.tell()}')
                        checksum_new, checksum_error = write_data_to_file(ziyou_file, zuci_txt, zuci_txt_len,
                                                                          real_encoder_tag)
                        if 0 != checksum_error:
                            print(f"[打包错误]写入组词 {zuci_txt} 文本错误: {checksum_error}")
                            return
                zuci_write_pos.append(zuci_sub_w_pos)
                zuci_write_len.append(zuci_sub_w_len)

                # 字 音频内容
                audios = words[iw].get('audio')
                audio_prefix = chapter.get_audio_dir()
                audio_sub_w_pos = []
                audio_sub_w_len = []
                if audios:
                    audio_cnt = len(audios)
                    for iz in range(audio_cnt):
                        audio_path = audio_prefix + audios[iz]
                        mp3_write = write_mp3_dict.get(audio_path)
                        if mp3_write:
                            mp3_pos = mp3_write.get('pos')
                            audio_sub_w_pos.append(mp3_pos)
                            audio_sub_w_len.append(mp3_write.get('len'))
                            # print(f'{audio_path} 已经写过，使用上个地址 {mp3_pos}')
                        else:
                            # print(f'写音频 {audio_path} -> {ziyou_file.tell()}')
                            audio_sub_w_pos.append(ziyou_file.tell())
                            data_len = os.path.getsize(audio_path)
                            audio_sub_w_len.append(data_len)
                            # 写音频记录
                            write_mp3_dict[audio_path] = {}
                            write_mp3_dict[audio_path]['pos'] = ziyou_file.tell()
                            write_mp3_dict[audio_path]['len'] = data_len
                            # 写音频
                            write_filedata_to_file(ziyou_file, audio_path, data_len, real_encoder_tag)

                # 字 听写音频内容
                daudios = words[iw].get('daudio')
                audio_prefix = chapter.get_audio_dir()
                daudio_sub_w_pos = []
                daudio_sub_w_len = []
                if daudios:
                    daudio_cnt = len(daudios)
                    for iz in range(daudio_cnt):
                        daudio_path = audio_prefix + daudios[iz]
                        mp3_write = write_mp3_dict.get(daudio_path)
                        if mp3_write:
                            mp3_pos = mp3_write.get('pos')
                            daudio_sub_w_pos.append(mp3_pos)
                            daudio_sub_w_len.append(mp3_write.get('len'))
                            # print(f'{audio_path} 已经写过，使用上个地址 {mp3_pos}')
                        else:
                            # print(f'写音频 {audio_path} -> {ziyou_file.tell()}')
                            daudio_sub_w_pos.append(ziyou_file.tell())
                            data_len = os.path.getsize(daudio_path)
                            daudio_sub_w_len.append(data_len)
                            # 写音频记录
                            write_mp3_dict[daudio_path] = {}
                            write_mp3_dict[daudio_path]['pos'] = ziyou_file.tell()
                            write_mp3_dict[daudio_path]['len'] = data_len
                            # 写音频
                            write_filedata_to_file(ziyou_file, daudio_path, data_len, real_encoder_tag)

                audio_write_pos.append(audio_sub_w_pos)
                audio_write_len.append(audio_sub_w_len)
                daudio_write_pos.append(daudio_sub_w_pos)
                daudio_write_len.append(daudio_sub_w_len)

            word_txt_write_pos_list.append(txt_write_pos)
            word_txt_write_len_list.append(txt_write_len)
            word_pinyin_write_pos_list.append(pinyin_write_pos)
            word_pinyin_write_len_list.append(pinyin_write_len)
            word_zuci_write_pos_list.append(zuci_write_pos)
            word_zuci_write_len_list.append(zuci_write_len)
            word_audio_write_pos_list.append(audio_write_pos)
            word_audio_write_len_list.append(audio_write_len)
            word_daudio_write_pos_list.append(daudio_write_pos)
            word_daudio_write_len_list.append(daudio_write_len)

        # 写 词 内容
        phase_txt_write_pos_list = []
        phase_txt_write_len_list = []

        phase_pinyin_write_pos_list = []
        phase_pinyin_write_len_list = []

        phase_shiyi_write_pos_list = []
        phase_shiyi_write_len_list = []

        phase_audio_write_pos_list = []
        phase_audio_write_len_list = []

        phase_daudio_write_pos_list = []
        phase_daudio_write_len_list = []

        for i in range(len(chapters)):
            chapter = chapters[i]
            phases = chapter.get_newPhase()
            txt_write_pos = []
            txt_write_len = []

            pinyin_write_pos = []
            pinyin_write_len = []

            shiyi_write_pos = []
            shiyi_write_len = []

            audio_write_pos = []
            audio_write_len = []

            daudio_write_pos = []
            daudio_write_len = []

            for iw in range(len(phases)):
                txt = phases[iw].get('text')
                # txt_len = 4 * int((len(txt) * 2 + 2) / 4)
                txt_utf_8_len = len(txt.encode('utf-8'))
                txt_len = 4 * int((txt_utf_8_len + 3) / 4)

                # 词 文本内容
                txt_write_pos.append(ziyou_file.tell())
                txt_write_len.append(txt_len)
                checksum_new, checksum_error = write_data_to_file(ziyou_file, txt, txt_len, real_encoder_tag)
                if 0 != checksum_error:
                    print(f"[打包错误]写入词 {txt} 文本错误")
                    return

                # 词 拼音内容
                pinyin = phases[iw].get('pinyin')
                if pinyin:
                    # pinyin_len = 4 * int((len(pinyin) * 2 + 2) / 4)
                    txt_utf_8_len = len(pinyin.encode('utf-8'))
                    pinyin_len = 4 * int((txt_utf_8_len + 3) / 4)

                    pinyin_write_pos.append(ziyou_file.tell())
                    pinyin_write_len.append(pinyin_len)
                    checksum_new, checksum_error = write_data_to_file(ziyou_file, pinyin, pinyin_len, real_encoder_tag)
                    if 0 != checksum_error:
                        print(f"[打包错误]写入拼音 {pinyin} 文本错误")
                        return
                else:
                    pinyin_write_pos.append(0)
                    pinyin_write_len.append(0)

                # 词 组词内容
                shiyis = phases[iw].get('shiyi')
                shiyi_sub_w_pos = []
                shiyi_sub_w_len = []
                if shiyis:
                    shiyi_cnt = len(shiyis)
                    for iz in range(shiyi_cnt):
                        shiyi_txt = shiyis[iz]
                        # zuci_txt_len = 4 * int((len(zuci_txt) * 2 + 2) / 4)
                        txt_utf_8_len = len(shiyi_txt.encode('utf-8'))
                        shiyi_txt_len = 4 * int((txt_utf_8_len + 3) / 4)

                        shiyi_sub_w_pos.append(ziyou_file.tell())
                        shiyi_sub_w_len.append(shiyi_txt_len)
                        checksum_new, checksum_error = write_data_to_file(ziyou_file, shiyi_txt, shiyi_txt_len,
                                                                          real_encoder_tag)
                        if 0 != checksum_error:
                            print(f"[打包错误]写入释义 {shiyi_txt} 文本错误")
                            return
                shiyi_write_pos.append(shiyi_sub_w_pos)
                shiyi_write_len.append(shiyi_sub_w_len)

                # 词 音频内容
                audios = phases[iw].get('audio')
                audio_prefix = chapter.get_audio_dir()
                audio_sub_w_pos = []
                audio_sub_w_len = []
                if audios:
                    audio_cnt = len(audios)
                    for iz in range(audio_cnt):
                        audio_path = audio_prefix + audios[iz]
                        mp3_write = write_mp3_dict.get(audio_path)
                        if mp3_write:
                            mp3_pos = mp3_write.get('pos')
                            audio_sub_w_pos.append(mp3_pos)
                            audio_sub_w_len.append(mp3_write.get('len'))
                            # print(f'{audio_path} 已经写过，使用上个地址 {mp3_pos}')
                        else:
                            # print(f'写音频 {audio_path} -> {ziyou_file.tell()}')
                            audio_sub_w_pos.append(ziyou_file.tell())
                            data_len = os.path.getsize(audio_path)
                            audio_sub_w_len.append(data_len)
                            # 写音频记录
                            write_mp3_dict[audio_path] = {}
                            write_mp3_dict[audio_path]['pos'] = ziyou_file.tell()
                            write_mp3_dict[audio_path]['len'] = data_len
                            # 写音频
                            write_filedata_to_file(ziyou_file, audio_path, data_len, real_encoder_tag)

                audio_write_pos.append(audio_sub_w_pos)
                audio_write_len.append(audio_sub_w_len)

                # 词 听写音频内容
                daudios = phases[iw].get('daudio')
                audio_prefix = chapter.get_audio_dir()
                daudio_sub_w_pos = []
                daudio_sub_w_len = []
                if daudios:
                    daudio_cnt = len(daudios)
                    for iz in range(daudio_cnt):
                        daudio_path = audio_prefix + daudios[iz]
                        mp3_write = write_mp3_dict.get(daudio_path)
                        if mp3_write:
                            mp3_pos = mp3_write.get('pos')
                            daudio_sub_w_pos.append(mp3_pos)
                            daudio_sub_w_len.append(mp3_write.get('len'))
                            # print(f'{audio_path} 已经写过，使用上个地址 {mp3_pos}')
                        else:
                            # print(f'写音频 {audio_path} -> {ziyou_file.tell()}')
                            daudio_sub_w_pos.append(ziyou_file.tell())
                            data_len = os.path.getsize(daudio_path)
                            daudio_sub_w_len.append(data_len)
                            # 写音频记录
                            write_mp3_dict[daudio_path] = {}
                            write_mp3_dict[daudio_path]['pos'] = ziyou_file.tell()
                            write_mp3_dict[daudio_path]['len'] = data_len
                            # 写音频
                            write_filedata_to_file(ziyou_file, daudio_path, data_len, real_encoder_tag)

                daudio_write_pos.append(daudio_sub_w_pos)
                daudio_write_len.append(daudio_sub_w_len)

            phase_txt_write_pos_list.append(txt_write_pos)
            phase_txt_write_len_list.append(txt_write_len)
            phase_pinyin_write_pos_list.append(pinyin_write_pos)
            phase_pinyin_write_len_list.append(pinyin_write_len)
            phase_shiyi_write_pos_list.append(shiyi_write_pos)
            phase_shiyi_write_len_list.append(shiyi_write_len)
            phase_audio_write_pos_list.append(audio_write_pos)
            phase_audio_write_len_list.append(audio_write_len)
            phase_daudio_write_pos_list.append(daudio_write_pos)
            phase_daudio_write_len_list.append(daudio_write_len)

        # 写 跟读 内容
        sentence_txt_write_pos_list = []
        sentence_txt_write_len_list = []

        for i in range(len(chapters)):
            chapter = chapters[i]
            sentence = chapter.get_newSentence()
            txt_write_pos = []
            txt_write_len = []

            for iw in range(len(sentence)):
                txt = sentence[iw].get('lrc')
                # txt_len = 4 * int((len(txt) * 2 + 2) / 4)
                txt_utf_8_len = len(txt.encode('utf-8'))
                txt_len = 4 * int((txt_utf_8_len + 3) / 4)

                # 跟读 文本内容
                txt_write_pos.append(ziyou_file.tell())
                txt_write_len.append(txt_len)
                checksum_new, checksum_error = write_data_to_file(ziyou_file, txt, txt_len, real_encoder_tag)
                if 0 != checksum_error:
                    print(f"[打包错误]写入跟读 {txt} 文本错误")
                    return

            sentence_txt_write_pos_list.append(txt_write_pos)
            sentence_txt_write_len_list.append(txt_write_len)


        # 回写 头部填充地址，长度

        # 填充章节头地址
        chapter_cnts = len(chapters)
        print(f'章节数： {chapter_cnts}')
        head_cnts = len(chapter_head_list_pos)
        print('章节头地址数：', head_cnts)
        if chapter_cnts != head_cnts:
            print('章节数和预留信息格式不符，请检查工具代码')
            return
        words_pos_cnt = len(chapter_words_addr)
        if chapter_cnts != words_pos_cnt:
            print('章节数和字信息格式不符，请检查工具代码')
            return
        phase_pos_cnt = len(chapter_phase_addr)
        if chapter_cnts != phase_pos_cnt:
            print('章节数和词信息格式不符，请检查工具代码')
            return
        sentence_pos_cnt = len(chapter_sentence_addr)
        if chapter_cnts != sentence_pos_cnt:
            print('章节数和跟读信息格式不符，请检查工具代码')
            return
        recite_pos_cnt = len(chapter_recite_addr)
        if chapter_cnts != recite_pos_cnt:
            print('章节数和背诵信息格式不符，请检查工具代码')
            return
        for i in range(chapter_cnts):
            chapter_head_pos = chapter_head_list_pos[i]
            # print(f'第 {i+1} 章节地址 {chapter_head_pos}')
            ziyou_file.seek(chapter_head_pos, 0)
            chapter_name_pos = chapter_name_write_pos_list[i]
            chapter_name_len = chapter_name_write_len_list[i]
            word_pos = chapter_words_addr[i]
            # print(f'第 {i+1} 章节 字描述地址 {word_pos}')
            phase_pos = chapter_phase_addr[i]
            # print(f'第 {i+1} 章节 词描述地址 {phase_pos}')
            sentence_pos = chapter_sentence_addr[i]
            # print(f'第 {i+1} 章节 跟读描述地址 {sentence_pos}')
            recite_pos = chapter_recite_addr[i]
            # print(f'第 {i+1} 章节 背诵描述地址 {recite_pos}')

            zhanwei_list.remove(chapter_head_pos)
            zhanwei_list.remove(chapter_head_pos + 4)
            zhanwei_list.remove(chapter_head_pos + 8)
            zhanwei_list.remove(chapter_head_pos + 12)
            zhanwei_list.remove(chapter_head_pos + 16)
            zhanwei_list.remove(chapter_head_pos + 20)

            write_data = chapter_name_pos ^ real_encoder_tag
            check_sum += (write_data & 0xffff)
            check_sum += ((write_data & 0xffff0000) >> 16)
            check_len += 4
            ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

            write_data = chapter_name_len ^ real_encoder_tag
            check_sum += (write_data & 0xffff)
            check_sum += ((write_data & 0xffff0000) >> 16)
            check_len += 4
            ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

            write_data = word_pos ^ real_encoder_tag
            check_sum += (write_data & 0xffff)
            check_sum += ((write_data & 0xffff0000) >> 16)
            check_len += 4
            ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

            write_data = phase_pos ^ real_encoder_tag
            check_sum += (write_data & 0xffff)
            check_sum += ((write_data & 0xffff0000) >> 16)
            check_len += 4
            ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

            write_data = sentence_pos ^ real_encoder_tag
            check_sum += (write_data & 0xffff)
            check_sum += ((write_data & 0xffff0000) >> 16)
            check_len += 4
            ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

            write_data = recite_pos ^ real_encoder_tag
            check_sum += (write_data & 0xffff)
            check_sum += ((write_data & 0xffff0000) >> 16)
            check_len += 4
            ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

        # 填充字
        for i in range(chapter_cnts):
            chapter = chapters[i]
            new_words = chapter.get_newWord()
            word_num = len(new_words)
            word_num_pos = words_num_pos_list[i]
            word_addr_pos = words_addr_list[i]

            txt_write_pos = word_txt_write_pos_list[i]
            txt_write_len = word_txt_write_len_list[i]

            pinyin_write_pos = word_pinyin_write_pos_list[i]
            pinyin_write_len = word_pinyin_write_len_list[i]

            word_audio_list = words_audio_addr_post_list[i]
            audio_write_pos = word_audio_write_pos_list[i]
            audio_write_len = word_audio_write_len_list[i]

            word_daudio_list = words_daudio_addr_post_list[i]
            daudio_write_pos = word_daudio_write_pos_list[i]
            daudio_write_len = word_daudio_write_len_list[i]

            word_zuci_list = words_zuci_addr_post_list[i]
            zuci_write_pos = word_zuci_write_pos_list[i]
            zuci_write_len = word_zuci_write_len_list[i]

            print(f'第{i + 1}章节字个数{word_num}')
            if len(word_num_pos) != word_num:
                print(f'第 {i+1} 章节字个数加载信息不匹配')
                return
            for j in range(word_num):
                word_pos = word_num_pos[j]
                word_addr = word_addr_pos[j]

                word_audio_pos = word_audio_list[j]
                audio_sub_w_pos = audio_write_pos[j]
                audio_sub_w_len = audio_write_len[j]

                word_daudio_pos = word_daudio_list[j]
                daudio_sub_w_pos = daudio_write_pos[j]
                daudio_sub_w_len = daudio_write_len[j]

                word_zuci_pos = word_zuci_list[j]
                zuci_sub_w_pos = zuci_write_pos[j]
                zuci_sub_w_len = zuci_write_len[j]


                # print(f'第 {i+1} 章节 第 {j+1} 字地址 {word_pos} -> {word_addr}')
                ziyou_file.seek(word_pos, 0)
                write_data = word_addr ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))
                zhanwei_list.remove(word_pos)

                # 字 txt 位置
                txt_pos = txt_write_pos[j]
                txt_len = txt_write_len[j]
                ziyou_file.seek(word_addr, 0)

                write_data = txt_pos ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                write_data = txt_len ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                # 字 拼音 位置
                pinyin_pos = pinyin_write_pos[j]
                pinyin_len = pinyin_write_len[j]
                # ziyou_file.seek(word_addr, 0)

                write_data = pinyin_pos ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                write_data = pinyin_len ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                zhanwei_list.remove(word_addr)
                zhanwei_list.remove(word_addr + 4)
                zhanwei_list.remove(word_addr + 8)
                zhanwei_list.remove(word_addr + 12)

                # 字 音频位置
                audios = new_words[j].get('audio')
                audios_cnt = 0
                if audios:
                    audios_cnt = len(audios)
                for k in range(audios_cnt):
                    audio_pos = word_audio_pos[k]
                    audio_w_pos = audio_sub_w_pos[k]
                    audio_w_len = audio_sub_w_len[k]
                    ziyou_file.seek(audio_pos, 0)

                    write_data = audio_w_pos ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    write_data = audio_w_len ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    zhanwei_list.remove(audio_pos)
                    zhanwei_list.remove(audio_pos + 4)

                # 字 听写音频位置
                daudios = new_words[j].get('daudio')
                daudios_cnt = 0
                if daudios:
                    daudios_cnt = len(daudios)
                for k in range(daudios_cnt):
                    daudio_pos = word_daudio_pos[k]
                    daudio_w_pos = daudio_sub_w_pos[k]
                    daudio_w_len = daudio_sub_w_len[k]
                    ziyou_file.seek(daudio_pos, 0)

                    write_data = daudio_w_pos ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    write_data = daudio_w_len ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    zhanwei_list.remove(daudio_pos)
                    zhanwei_list.remove(daudio_pos + 4)

                # 字 组词位置
                zucis = new_words[j].get('zuci')
                zucis_cnt = 0
                if zucis:
                    zucis_cnt = len(zucis)
                for k in range(zucis_cnt):
                    zuci_pos = word_zuci_pos[k]
                    zuci_w_pos = zuci_sub_w_pos[k]
                    zuci_w_len = zuci_sub_w_len[k]
                    ziyou_file.seek(zuci_pos, 0)

                    write_data = zuci_w_pos ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    write_data = zuci_w_len ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    zhanwei_list.remove(zuci_pos)
                    zhanwei_list.remove(zuci_pos + 4)

        # 填充词
        for i in range(chapter_cnts):
            chapter = chapters[i]
            new_phase = chapter.get_newPhase()
            phases_num = len(new_phase)
            phase_num_pos = phase_num_pos_list[i]
            phase_addr_pos = phase_addr_list[i]

            txt_write_pos = phase_txt_write_pos_list[i]
            txt_write_len = phase_txt_write_len_list[i]

            pinyin_write_pos = phase_pinyin_write_pos_list[i]
            pinyin_write_len = phase_pinyin_write_len_list[i]

            phase_audio_list = phase_audio_addr_post_list[i]
            audio_write_pos = phase_audio_write_pos_list[i]
            audio_write_len = phase_audio_write_len_list[i]

            phase_daudio_list = phase_daudio_addr_post_list[i]
            daudio_write_pos = phase_daudio_write_pos_list[i]
            daudio_write_len = phase_daudio_write_len_list[i]

            phase_shiyi_list = phase_shiyi_addr_post_list[i]
            shiyi_write_pos = phase_shiyi_write_pos_list[i]
            shiyi_write_len = phase_shiyi_write_len_list[i]

            print(f'第{i + 1}章节词个数{phases_num}')
            if len(phase_num_pos) != phases_num:
                print(f'第 {i+1} 章节词个数加载信息不匹配')
                return
            for j in range(phases_num):
                phase_pos = phase_num_pos[j]
                phase_addr = phase_addr_pos[j]

                phase_audio_pos = phase_audio_list[j]
                audio_sub_w_pos = audio_write_pos[j]
                audio_sub_w_len = audio_write_len[j]

                phase_daudio_pos = phase_daudio_list[j]
                daudio_sub_w_pos = daudio_write_pos[j]
                daudio_sub_w_len = daudio_write_len[j]

                phase_shiyi_pos = phase_shiyi_list[j]
                shiyi_sub_w_pos = shiyi_write_pos[j]
                shiyi_sub_w_len = shiyi_write_len[j]

                # print(f'第 {i+1} 章节 第 {j+1} 词地址 {phase_pos} -> {phase_addr}')
                ziyou_file.seek(phase_pos, 0)
                write_data = phase_addr ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                zhanwei_list.remove(phase_pos)

                # 词 txt 位置
                txt_pos = txt_write_pos[j]
                txt_len = txt_write_len[j]
                ziyou_file.seek(phase_addr, 0)

                write_data = txt_pos ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                write_data = txt_len ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                # 词 拼音 位置
                pinyin_pos = pinyin_write_pos[j]
                pinyin_len = pinyin_write_len[j]
                # ziyou_file.seek(word_addr, 0)

                write_data = pinyin_pos ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                write_data = pinyin_len ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                zhanwei_list.remove(phase_addr)
                zhanwei_list.remove(phase_addr + 4)
                zhanwei_list.remove(phase_addr + 8)
                zhanwei_list.remove(phase_addr + 12)

                # 词 音频位置
                audios = new_phase[j].get('audio')
                audios_cnt = 0
                if audios:
                    audios_cnt = len(audios)
                for k in range(audios_cnt):
                    audio_pos = phase_audio_pos[k]
                    audio_w_pos = audio_sub_w_pos[k]
                    audio_w_len = audio_sub_w_len[k]
                    ziyou_file.seek(audio_pos, 0)

                    write_data = audio_w_pos ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    write_data = audio_w_len ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    zhanwei_list.remove(audio_pos)
                    zhanwei_list.remove(audio_pos + 4)

                # 词 听写音频位置
                daudios = new_phase[j].get('daudio')
                daudios_cnt = 0
                if daudios:
                    daudios_cnt = len(daudios)
                for k in range(daudios_cnt):
                    daudio_pos = phase_daudio_pos[k]
                    daudio_w_pos = daudio_sub_w_pos[k]
                    daudio_w_len = daudio_sub_w_len[k]
                    ziyou_file.seek(daudio_pos, 0)

                    write_data = daudio_w_pos ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    write_data = daudio_w_len ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    zhanwei_list.remove(daudio_pos)
                    zhanwei_list.remove(daudio_pos + 4)

                # 词 释义位置
                shiyis = new_phase[j].get('shiyi')
                shiyis_cnt = 0
                if shiyis:
                    shiyis_cnt = len(shiyis)
                for k in range(shiyis_cnt):
                    shiyi_pos = phase_shiyi_pos[k]
                    shiyi_w_pos = shiyi_sub_w_pos[k]
                    shiyi_w_len = shiyi_sub_w_len[k]
                    ziyou_file.seek(shiyi_pos, 0)

                    write_data = shiyi_w_pos ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    write_data = shiyi_w_len ^ real_encoder_tag
                    check_sum += (write_data & 0xffff)
                    check_sum += ((write_data & 0xffff0000) >> 16)
                    check_len += 4
                    ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                    zhanwei_list.remove(shiyi_pos)
                    zhanwei_list.remove(shiyi_pos + 4)

        # 填充跟读
        for i in range(chapter_cnts):
            chapter = chapters[i]
            sentence = chapter.get_newSentence()
            sentence_num = len(sentence)
            sentence_num_pos = sentence_num_pos_list[i]
            sentence_addr_pos = sentence_addr_list[i]

            txt_write_pos = sentence_txt_write_pos_list[i]
            txt_write_len = sentence_txt_write_len_list[i]

            print(f'第{i+1}章节跟读配置个数{sentence_num}')
            if len(sentence_num_pos) != sentence_num:
                print(f'第 {i+1} 章节跟读个数加载信息不匹配')
                return
            for j in range(sentence_num):
                sentence_pos = sentence_num_pos[j]
                sentence_addr = sentence_addr_pos[j]

                # print(f'第 {i+1} 章节 第 {j+1} 跟读地址 {sentence_pos} -> {sentence_addr}')
                ziyou_file.seek(sentence_pos, 0)
                write_data = sentence_addr ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                zhanwei_list.remove(sentence_pos)

                # 跟读 txt 位置
                txt_pos = txt_write_pos[j]
                txt_len = txt_write_len[j]
                ziyou_file.seek(sentence_addr, 0)

                write_data = txt_pos ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                write_data = txt_len ^ real_encoder_tag
                check_sum += (write_data & 0xffff)
                check_sum += ((write_data & 0xffff0000) >> 16)
                check_len += 4
                ziyou_file.write(write_data.to_bytes(length=4, byteorder='little', signed=False))

                zhanwei_list.remove(sentence_addr)
                zhanwei_list.remove(sentence_addr + 4)

        # print(f'占位个数：{len(zhanwei_list)}: {zhanwei_list}')
        ziyou_file.seek(BOOK_TIME_LEN)
        ziyou_file.write(check_len.to_bytes(length=4, byteorder='little', signed=False))
        ziyou_file.write(check_sum.to_bytes(length=4, byteorder='little', signed=False))
        print('校验 {%d} {%x}' % (check_len, check_sum))
        ziyou_file.close()
        print("数据写入完成")
        if warn_cnt > 0:
            print('有警告消息，请确认:', warning_msg)
    # except BaseException as e:
    #     print(f"[生成出错]写入数据段1出错: {e}")
    #     return

def usage(info):
    print("wrong used:", info)


if __name__ == "__main__":
    print(sys.argv)
    if (2 == len(sys.argv)):
        if os.path.isdir(sys.argv[1]):
            wst_gen(sys.argv[1], "new", 0)
        elif os.path.isfile(sys.argv[1]):
            wst_decode(sys.argv[1])
        else:
            usage()
    elif (3 == len(sys.argv)):
        if os.path.isdir(sys.argv[1]):
            if os.path.isfile(sys.argv[2]):
                wst_gen(sys.argv[1], sys.argv[2], 0)
            else:
                usage()
        else:
            usage()
    else:
        usage()
