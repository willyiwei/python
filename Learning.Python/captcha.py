#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys, os, re
import Image,ImageFilter
try:
    import psyco
    psyco.full()
except ImportError:
    pass

class CaptchaAlgorithm(object):
    '''captcha algorithm'''
    def LevenshteinDistance(self, m, n):
        c = [[i] for i in range(0, len(m)+1)]
        c[0] = [j for j in range(0, len(n)+1)]

        for i in range(0, len(m)):
            for j in range(0, len(n)):
                c[i+1].append(
                    min(
                        c[i][j+1] + 1,
                        c[i+1][j] + 1,
                        c[i][j] + (0 if m[i] == n[j] else 1)
                    )
                )

        return c[-1][-1]

class CaptchaImageAlgorithm(object):
    '''captcha image algorithm'''
    def GetPixelsXEdges(self, im):
        pixels = im.load()
        xsize, ysize = im.size
        state = -1
        edges = []
        for x in xrange(xsize):
            weight = sum(1 if pixels[x, y]==0 else 0 for y in xrange(ysize))
            level = 0
            if state == -1 and weight <= level:
                continue
            elif state == 1 and weight > level:
                continue
            else:
                state = -state
                edges.append(x)
        return [(edges[x], edges[x+1]) for x in range(0, len(edges), 2)]

    def GetPixelsYEdges(self, im):
        pixels = im.load()
        xsize, ysize = im.size
        state = -1
        edges = []
        for y in xrange(ysize):
            weight = sum(1 if pixels[x, y]==0 else 0 for x in xrange(xsize))
            level = 0
            if state == -1 and weight <= level:
                continue
            elif state == 1 and weight > level:
                continue
            else:
                state = -state
                edges.append(y)
        return [(edges[x], edges[x+1]) for x in range(0, len(edges), 2)]

    def StripYEdge(self, im):
        yedges = self.GetPixelsYEdges(im)
        y1, y2 = yedges[0][0], yedges[-1][1]
        return im.crop((0, y1, im.size[0], y2))

    def GetBinaryMap(im):
        xsize, ysize = im.size
        pixels = im.load()
        return '\n'.join(''.join('#' if  pixels[x, y] == 0 else '_' for x in xrange(xsize)) for y in xrange(ysize))

class CaptchaProfile(object):
    def fiter(self, im):
        raise NotImplemented
    def split(self, im):
        raise NotImplemented
    def match(self, im):
        raise NotImplemented

class CaptchaProfile_360Buy(CaptchaProfile):

    __FEATURES_MAP__ = {
                        '''
                        __#####__
                        _#____#__
                        ##_____##
                        #______##
                        ##_____#_
                        #______##
                        ##_______
                        #______##
                        ##_____#_
                        ____##___
                        __##_#___
                        '''
                        :
                        '0',

                        '''
                        ____##___
                        __##_#___
                        ____##___
                        ____#____
                        ____##___
                        ____#____
                        ____##___
                        ____#____
                        ____##___
                        ____#____
                        __##_###_
                        '''
                        :
                        '1',

                        '''
                        _#_______
                        ##____##_
                        ##_____##
                        _______#_
                        ______##_
                        _____#___
                        ____##___
                        ___#_____
                        __##_____
                        _#_______
                        #########
                        '''
                        :
                        '2',

                        '''
                        _######__
                        #_____#__
                        ##_____##
                        _______#_
                        ______##_
                        ___###___
                        ______##_
                        _______##
                        ##_____#_
                        #_____#__
                        _####_#__
                        '''
                        :
                        '3',

                        '''
                        ______##_
                        _____#_#_
                        ____#_##_
                        ___#__#__
                        __#___##_
                        _#____#__
                        #_____##_
                        #####_##_
                        ______#__
                        ______##_
                        ______#__
                        '''
                        :
                        '4',

                        '''
                        _########
                        _#_______
                        _##______
                        _#_______
                        _######__
                        ______#__
                        _______##
                        _______#_
                        ##_____##
                        #_____#__
                        _####_#__
                        '''
                        :
                        '5',

                        '''
                        ___#####_
                        __#______
                        _##______
                        #________
                        ##_####__
                        #_#___#__
                        ##_____##
                        #______#_
                        ##_____##
                        _##___#__
                        __###_#__
                        '''
                        :
                        '6',

                        '''
                        #########
                        ________#
                        ______##_
                        ______#__
                        _____##__
                        _____#___
                        ____#____
                        ____##___
                        ___#_____
                        ___##____
                        __#______
                        '''
                        :
                        '7',

                        '''
                        __#####__
                        _#____#__
                        ##_____##
                        #______#_
                        _##___##_
                        __###_#__
                        _#____##_
                        ##_____##
                        #______#_
                        _##___#__
                        __###_#__
                        '''
                        :
                        '8',

                        '''
                        __#####__
                        _#____##_
                        _#_____##
                        ##______#
                        #______##
                        _##___##_
                        __###__##
                        _______#_
                        ______##_
                        _____#___
                        _###_#___
                        '''
                        :
                        '9',
                        }

    def filter(self, im):
        return im.filter(ImageFilter.EDGE_ENHANCE_MORE).convert('L').convert('1')

    def split(self, im):
        matrix = {
                    4 : [(20, 4, 29, 15), (31, 4, 40, 15)],
                    5 : [(20, 4, 29, 15), (31, 4, 40, 15), (42, 4, 51, 15)],
                    6 : [(20, 4, 29, 15), (31, 4, 40, 15), (42, 4, 51, 15), (53, 4, 62, 15)],
                 }
        xsize, ysize = im.size
        length = int(round(xsize/16.0))
        return [im.crop(box) for box in matrix[length]]

    def match(self, im):
        def __feature_to_data(feature):
            feature = re.sub(r'[\t\s]', '', feature)
            feature = re.sub(r'[\r\n]', '', feature)
            return tuple(0 if x == '#' else 255 for x in feature)
        source = im.getdata()
        algorithm = CaptchaAlgorithm()
        minimal = min(self.__FEATURES_MAP__, key=lambda feature:algorithm.LevenshteinDistance(source, __feature_to_data(feature)))
        return self.__FEATURES_MAP__[minimal]

