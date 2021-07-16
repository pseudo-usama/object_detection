// The code to generate this data structure is here: indexing\one_graphical_obj\index.py

a = {
    1: {    // Indicate that graphical objs are 1
        1: {    // Width & height ratio of graphical obj
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
