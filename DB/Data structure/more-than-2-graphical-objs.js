// The code to generate this data structure is here: indexing\more_than_three_graphical_objs\index.py


a = {
    3: {    // n graphical objects
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