class CaptchaProfile_NewEgg(CaptchaProfile):

    __FEATURES_MAP__ = {
                        '''
                        __#####__
                        _##___##_
                        ##_____##
                        ##_____##
                        ##_____##
                        ##_____##
                        ##_____##
                        ##_____##
                        ##_____##
                        _##___##_
                        __#####__
                        '''
                        :
                        '0',

                        '''
                        __###__
                        #####__
                        __#_#__
                        __###__
                        __#_#__
                        __###__
                        __#_#__
                        __###__
                        __#_#__
                        __###__
                        #######
                        '''
                        :
                        '1',

                        '''
                        _#####___
                        _#___###_
                        #______#_
                        ______##_
                        _____#_#_
                        _____###_
                        ____###__
                        ___####__
                        ___##____
                        _##______
                        #########
                        '''
                        :
                        '2',

                        '''
                        _######__
                        ##____##_
                        ##_____##
                        _______##
                        ______##_
                        ___####__
                        ______##_
                        _______##
                        ##_____##
                        ##____##_
                        _######__
                        '''
                        :
                        '3',

                        '''
                        _____####_
                        _____###__
                        ____#_#___
                        ___##_##__
                        __##__#___
                        __##__##__
                        _##___#___
                        ##########
                        ______#___
                        ______##__
                        ______###_
                        '''
                        :
                        '4',

                        '''
                        _########
                        _##______
                        _##______
                        _##______
                        _######__
                        ______##_
                        _______##
                        _______##
                        ##_____##
                        ##____##_
                        _######__
                        '''
                        :
                        '5',

                        '''
                        ___#####_
                        __##_____
                        _##______
                        ###______
                        _#_####__
                        #_#___##_
                        ##____###
                        ###___#_#
                        ###___##_
                        _##___##_
                        __#####__
                        '''
                        :
                        '6',

                        '''
                        #########
                        ______##_
                        _____#_#_
                        ____###__
                        ____###__
                        ____##___
                        ___#_#___
                        __###____
                        __###____
                        _###_____
                        _###_____
                        '''
                        :
                        '7',

                        '''
                        __#####__
                        _##___##_
                        ##_____##
                        ##_____##
                        _##___##_
                        __#####__
                        _##___##_
                        ##_____##
                        ##_____##
                        _##___##_
                        __#####__
                        '''
                        :
                        '8',

                        '''
                        __#####__
                        _##___##_
                        ##_____##
                        ##_____##
                        ##_____##
                        _##___###
                        __####_##
                        _______##
                        ______##_
                        _____##__
                        _#####___
                        '''
                        :
                        '9',
                        }

    def filter(self, im):
        return im.convert('RGB').convert('L').filter(ImageFilter.EDGE_ENHANCE).filter(ImageFilter.SHARPEN).convert('1')

    def split(self, im):
        xsize, ysize = im.size
        xedges = CaptchaImageAlgorithm().GetPixelsXEdges(im)
        im_list = [CaptchaImageAlgorithm().StripYEdge(im.crop((x1,0,x2,ysize))) for (x1,x2) in xedges[1:len(xedges)-3]]
        return im_list

    def match(self, im):
        def __feature_to_data(feature):
            feature = re.sub(r'[\t\s]', '', feature)
            feature = re.sub(r'[\r\n]', '', feature)
            return tuple(0 if x == '#' else 255 for x in feature)
        source = im.getdata()
        algorithm = CaptchaAlgorithm()
        minimal = min(self.__FEATURES_MAP__, key=lambda feature:algorithm.LevenshteinDistance(source, __feature_to_data(feature)))
        return self.__FEATURES_MAP__[minimal]

def captcha(filename, profile):
    im = Image.open(filename)
    im = profile.filter(im)
    im_list = profile.split(im)
    return ''.join(profile.match(im) for im in im_list)

def captcha_360buy(filename):
    return captcha(filename, CaptchaProfile_360Buy())

def captcha_newegg(filename):
    return captcha(filename, CaptchaProfile_NewEgg())

def test():
    print captcha_360buy(sys.argv[1])

if __name__ == '__main__':
    test()
