// The code to generate this data structure is here: indexing\two_graphical_objs\index.py

a = {
    2: {    // Indicate that graphical objs are 2
        1: {   // Angles obj
            1: {   // Ratio of corners of objs (explanation of calculation is given below)
                1: {    // No. of SBBs
                    1: [    // No. of DBBs
                        {   // Obj for single image data
                            sbb: [{ val: 'some text', pos: [1, 1], size: [1, 1] }],
                            dbb: [{ regex: '/^([a-zA-Z0-9_-]){3,5}$/' }],
                            img: 'img.jpg'
                        }
                    ]
                }
            }
        }
    }
}

/*
    Calculation of corners ratio of objects

    Object 1                            Object 2
    c1 ---------- c2                    c5 ---------- c6
    |             |                     |             |
    |             |                     |             |
    |             |                     |             |
    |             |                     |             |
    c3 ---------- c4                    c7 ---------- c8

    The ratio is calculated using this formula:
        ratio1 = distanceOf(c1, c5) / distanceOf(c4, c8)
        ratio2 = distanceOf(c2, c6) / distanceOf(c3, c7)
        finalRatio = ratio1 / ratio2
*/
